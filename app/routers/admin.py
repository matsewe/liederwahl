from fastapi import APIRouter, HTTPException, Security, File, UploadFile
from app.models import GoogleFile
from app.dependencies import dbEngine
from app.routers.user import get_current_user
import gspread
from gspread.urls import DRIVE_FILES_API_V3_URL
import pandas as pd
import numpy as np

router = APIRouter(
    prefix="/admin",
    dependencies=[Security(get_current_user, scopes=["admin"])],
    responses={404: {"description": "Not found"}},
)

gc = gspread.service_account(filename="service_account.json")  # type: ignore

google_files: dict[str, GoogleFile] = {}

spreadsheets: dict[str, gspread.Spreadsheet] = {}  # type: ignore

selected_worksheets: dict[tuple[str, int], bool] = {}


def fetch_files():
    if not (google_files):
        for s in gc.http_client.request("get", DRIVE_FILES_API_V3_URL).json()["files"]: #
            google_files[s["id"]] = GoogleFile(
                file_id=s["id"], file_name=s["name"])


def load_spreadsheet(file_id):
    if file_id not in spreadsheets:
        spreadsheets[file_id] = gc.open_by_key(file_id)


# Route to get google files (sheets)
@router.get("/files")
async def get_files() -> dict[str, GoogleFile]:
    fetch_files()
    return google_files


@router.get("/files/{file_id}")
def get_worksheets(file_id: str) -> dict[int, str]:
    fetch_files()
    if file_id not in google_files:
        raise HTTPException(status_code=404, detail="Spreadsheet not found.")

    load_spreadsheet(file_id)

    # type: ignore
    return {ws.id: ws.title for ws in spreadsheets[file_id].worksheets()}


@router.get("/selected_worksheets")
def list_selected_worksheet() -> dict[tuple[str, int], bool]:
    return selected_worksheets


@router.post("/selected_worksheets")
def select_worksheet(file_id: str, worksheet_id: int, ignore_arrangement: bool = False):
    selected_worksheets[(file_id, worksheet_id)] = ignore_arrangement


@router.delete("/selected_worksheets")
def deselect_worksheet(file_id: str, worksheet_id: int):
    del selected_worksheets[(file_id, worksheet_id)]


@router.post("/process_worksheets")
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

    song_list.to_sql(name='songs', con=dbEngine,
                     index=False, if_exists='append')
    # song_list.to_csv("song-list.csv")


@router.post("/process_file")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}