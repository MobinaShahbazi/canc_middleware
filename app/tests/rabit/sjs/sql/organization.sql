SELECT
	gid,
	title as org_title,
	city,
	province 
FROM
	organization 
WHERE
	deleted = FALSE