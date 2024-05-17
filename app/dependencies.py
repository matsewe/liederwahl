import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

Base = automap_base()

dbEngine = sqlalchemy.create_engine('sqlite:///db.sqlite')

dbSession = Session(dbEngine)

Base.prepare(dbEngine, reflect=True)
