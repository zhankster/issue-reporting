UPDATE [dbo].[RPT_OCCUR]
   SET [USER_ID] = ?
      ,[DISCOVER_DATE] = ?
      ,[OCCUR_DATE] = ?
      ,[USERNAME] = ?
      ,[FACILITY_CODE] = ? 
      ,[PATIENT_NAME] =  ?
      ,[PERSON_REPORTING] = ?
      ,[PHONE] = ?
      ,[PERSON_COMPLETING] = ?
      ,[ORDER_INTAKE] = ?
      ,[MEDICATION] = ?
      ,[SHIPPING] = ?
      ,[DELIVERY] = ?
      ,[BILLING] =  ?
      ,[COOKING] = ?>
      ,[OTHER] =  ?
      ,[TECH_ID] =  ?
      ,[RPH_ID] =  ?
      ,[EXPLANATION] =  ?
      ,[UPDATED_AT] = GETDATE()
      ,[UPDATED_BY] = ?
 WHERE ID = ?
GO




    ;WITH CTE AS (
    SELECT USER_ID, ROLE_ID, r.DESCRIPTION,
    ROW_NUMBER ( )   OVER (PARTITION BY USER_ID ORDER BY USER_ID, ROLE_ID ) as [ROW_NUM]
    FROM [dbo].[RPT_USER_ROLE] u
	INNER JOIN [RPT_ROLES] r
	on u.ROLE_ID = r.ID
    )
    SELECT u.[ID]
            ,[USERNAME]
            ,[FIRST_NAME]
            ,[LAST_NAME]
            ,[POSITION]
            ,[PASSWORD]
            ,[ACTIVE]
            ,[INITIALS]
            ,r.[ROLE_ID]
			,r.DESCRIPTION as ROLE_NAME
    FROM [dbo].[RPT_USERS] u LEFT JOIN 
    (SELECT * FROM CTE) r
    on u.[ID] = r.[USER_ID]
    WHERE [ROW_NUM] = 1  AND [USERNAME] = 'hanka'

SELECT
    ISNULL(
        (SELECT DISTINCT FIL_PRICE
        FROM TO_UPS
        ORDER BY FIL_PRICE DESC
        LIMIT 1 OFFSET 1
        ), null) as SecondHighestSalary
FROM TO_UPS
LIMIT 1

SELECT ID
                        ,CONVERT(char(10),[DISCOVER_DATE],126) as DISCOVER_DATE
                        ,CONVERT(char(10), [OCCUR_DATE],126) as OCCUR_DATE
                        ,[USERNAME]
                        ,[FACILITY_CODE]
                        ,[CREATED_BY]
                        ,[USERNAME]
                        ,[FACILITY_CODE]
                        ,[PATIENT_NAME]
                        ,[PERSON_REPORTING]
                        ,[PHONE]
                        ,[PERSON_COMPLETING]
                        ,[ORDER_INTAKE]
                        ,[MEDICATION]
                        ,[SHIPPING]
                        ,[DELIVERY]
                        ,[BILLING]
                        ,[COOKING]
                        ,[OTHER]
                        ,[TECH_ID]
                        ,[RPH_ID]
                        ,[EXPLANATION]
                        FROM dbo.[RPT_OCCUR] WHERE [ID] = 3

SELECT ID
                        ,CONVERT(char(10)
                        ,DISCOVER_DATE,126) as DISCOVER_DATE
                        ,CONVERT(char(10), OCCUR_DATE,126) as OCCUR_DATE
                        ,FACILITY_CODE, CREATED_BY
                        ,USERNAME
                        FROM dbo.RPT_OCCUR
                     WHERE  ( DISCOVER_DATE >= '2019-11-25' AND DISCOVER_DATE <= '2020-04-09' )

[{'ID': 3, 'DISCOVER_DATE': '2020-01-27', 'OCCUR_DATE': '2020-01-26', 'FACILITY_CODE': 'MCJ   ', 'CREATED_BY': 'HDA   ', 'USERNAME': 'hanka'}, 
{'ID': 4, 'DISCOVER_DATE': '2020-01-28', 'OCCUR_DATE': '2020-01-08', 'FACILITY_CODE': 'DJ    ', 'CREATED_BY': 'HDA   ', 'USERNAME': 'hanka'}]
select *  FROM dbo.RPT_OCCUR



