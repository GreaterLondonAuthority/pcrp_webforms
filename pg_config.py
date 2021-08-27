import os

connection_details = {
    "host"     : os.getenv("PCRP_POSTGRES_HOST"),
    "user"     : os.getenv("PCRP_POSTGRES_USER"),
    "password" : os.getenv("PCRP_POSTGRES_PASSWORD"),
    "database" : "lbsm"
}

connection = "host={host} user={user} password={password} dbname={database}".format_map(connection_details)
