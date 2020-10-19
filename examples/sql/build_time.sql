WITH
  automate_build_time AS (
  SELECT
    build_id,
    user.group_id AS group_id,
    user.sub_group_id AS sub_group_id,
    MIN(TIMESTAMP(datetime_TRUNC(DATETIME(created_day),
          day))) created_day,
    DATETIME_DIFF(MAX((DATETIME_ADD(DATETIME(created_day),
            INTERVAL CAST(duration AS INT64) SECOND))),
      MIN(DATETIME(created_day)),
      SECOND) AS build_time,
    COUNT(DISTINCT hashed_id) session_count
  FROM
    automate.automate_test_sessions_partitioned sessions
  JOIN
    common.users users
  ON
    sessions.user.user_id = users.id
  LEFT JOIN
    common.sub_groups sub_groups
  ON
    sessions.user.sub_group_id = sub_groups.id
  WHERE
    duration IS NOT NULL
    AND build_id IS NOT NULL
    AND _PARTITIONTIME > "2018-05-09"
  GROUP BY
    build_id,
    user.group_id,
    user.sub_group_id )
SELECT
  FORMAT_TIMESTAMP('%F %T', automate_build_time.created_day ) AS automate_build_time_timeline,
  CASE
    WHEN SUM(automate_build_time.build_time) = 0 THEN 0
  ELSE
  TRUNC(SUM(automate_build_time.build_time) / COUNT(DISTINCT(automate_build_time.build_id)))/86400
END
  AS automate_build_time_average_build_time,
  ROUND(AVG(automate_build_time.session_count)) AS automate_build_time_average_session_count
FROM
  automate_build_time
WHERE
  automate_build_time.created_day  >= "2018-05-09"
GROUP BY
  1
ORDER BY
  1 DESC
LIMIT
  500
