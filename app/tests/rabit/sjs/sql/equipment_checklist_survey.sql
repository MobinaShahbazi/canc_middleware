SELECT DISTINCT
	oec.survey_id AS survey_id,
	s."name" :: VARCHAR AS survey_name,
	s.description :: VARCHAR AS survey_description,
	s.survey_json :: JSONB
FROM
	operation_entity_checklist_respond oecr
	LEFT JOIN operation_entity_check_list oec ON oec.pid = oecr.operation_entity_check_list_id
	LEFT JOIN survey s ON s.gid = oec.survey_id
WHERE
	oecr.deleted = FALSE