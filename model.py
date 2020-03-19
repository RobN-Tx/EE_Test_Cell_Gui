# model.py
 
from sqlalchemy import Table, Column, create_engine
from sqlalchemy import Integer, ForeignKey, String, Unicode, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relation
 
engine = create_engine("sqlite:///test_config.db", echo=True)
DeclarativeBase = declarative_base(engine)
metadata = DeclarativeBase.metadata
 
########################################################################
class OlvBook(object):
    """
    Book model for ObjectListView
    """
 
    #----------------------------------------------------------------------
    def __init__(self, id, title, config_value, comment, is_list):
        self.id = id  # unique row id from database
        self.title = title
        self.config_value = config_value        
        self.comment = comment
        self.is_list = is_list

 

########################################################################
class Book(DeclarativeBase):
    """"""
    __tablename__ = "config"
 
    id = Column(Integer, primary_key=True)
    
    title = Column("title", Unicode)
    config_value = Column("config_value", Unicode)
    comment = Column("comment", Unicode)
    is_list = Column("is_list", Boolean, default=False)
    #person = relation("Person", backref="books", cascade_backrefs=False)
 
metadata.create_all()


