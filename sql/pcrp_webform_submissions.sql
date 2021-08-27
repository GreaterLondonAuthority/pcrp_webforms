-- Table: pcrp.pcrp_webform_submissions;

-- DROP TABLE pcrp.pcrp_webform_submissions;

CREATE TABLE IF NOT EXISTS pcrp.pcrp_webform_submissions
(
    sid integer UNIQUE NOT NULL,
    nid integer NOT NULL,
    serial integer NOT NULL,
    uid integer NOT NULL,
    submitted integer,
    completed integer,
    modified integer,
    remote_addr character varying COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE pcrp.pcrp_webform_submissions
    OWNER to pcrp_gla_admin;

GRANT INSERT, SELECT, UPDATE, DELETE ON TABLE pcrp.pcrp_webform_submissions TO lbsm_full_role;

GRANT SELECT ON TABLE pcrp.pcrp_webform_submissions TO pcrp_feed;

GRANT ALL ON TABLE pcrp.pcrp_webform_submissions TO pcrp_gla_admin;

GRANT INSERT, SELECT, UPDATE ON TABLE pcrp.pcrp_webform_submissions TO pcrp_webform_import;

COMMENT ON TABLE pcrp.pcrp_matt_test
    IS 'Holds general information about Drupal webform submissions for Be Seen. Data originates from the webform_submissions table in Drupal.';
