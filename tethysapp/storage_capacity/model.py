# Put your persistent store models in this file
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker

from .app import StorageCapacity as app

engine = app.get_persistent_store_engine('fdc_db')
SessionMaker = sessionmaker(bind=engine)
Base = declarative_base()


class FlowDurationData(Base):
    """
    sqlalchemy table definition for storing address points.
    """
    __tablename__ = 'flow_duration_data'

    # columns
    id = Column(Integer, primary_key=True)
    site = Column(String)
    percent = Column(Integer)
    flow = Column(Float)
    units = Column(String)

    def __init__(self, site, percent, flow, units):
        """
        Constructor
        """
        self.site = site
        self.percent = percent
        self.flow = flow
        self.units = units