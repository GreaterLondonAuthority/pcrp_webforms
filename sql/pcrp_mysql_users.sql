CREATE USER IF NOT EXISTS 'pcrp_readonly'@'%';
GRANT USAGE ON webforms.* TO 'pcrp_readonly'@'%';
GRANT SELECT ON `webforms`.`webform_submissions` TO 'pcrp_readonly'@'%';
GRANT SELECT ON `webforms`.`webform_submitted_data` TO 'pcrp_readonly'@'%';
GRANT SELECT ON `londongov`.`file_managed` TO 'pcrp_readonly'@'%';
GRANT SELECT ON `londongov`.`node` TO 'pcrp_readonly'@'%';
GRANT SELECT ON `londongov`.`webform_component` TO 'pcrp_readonly'@'%';
