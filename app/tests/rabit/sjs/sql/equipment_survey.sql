SELECT DISTINCT
	                            oe.survey_id,
	                            oe.title AS survey_name,
	                            s.description AS description,
	                            s.survey_json :: JSONB
                                FROM
	                            operation_entity oe
	                            LEFT JOIN survey s ON s.gid = oe.survey_id
                                WHERE
	                            s.deleted = FALSE