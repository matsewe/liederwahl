import sqlalchemy

dbEngine = sqlalchemy.create_engine('sqlite:///db.sqlite')

def get_token_header():
    pass