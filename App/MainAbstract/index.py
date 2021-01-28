from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import urllib
from flask import Flask
########################################################################################DataBase@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2
#connection string
params = urllib.parse.quote_plus('Driver={SQL Server};'
        'Server=YoussefSami;'
        'Database=CLS_DB2;'
        'Trusted_Connection=yes;')
#init flas app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS']='Content-Type'
app.config['Access-Control-Allow-Origin'] ='*'
app.config["DEBUG"]=True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =True
app.config['TESTING']=True
app.config['SECRET_KEY']='thisissecretkey'
#init db
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
db=SQLAlchemy(app)

#create modules for database
class Entity_list_user(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    NationalID = db.Column(db.String(250),nullable=False)
    FirstName = db.Column(db.String(250), nullable=False)
    LastName = db.Column(db.String(250), nullable=False)
    Email = db.Column(db.String(250), nullable=False)
    Password = db.Column(db.String(250), nullable=False)
    FacultyID = db.Column(db.String(250))
    Faculty = db.Column(db.String(250))
    Dept = db.Column(db.String(250))
    UserType=db.Column(db.String(250),nullable=False)


class Entity_list_Attendance(db.Model):
    ID = db.Column(db.Integer, primary_key=True, )
    FacultyID = db.Column(db.String(250),nullable=False)
    Name = db.Column(db.String(250), nullable=False)
    Time = db.Column(db.String(250), nullable=False)
    InOut = db.Column(db.String(250), nullable=False)
    Date = db.Column(db.Date, nullable=False)
    db.ForeignKeyConstraint(
        ['FacultyID'], ['Entity_list_user.FacultyID'],
        name='fk_FacultyID'
    )


