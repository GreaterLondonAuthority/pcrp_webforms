-- Table: pcrp.pcrp_webform_submitted_data;

-- DROP TABLE pcrp.pcrp_webform_submitted_data;

CREATE TABLE IF NOT EXISTS pcrp.pcrp_webform_submitted_data
(
    nid integer NOT NULL,
    sid integer NOT NULL,
    cid integer NOT NULL,
    no varchar(128),
    data text
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE pcrp.pcrp_webform_submitted_data
    OWNER to pcrp_gla_admin;

ALTER TABLE pcrp.pcrp_webform_submitted_data ADD CONSTRAINT nid_sid_cid_no PRIMARY KEY (nid, sid, cid, no);

GRANT INSERT, SELECT, UPDATE, DELETE ON TABLE pcrp.pcrp_webform_submitted_data TO lbsm_full_role;

GRANT SELECT ON TABLE pcrp.pcrp_webform_submitted_data TO pcrp_feed;

GRANT ALL ON TABLE pcrp.pcrp_webform_submitted_data TO pcrp_gla_admin;

GRANT INSERT, SELECT, UPDATE ON TABLE pcrp.pcrp_webform_submitted_data TO pcrp_webform_import;

COMMENT ON TABLE pcrp.pcrp_matt_test
    IS 'Stores all submitted field data for webform submissions. Data originates from the webform_submitted_data table in Drupal.';
