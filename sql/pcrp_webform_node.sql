-- Table: pcrp.pcrp_webform_node;

-- DROP TABLE pcrp.pcrp_webform_node;

CREATE TABLE IF NOT EXISTS pcrp.pcrp_webform_node
(
    nid integer UNIQUE NOT NULL,
    vid integer,
    status integer,
    title varchar(255),
    created integer,
    changed integer
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE pcrp.pcrp_webform_node
    OWNER to pcrp_gla_admin;

GRANT INSERT, SELECT, UPDATE, DELETE ON TABLE pcrp.pcrp_webform_node TO lbsm_full_role;

GRANT SELECT ON TABLE pcrp.pcrp_webform_node TO pcrp_feed;

GRANT ALL ON TABLE pcrp.pcrp_webform_node TO pcrp_gla_admin;

GRANT INSERT, SELECT, UPDATE ON TABLE pcrp.pcrp_webform_node TO pcrp_webform_import;

COMMENT ON TABLE pcrp.pcrp_matt_test
    IS 'Stores all submitted field data for webform submissions. Data originates from the webform_submitted_data table in Drupal.';
