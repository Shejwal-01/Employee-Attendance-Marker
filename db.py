import mysql.connector

def get_connection():
    try:
        db = mysql.connector.connect(host ="localhost", user = "root", passwd = "shejwal", database = "attendance_system")
        return db
        
    
    except Exception as msg:
        print(msg)
        return None