SELECT DISTINCT
	e.pid,
	s.gid :: VARCHAR AS survey_id,
	e.respond :: JSONB AS survey_respond,
	oe.title,
	e.created_by_user_id :: VARCHAR AS created_by,
	e.modified_date :: TIMESTAMP,
	e.created_date :: VARCHAR AS fillDate
FROM
	operation_entity_respond e
	INNER JOIN operation_entity oe ON oe."pid" = e."operation_entity_id"
	LEFT JOIN survey s ON oe.survey_id = s.gid
WHERE
	e.deleted = FALSE and s.deleted = FALSE