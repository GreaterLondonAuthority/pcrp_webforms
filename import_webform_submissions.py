import subprocess
import os
import logging
import boto3
from botocore.exceptions import ClientError

import constants
import mysql_config
import mysql_connect

import pg_config
import pg_connect

def main():
    import_webform_submissions()


def import_webform_submissions():
    mydb = mysql_connect.connect(mysql_config.connection)
    pgdb = pg_connect.connect(pg_config.connection)

    if mydb is None:
        print("Could not connect to the database.")
        return()

    if pgdb is None:
        print("Could not connect to the database.")
        return()

    for nid in constants.WEBFORM_NIDS:

        file_components = get_webform_file_components(mydb, nid)

        print("\n-----------------------------------------------------------------------------")
        print("Importing submissions for {0} ({1})\n".format(get_webform_title(pgdb, nid), nid))
        latest_submission = get_latest_submission_id(mydb, nid)
        latest_imported_submission = get_latest_submission_id(pgdb, nid)

        if latest_imported_submission is None:
            latest_imported_submission = 0

        print("Latest submission for webform {0}:          {1}".format(nid, latest_submission))
        print("Latest imported submission for webform {0}: {1}".format(nid, latest_imported_submission))

        if latest_imported_submission >= latest_submission:
            print("\nNo new submissions to import for webform {0}".format(nid))
            continue

        submissions = get_webform_submissions(mydb, nid, latest_imported_submission)
        if len(submissions) == 0:
            print("No submissions to import for webform {0}!".format(nid))
            continue

        print("\n{0} new submissions to import for webform {1}.\n".format(len(submissions), nid))
        for submission in submissions:
            print("Importing submission {0} for webform {1}.".format(submission.get("sid"), nid))
            import_webform_submission(pgdb, submission)
            submitted_data = get_webform_submitted_data(mydb, submission.get("sid"))
            for data in submitted_data:
                if data.get("cid") in file_components:
                    import_webform_file(mydb, pgdb, data.get("data"))
                    # download_filename = download_webform_file(get_drupal_instance_ip(), get_webform_file_uri(pgdb, data.get("data")))
                    download_filename = copy_webform_file(get_webform_file_uri(pgdb, data.get("data")), constants.WEBFORM_FILES_PATH)
                    upload_file_to_s3(download_filename, constants.S3_BUCKET_NAME, data.get("data"))
                import_webform_submitted_data(pgdb, data)

    pgdb.commit()
    pgdb.close()
    mydb.close()
    print("\n")


def get_latest_submission_id(db_connection, nid):

    if db_connection.__class__.__name__ == "CMySQLConnection":
        webform_submissions_table = "webforms.webform_submissions"
    else:
        webform_submissions_table = "pcrp.pcrp_webform_submissions"

    query = "SELECT MAX(sid) FROM {0} WHERE nid = %s".format(webform_submissions_table)

    cursor = db_connection.cursor()
    cursor.execute(query, (nid,))
    # @todo Get some error handling in here and check for results
    submission_id = cursor.fetchone()[0]
    cursor.close()
    return(submission_id)
    

def get_webform_submissions(db_connection, nid, latest_imported_submission):
    query = """
            SELECT
              sid,
              nid,
              serial,
              uid,
              submitted,
              completed,
              modified,
              remote_addr
            FROM
              webforms.webform_submissions
            WHERE
              nid = %s
              AND sid > %s
            """
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute(query, (nid, latest_imported_submission))
    submissions = cursor.fetchall()
    cursor.close()
    return(submissions)


def import_webform_submission(db_connection, submission):
    query = """
            INSERT INTO
                pcrp.pcrp_webform_submissions (
                    sid,
                    nid,
                    serial,
                    uid,
                    submitted,
                    completed,
                    modified,
                    remote_addr
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            ON CONFLICT (sid)
                DO UPDATE SET
                   nid = %s,
                   serial = %s,
                   uid = %s,
                   submitted = %s,
                   completed = %s,
                   modified = %s,
                   remote_addr = %s;
            """

    data = (
        submission.get("sid"),
        submission.get("nid"),
        submission.get("serial"),
        submission.get("uid"),
        submission.get("submitted"),
        submission.get("completed"),
        submission.get("modified"),
        submission.get("remote_addr"),
        submission.get("nid"),
        submission.get("serial"),
        submission.get("uid"),
        submission.get("submitted"),
        submission.get("completed"),
        submission.get("modified"),
        submission.get("remote_addr")
    )
    cursor = db_connection.cursor()
    cursor.execute(query, data)
    cursor.close()

def import_webform_submitted_data(db_connection, submitted_data):
    query = """
            INSERT INTO
                pcrp.pcrp_webform_submitted_data (
                    nid,
                    sid,
                    cid,
                    no,
                    data
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            ON CONFLICT ON CONSTRAINT nid_sid_cid_no
                DO UPDATE SET
                   data = %s;
            """

    data = (
        submitted_data.get("nid"),
        submitted_data.get("sid"),
        submitted_data.get("cid"),
        submitted_data.get("no"),
        submitted_data.get("data"),
        submitted_data.get("data")
    )
    cursor = db_connection.cursor()
    cursor.execute(query, data)
    cursor.close()
            

