import psycopg

# def main():
#     pgdb = psycopg.connect(pg_config.connection)
#     pgcursor = pgdb.cursor()
#     pgcursor.execute("SELECT * FROM pcrp.pcrp_matt_test")
#     for x in pgcursor:
#         print(x)
#     pgcursor.close()
#     pgdb.close()


def connect(config):
    try:
        pgdb = psycopg.connect(config)
    except Exception as e:
        print("ERROR: Could not connect to database due to {0}".format(e))
        return(None)
    return(pgdb)

# if __name__ == "__main__":
#     main()


