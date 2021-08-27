SELECT
    wc.name AS "Field name",
    wsd.data AS "Data"
    -- wc.type AS "Field type"
    -- wf.s3_url AS "S3 URL"
    -- wf.*
FROM
    pcrp.pcrp_webform_submitted_data wsd
    LEFT JOIN pcrp.pcrp_webform_component wc ON wc.cid = wsd.cid AND wc.nid = wsd.nid
    -- LEFT JOIN pcrp.pcrp_webform_files wf ON wf.fid = CAST(wsd.data AS INTEGER) AND wc.type = 'file' WHERE wc.type = 'file'
WHERE
    sid = 820883
    -- AND wc.type = 'file'
    AND wsd.data != ''
ORDER BY
    wsd.cid,
    wsd.no
;