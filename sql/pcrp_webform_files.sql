-- Table: pcrp.pcrp_webform_files;

-- DROP TABLE pcrp.pcrp_webform_files;

CREATE TABLE IF NOT EXISTS pcrp.pcrp_webform_files
(
    fid integer UNIQUE NOT NULL,
    filename varchar(255),
    filemime varchar(255),
    uri varchar(255),
    s3_url varchar(255),
    status integer,
    type varchar(50),
    timestamp integer
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE pcrp.pcrp_webform_files
    OWNER to pcrp_gla_admin;

GRANT INSERT, SELECT, UPDATE, DELETE ON TABLE pcrp.pcrp_webform_files TO lbsm_full_role;

GRANT SELECT ON TABLE pcrp.pcrp_webform_files TO pcrp_feed;

GRANT ALL ON TABLE pcrp.pcrp_webform_files TO pcrp_gla_admin;

GRANT INSERT, SELECT, UPDATE ON TABLE pcrp.pcrp_webform_files TO pcrp_webform_import;

COMMENT ON TABLE pcrp.pcrp_matt_test
    IS 'Stores information about files uploaded via Drupal webforms. Data originates from the file_managed table in Drupal.';
