SELECT DISTINCT
	oer.pid :: INTEGER AS equipment_id,
	oec.survey_id :: VARCHAR AS survey_id,
	oecr.respond :: JSONB AS survey_respond,
	oe.title,
	oer.created_by_user_id :: VARCHAR AS created_by,
	oecr.created_date AS fillDate
FROM
	operation_entity_checklist_respond oecr
	LEFT JOIN operation_entity_respond oer ON oecr.operation_entity_respond_id = oer.pid
	LEFT JOIN operation_entity_check_list oec ON oec.pid = oecr.operation_entity_check_list_id
	LEFT JOIN operation_entity oe ON oe.pid = oer.operation_entity_id
WHERE
	oecr.deleted = FALSE
	AND oer.deleted = FALSE