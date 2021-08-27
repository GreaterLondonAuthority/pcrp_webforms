import constants
import mysql_config
import mysql_connect

import pg_config
import pg_connect

def main():
    import_webform_components()

def import_webform_components():
    components = get_webform_components(constants.WEBFORM_NIDS)
    import_components(components)


def get_webform_components(nids):
    fields = ["nid", "cid", "pid", "form_key", "name", "type", "value", "weight"]
    mydb = mysql_connect.connect(mysql_config.connection)
    
    if mydb is None:
        return()

    mycursor = mydb.cursor(dictionary=True)
    query = "SELECT {0} FROM londongov.webform_component WHERE nid IN ({1})".format(",".join(fields), ",".join(nids))
    mycursor.execute(query)
    components = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return(components)
    

def import_components(components):
    pgdb = pg_connect.connect(pg_config.connection)
    if pgdb is None:
        return()
    pgcursor = pgdb.cursor()
    
    for component in components:
        import_component(pgcursor, component)
        pgdb.commit()

    pgcursor.close()
    pgdb.close()

def import_component(cursor, component):
    print("Importing component {0} ({1}) for webform {2}".format(component.get("form_key"), component.get("cid"), component.get("nid")))
    query = """INSERT INTO pcrp.pcrp_webform_component 
                 (nid, cid, pid, form_key, name, type, value, weight)
               VALUES
                 (%s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT ON CONSTRAINT nid_cid
                 DO UPDATE SET
                   pid = %s,
                   form_key = %s,
                   name = %s,
                   type = %s,
                   value = %s,
                   weight = %s;"""
    data = (
        component.get("nid"),
        component.get("cid"),
        component.get("pid"),
        component.get("form_key"),
        component.get("name"),
        component.get("type"),
        component.get("value"),
        component.get("weight"),
        component.get("pid"),
        component.get("form_key"),
        component.get("name"),
        component.get("type"),
        component.get("value"),
        component.get("weight")
    )
    cursor.execute(query, data)


if __name__ == "__main__":
    main()
