import mysql.connector

def connect(config):
    try:
        mydb = mysql.connector.connect(**config)
    except Exception as e:
        print("ERROR: Could not connect to database due to {0}".format(e))
        return(None)
    return(mydb)
