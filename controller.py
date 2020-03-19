# controller.py
from model import Book, OlvBook
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
#----------------------------------------------------------------------
def addRecord(data):
    """
    Data should be a tuple of two dictionaries in the following format:
 
    ("author":{"first_name":"John", "last_name":"Doe"},
     "book":{"title":"Some book", "isbn":"1234567890", 
             "publisher":"Packt"}
    )
    """
    book = Book()
    book.title = data["book"]["title"]
    book.config_value = data["book"]["config_value"]
    book.comment = data["book"]["comment"]
    book.is_list = data["book"]["is_list"]
    
 
    # connect to session and commit data to database
    session = connectToDatabase()
    session.add(book)
    session.commit()
    session.close()
 
#----------------------------------------------------------------------
def connectToDatabase():
    """
    Connect to our SQLite database and return a Session object
    """
    engine = create_engine("sqlite:///test_config.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
 
#----------------------------------------------------------------------
def convertResults(results):
    """
    Convert results to OlvBook objects
    """
    
    books = []
    for record in results:
        book = OlvBook(record.id, record.title, 
                       record.config_value, record.comment,
                       record.is_list
                       )    
        books.append(book)
    return books
 
#----------------------------------------------------------------------
def deleteRecord(idNum):
    """
    Delete a record from the database
    """
    session = connectToDatabase()
    record = session.query(Book).filter_by(id=idNum).one()
    session.delete(record)
    session.commit()
    session.close()
 
#----------------------------------------------------------------------
def editRecord(idNum, row):
    """
    Edit a record
    """
    session = connectToDatabase()
    record = session.query(Book).filter_by(id=idNum).one()
    print
    record.title = row["title"]
    record.config_value = row["config_value"]
    record.comment = row["comment"]
    record.is_list = row["is_list"]
    session.add(record)
    session.commit()
    session.close()
 
#----------------------------------------------------------------------
def getAllRecords():
    """
    Get all records and return them
    """
    session = connectToDatabase()
    result = session.query(Book).all()
    books = convertResults(result)
    session.close()
    return books
 
#----------------------------------------------------------------------
def searchRecords(filterChoice, keyword):
    """
    Searches the database based on the filter chosen and the keyword
    given by the user
    """
    session = connectToDatabase()
    if  filterChoice == "Title":
        qry = session.query(Book)
        result = qry.filter(Book.title.contains('%s' % keyword)).all()
    elif filterChoice == "config_value":
        qry = session.query(Book)
        result = qry.filter(Book.config_value.contains('%s' % keyword)).all()
    elif filterChoice == "is_list":
        qry = session.query(Book)
        result = qry.filter(Book.is_list == True).all()
    else:
        qry = session.query(Book)
        result = qry.filter(Book.comment.contains('%s' % keyword)).all()    
    books = convertResults(result)
    
    return books