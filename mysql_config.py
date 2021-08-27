import os

connection = {
    "host"     : os.getenv("PCRP_MYSQL_HOST"),
    "user"     : os.getenv("PCRP_MYSQL_USER"),
    "password" : os.getenv("PCRP_MYSQL_PASSWORD"),
    "database" : "webforms"
}
