-- Table: pcrp.pcrp_webform_component;

-- DROP TABLE pcrp.pcrp_webform_component;

CREATE TABLE IF NOT EXISTS pcrp.pcrp_webform_component
(
    nid integer NOT NULL,
    cid integer NOT NULL,
    pid integer,
    form_key varchar(128),
    name text,
    type varchar(16),
    value text,
    weight integer
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE pcrp.pcrp_webform_component ADD CONSTRAINT nid_cid PRIMARY KEY (nid, cid);

ALTER TABLE pcrp.pcrp_webform_component
    OWNER to pcrp_gla_admin;

GRANT INSERT, SELECT, UPDATE, DELETE ON TABLE pcrp.pcrp_webform_component TO lbsm_full_role;

GRANT SELECT ON TABLE pcrp.pcrp_webform_component TO pcrp_feed;

GRANT ALL ON TABLE pcrp.pcrp_webform_component TO pcrp_gla_admin;

GRANT INSERT, SELECT, UPDATE ON TABLE pcrp.pcrp_webform_component TO pcrp_webform_import;

COMMENT ON TABLE pcrp.pcrp_matt_test
    IS 'Stores information about webform components (fields). Data originates from the webform_component table in Drupal.';
