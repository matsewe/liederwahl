from fastapi import FastAPI, HTTPException
from models import Genre, Song, GoogleFile
import gspread
from types import MethodType
from typing import Any
import pandas as pd
import numpy as np
import sqlalchemy


app = FastAPI()

dbEngine = sqlalchemy.create_engine('sqlite:///db.sqlite')

gc = gspread.service_account(filename="service_account.json") # type: ignore

google_files: dict[str, GoogleFile] = {}

spreadsheets: dict[str, gspread.Spreadsheet] = {} # type: ignore

selected_worksheets: dict[tuple[str, int], bool] = {}

def fetch_files():
    if not(google_files):
        for s in gc.http_client.request("get", gspread.http_client.DRIVE_FILES_API_V3_URL).json()["files"]: # type: ignore
            google_files[s["id"]] = GoogleFile(file_id = s["id"], file_name = s["name"])

def load_spreadsheet(file_id):
    if file_id not in spreadsheets:
        spreadsheets[file_id] = gc.open_by_key(file_id)

@app.get("/")
def root():
    return {"message": "Hello World"}

# Route to get google files (sheets)
@app.get("/admin/files")
def get_files() -> dict[str, GoogleFile]:
    fetch_files()
    return google_files

@app.get("/admin/files/{file_id}")
def get_worksheets(file_id: str) -> dict[int, str]:
    fetch_files()
    if file_id not in google_files:
        raise HTTPException(status_code=404, detail="Spreadsheet not found.")
    
    load_spreadsheet(file_id)

    return {ws.id : ws.title for ws in spreadsheets[file_id].worksheets()} # type: ignore
    
@app.get("/admin/selected_worksheets")
def list_selected_worksheet() -> dict[tuple[str, int], bool]:
    return selected_worksheets

@app.post("/admin/selected_worksheets")
def select_worksheet(file_id: str, worksheet_id: int, ignore_arrangement: bool = False):
    selected_worksheets[(file_id, worksheet_id)] = ignore_arrangement

@app.delete("/admin/selected_worksheets")
def deselect_worksheet(file_id: str, worksheet_id: int):
    del selected_worksheets[(file_id, worksheet_id)]

@app.post("/admin/process_worksheets")
def process_worksheets():
    fetch_files()

    song_list = []

    for (file_id, worksheet_id), ignore_arrangement in selected_worksheets.items():
        load_spreadsheet(file_id)
        worksheet = spreadsheets[file_id].get_worksheet_by_id(worksheet_id)
        worksheet_df = pd.DataFrame(worksheet.get_all_records())

        last_column = np.where(worksheet_df.columns == "Kommentare")[0][0]

        worksheet_df = worksheet_df.iloc[:, 0:last_column+1]

        worksheet_df["Ignore Arrangement"] = ignore_arrangement

        song_list.append(worksheet_df)

    song_list = pd.concat(song_list)

    song_list.to_sql(name = 'songs', con = dbEngine, index = False, if_exists = 'append') 
    # song_list.to_csv("song-list.csv")




# 1PMy17eraogNUz436w3aZKxyij39G1didaN02Ka_-45Q
# 71046222