def get_webform_submitted_data(db_connection, sid):
    query = """
            SELECT
                nid,
                sid,
                cid,
                no,
                data
            FROM
                webforms.webform_submitted_data
            WHERE
                sid = %s
            """
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute(query, (sid,))
    submitted_data = cursor.fetchall()
    cursor.close()
    return(submitted_data)



def get_webform_file_components(db_connection, nid):
    query = """
            SELECT
                cid
            FROM
                londongov.webform_component
            WHERE
                type = 'file'
                AND nid = %s
            """
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute(query, (nid,))
    results = cursor.fetchall()
    cursor.close()
    cids = []
    for result in results:
        cids.append(result.get("cid"))

    return(cids)

def import_webform_file(mydb, pgdb, fid):
    query = """
            SELECT
                *
            FROM
                londongov.file_managed
            WHERE
                fid = %s
            """
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(query, (fid,))
    files = mycursor.fetchall()
    mycursor.close()
    if len(files) == 0:
        return()

    pgcursor = pgdb.cursor()
    for file in files:
        s3_url = "https://{0}.s3.eu-west-2.amazonaws.com/{1}".format(constants.S3_BUCKET_NAME, os.path.basename(file.get("uri")))
        query = """
                INSERT INTO
                    pcrp.pcrp_webform_files (
                        fid,
                        filename,
                        filemime,
                        uri,
                        s3_url,
                        status,
                        type,
                        timestamp
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                ON CONFLICT (fid)
                    DO UPDATE SET
                    filename = %s,
                    filemime = %s,
                    uri = %s,
                    s3_url = %s,
                    status = %s,
                    type = %s,
                    timestamp = %s;
                """
        data = (
            file.get("fid"),
            file.get("filename"),
            file.get("filemime"),
            file.get("uri"),
            s3_url,
            file.get("status"),
            file.get("type"),
            file.get("timestamp"),
            file.get("filename"),
            file.get("filemime"),
            file.get("uri"),
            s3_url,
            file.get("status"),
            file.get("type"),
            file.get("timestamp")
        )
        pgcursor.execute(query, data)

    pgcursor.close()


def get_webform_file_uri(db_connection, fid):
    query = """
            SELECT
                uri
            FROM
                pcrp.pcrp_webform_files
            WHERE
                fid = %s
            """
    cursor = db_connection.cursor()
    cursor.execute(query, (fid,))
    # @todo Check we have some results
    file_details = cursor.fetchone()
    cursor.close()
    uri = file_details[0]
    # print(" * Downloading file {0}".format(uri))
    return(uri)


def get_drupal_instance_ip():
    return_value = None
    client = boto3.client("ec2")
    response = client.describe_instances(
        Filters=[
            {
                'Name': 'tag:AnsibleHostGroup',
                'Values': [
                    'londongovDrupal',
                ]
            },
            {
                'Name': 'tag:Environment',
                'Values': [
                    'production',
                ]
            },
        ]
    )

    if not response.get("Reservations"):
        print("No drupal instances found.")
        return return_value

    return_value = response.get("Reservations")[0].get("Instances")[0].get("PrivateIpAddress")
    return(return_value)
    

def download_webform_file(host, uri, destination_folder="webform_files"):
    filepath = uri.replace("private://", "")
    filename = os.path.basename(filepath)
    local_username = os.environ.get('USER')
    file_copy = subprocess.run([
        "ssh",
        "-q",
        host,
        "mkdir -p ~/pcrp_webform_files",
        "&& sudo cp $DRUPAL_PRIVATE_FILES_PATH/{0}".format(filepath),
        "/home/{0}/pcrp_webform_files".format(local_username),
        "&& sudo chown {0}:{0} /home/{0}/pcrp_webform_files/{1}".format(local_username, filename),
    ])
    file_download = subprocess.run([
        "scp",
        "-q",
        "{0}:/home/{1}/pcrp_webform_files/{2}".format(host, local_username, filename),
        destination_folder
    ])
    return("{0}/{1}".format(destination_folder, filename))

def copy_webform_file(uri, destination_folder="webform_files"):
    filepath = uri.replace("private://", "")
    filename = os.path.basename(filepath)
    subprocess.run(["sudo", "cp", "{0}/{1}".format(constants.EFS_MOUNT_TARGET, filepath), destination_folder])
    print(" * Copied file {0} to folder {1}.".format(filepath, destination_folder))
    return("{0}/{1}".format(destination_folder, filename))


def upload_file_to_s3(file_name, bucket, fid):
    object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    print(" * Uploaded file {0} ({2}) to S3 bucket {1}.".format(object_name, bucket, fid))
    return True


def get_webform_title(db_connection, nid):
    query = """SELECT title FROM pcrp.pcrp_webform_node WHERE nid = %s"""
    cursor = db_connection.cursor()
    cursor.execute(query, (nid,))
    node_details = cursor.fetchone()
    cursor.close()
    title = node_details[0]
    return(title)



if __name__ == "__main__":
    main()


