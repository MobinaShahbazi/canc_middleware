SELECT
            bi.code AS "varCode",
            bid.code,
            bid.title
        FROM
            base_info bi
            INNER JOIN base_info_detail AS bid ON bi.pid = bid.base_info_id
        ORDER BY
            "varCode"