import os
WEBFORM_NIDS = ["60672", "61930"]
S3_BUCKET_NAME = "pcrp-webform-files"
EFS_MOUNT_TARGET = os.getenv("EFS_MOUNT_TARGET", "drupal_private_files")
WEBFORM_FILES_PATH = os.getenv("WEBFORM_FILES_PATH", "webform_files")
