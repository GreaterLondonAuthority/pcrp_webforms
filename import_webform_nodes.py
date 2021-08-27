import constants
import mysql_config
import mysql_connect

import pg_config
import pg_connect

def main():
    webforms = get_webforms(constants.WEBFORM_NIDS)
    import_webforms(webforms)

def import_webforms(webforms):
    pgdb = pg_connect.connect(pg_config.connection)
    if pgdb is None:
        return()
    pgcursor = pgdb.cursor()
    
    for webform in webforms:
        import_webform(pgcursor, webform)
        pgdb.commit()

    pgcursor.close()
    pgdb.close()

def import_webform(cursor, webform):
    query = """INSERT INTO pcrp.pcrp_webform_node 
                 (nid, vid, status, title, created, changed)
               VALUES
                 (%s, %s, %s, %s, %s, %s)
               ON CONFLICT (nid)
                 DO UPDATE SET
                   vid = %s,
                   status = %s,
                   title = %s,
                   created = %s,
                   changed =%s;"""
    data = (
        webform["nid"],
        webform["vid"],
        webform["status"],
        webform["title"],
        webform["created"],
        webform["changed"],
        webform["vid"],
        webform["status"],
        webform["title"],
        webform["created"], 
        webform["changed"]
    )
    cursor.execute(query, data)


def get_webforms(nids):
    node_type = "webform"
    node_status = 1
    fields = ["nid", "vid", "status", "title", "created", "changed"]

    mydb = mysql_connect.connect(mysql_config.connection)
    
    if mydb is None:
        return()

    mycursor = mydb.cursor(dictionary=True)
    query = "SELECT {0} FROM londongov.node WHERE type = %s AND status = %s AND nid IN ({1})".format(",".join(fields), ",".join(nids))
    mycursor.execute(query, (node_type, node_status))
    webforms = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return(webforms)

if __name__ == "__main__":
    main()
