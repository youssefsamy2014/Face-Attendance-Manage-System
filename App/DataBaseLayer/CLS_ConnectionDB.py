import pyodbc
from App.MainAbstract.CLS_MainAbstractModule import CLS


class CLS_ConnectionDB(CLS):
    def Connection(self):
        conn=pyodbc.connect('Driver={SQL Server};'
        'Server=YoussefSami;'
        'Database=CLS_DataBase;'
        'Trusted_Connection=yes;')
        return conn




