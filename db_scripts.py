import collections
import json
import pyodbc

RX_CONNECTION_STRING='DRIVER={SQL Server};SERVER=localhost;DATABASE=RXBackend;Trusted_Connection=yes'
CIPS_CONNECTION_STRING='DRIVER={SQL Server};SERVER=localhost;DATABASE=CIPS;Trusted_Connection=yes'

# Returs JSON array from database
def get_json(sql):
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    result = cur.execute(sql)

    items = [dict(zip([key[0] for key in cur.description], row)) for row in result]

    return items

insert_occurence = """ INSERT INTO [dbo].[RPT_OCCUR]
            ([USER_ID]
            ,[DISCOVER_DATE]
            ,[OCCUR_DATE]
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
            ,[CREATED_AT]
            ,[CREATED_BY])
        VALUES
            (?
            ,?
            ,?
            ,?
            ,?
            ,?
            ,?
            ,?
            ,?
            ,?
            ,?
            ,?
            ,?
            ,?
            ,?
            ,?
            ,?
            ,?
            ,?
            ,GETDATE()
            ,?) """

update_occurence = """ UPDATE [dbo].[RPT_OCCUR]
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
        ,[COOKING] = ?
        ,[OTHER] =  ?
        ,[TECH_ID] =  ?
        ,[RPH_ID] =  ?
        ,[EXPLANATION] =  ?
        ,[UPDATED_AT] = GETDATE()
        ,[UPDATED_BY] = ?
    WHERE ID = ?
"""

get_reasons_by_category = """ SELECT 
        [ID]
        ,[CATEGORY_CODE]
        ,r.[DESCRIPTION] as REASON_DESC
        ,[SORT_ORDER]
        ,c.[DESCRIPTION] as CATEGORY_DESC
        ,c.[CODE]
        ,[CREATED_BY]
        ,[CREATED]
        ,[LAST_USER]
        ,[LAST_UPDATE]
        ,[ACTIVE]
    FROM [dbo].[RPT_REASONS] r
    INNER JOIN [RPT_CATEGORIES]c
    on r.[CATEGORY_CODE] = c.CODE
    ORDER BY [SORT_ORDER]"""

update_users = """ UPDATE [dbo].[RPT_USERS]
    SET [USERNAME] = ?
        ,[FIRST_NAME] = ?
        ,[LAST_NAME] = ?
        ,[POSITION] = ?
        ,[PASSWORD] = ?
        ,[SALT] = 'NOTIMPLEMENTED'
        ,[UPDATED_AT] = GETDATE()
        ,[UPDATED_BY] = ?
        ,[ACTIVE] = ?
        ,[INITIALS] = ?
    WHERE ID = ?
"""

get_users_username = """ 
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
    WHERE [ROW_NUM] = 1  AND [USERNAME] = ?"""

get_users = """ 
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
            ,[SALT]
            ,[UPDATED_AT]
            ,[UPDATED_BY]
            ,[ACTIVE]
            ,[INITIALS]
            ,r.[ROLE_ID]
			,r.DESCRIPTION as ROLE_NAME
    FROM [dbo].[RPT_USERS] u LEFT JOIN 
    (SELECT * FROM CTE) r
    on u.[ID] = r.[USER_ID]
    WHERE [ROW_NUM] = 1 
    ORDER BY [USERNAME]"""

get_facilities = """ SELECT 
        [ID]
        ,[DCODE]
        ,[DNAME]
    FROM [dbo].[_FAC]
    ORDER BY [DCODE]
"""

def reason_codes (filter):
    if filter != "":
        filter = " WHERE CODE LIKE '%" + filter + "%'"
    else:
        filter = ""
    return """SELECT r.*, c.DESCRIPTION as CATEGORY FROM dbo.RPT_REASONS r 
    LEFT JOIN dbo.RPT_CATEGORIES c ON r.CATEGORY_CODE = c.CODE """ 
    + filter + """ ORDER BY CATEGORY_CODE, SORT_ORDER"""

category_codes = "SELECT * FROM dbo.RPT_CATEGORIES"

insert_reasons = """ INSERT INTO dbo.RPT_REASONS
        ([CATEGORY_CODE]
        ,[DESCRIPTION]
        ,[SORT_ORDER]
        ,[CREATED_BY]
        ,[CREATED])
        VALUES
        (?,?,?,?,GETDATE())"""

update_reasons = """ UPDATE dbo.RPT_REASONS
    SET [CATEGORY_CODE] = ?
        ,[DESCRIPTION] = ?
        ,[SORT_ORDER] = ?
        ,[LAST_USER] = ?
        ,[LAST_UPDATE] = GETDATE()
        ,[ACTIVE] = ?
    WHERE [ID] = ? """
