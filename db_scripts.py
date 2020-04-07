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

def add_activity(activity,user, description):
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    sql = """ INSERT INTO [RPT_ACTIVITY]
        ([ACTIVITY]
        ,[USER]
        ,[DESCRIPTION])
     VALUES
        (?
        ,?
        ,? )"""
    
    params=(( activity, int(user), description ))
    cur.execute(sql, params)
    conn.commit()

def get_signoff_users(filter):
    return """ SELECT RPT_OCCUR.ID,
    FORMAT (RPT_OCCUR.DISCOVER_DATE, 'MM/dd/yyyy ')  DISCOVER_DATE, 
    FORMAT (RPT_OCCUR.OCCUR_DATE, 'MM/dd/ yyyy ') OCCUR_DATE, 	
    RPT_OCCUR.CREATED_AT,
	CASE WHEN TECH_REQ_VERIFY <> 0 AND TECH_VERIFY_DATE IS NULL 
		THEN  RPT_USERS_TECH.FIRST_NAME + ' ' + RPT_USERS_TECH.LAST_NAME
	ELSE '' END AS TECH_NAME,
	CASE WHEN RPH_REQ_VERIFY <> 0 AND RPH_VERIFY_DATE IS NULL 
		THEN  RPT_USERS_RPH.FIRST_NAME + ' ' + RPT_USERS_RPH.LAST_NAME
	ELSE '' END AS RPH_NAME,
	CASE WHEN TECH_REQ_VERIFY <> 0 AND TECH_VERIFY_DATE IS NULL 
		THEN  TECH_ID
	ELSE 0 END AS TECH_ID_SIGN,
	CASE WHEN RPH_REQ_VERIFY <> 0 AND RPH_VERIFY_DATE IS NULL 
		THEN  RPH_ID
	ELSE 0 END AS RPH_ID_SIGN,
    RPT_USERS_TECH.FIRST_NAME + ' ' + RPT_USERS_TECH.LAST_NAME TECH,
    RPT_USERS_TECH.USERNAME  TECH_USERNAME,
    RPT_USERS_RPH.FIRST_NAME + ' ' + RPT_USERS_RPH.LAST_NAME RPH,
    RPT_USERS_RPH.USERNAME RPH_USERNAME,
    RPT_USERS_COMP.FIRST_NAME + ' ' + RPT_USERS_COMP.LAST_NAME PER_COMP,
	RPT_OCCUR.FACILITY_CODE, 
	RPT_OCCUR.PATIENT_NAME,  
	RPT_OCCUR.EXPLANATION,
    RPT_OCCUR.PHONE,
    FAC.DNAME,
	RPT_OCCUR.PERSON_REPORTING,
    RPT_REASONS.DESCRIPTION REASON,
	RPT_USERS_TECH.FIRST_NAME, RPT_USERS_TECH.LAST_NAME,
    RPT_USERS_RPH.FIRST_NAME, RPT_USERS_RPH.LAST_NAME,
    RPT_CATEGORIES.DESCRIPTION DEPT,
	RPT_OCCUR.TECH_REQ_VERIFY,
	RPT_OCCUR.TECH_VERIFY_DATE,
	RPT_OCCUR.RPH_REQ_VERIFY,
	RPT_OCCUR.RPH_VERIFY_DATE,
	RPT_OCCUR.TECH_ID,
	RPT_OCCUR.RPH_ID,
	RPT_OCCUR.PERSON_COMPLETING,
    RPT_OCCUR.TECH_VERIFY_DATE,
    RPT_OCCUR.RPH_VERIFY_DATE
FROM
    RXBackend.dbo.RPT_OCCUR RPT_OCCUR 
	LEFT OUTER JOIN RXBackend.dbo.RPT_REASONS RPT_REASONS ON
        RPT_OCCUR.REASON_CODE = RPT_REASONS.ID
        LEFT OUTER JOIN RXBackend.dbo.RPT_USERS RPT_USERS_RPH ON
        RPT_OCCUR.RPH_ID = RPT_USERS_RPH.ID
        LEFT OUTER JOIN RXBackend.dbo.RPT_USERS RPT_USERS_TECH ON
        RPT_OCCUR.TECH_ID = RPT_USERS_TECH.ID
        LEFT OUTER JOIN RXBackend.dbo.RPT_USERS RPT_USERS_COMP ON
        RPT_OCCUR.PERSON_COMPLETING = RPT_USERS_COMP.ID
        LEFT OUTER JOIN RXBackend.dbo.FAC FAC ON
        RPT_OCCUR.FACILITY_CODE = FAC.DCODE
        LEFT OUTER JOIN RXBackend.dbo.RPT_CATEGORIES RPT_CATEGORIES ON
        RPT_REASONS.CATEGORY_CODE = RPT_CATEGORIES.CODE
WHERE RPT_OCCUR.VALID= 1 AND ((RPH_REQ_VERIFY <> 0 AND RPH_VERIFY_DATE IS NULL) OR (TECH_REQ_VERIFY <> 0 AND TECH_VERIFY_DATE IS NULL) )"""+ filter 

get_occur_details = """  SELECT r.ID
                ,CONVERT(char(10),[DISCOVER_DATE],126) as DISCOVER_DATE
                ,CONVERT(char(10), [OCCUR_DATE],126) as OCCUR_DATE
                ,[USERNAME]
                ,[FACILITY_CODE]
                ,r.[CREATED_BY]
                ,[USERNAME]
                ,[FACILITY_CODE]
                ,f.[DNAME] as [FAC_NAME]
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
                ,[VALID]
                ,[REASON_CODE]
                ,c.CATEGORY_CODE
                ,r.ATTACHMENT
                ,r.UPLOAD
                ,CONVERT(varchar, [CREATED_AT], 23) as [CREATED_AT]
                ,r.TECH_REQ_VERIFY
                ,r.RPH_REQ_VERIFY
                FROM dbo.[RPT_OCCUR] r
                LEFT JOIN CIPS.dbo.[FAC] f
                ON r.[FACILITY_CODE] = f.DCODE
                LEFT JOIN RPT_REASONS c
                ON r.REASON_CODE = c.ID
                WHERE r.[ID] = ? """

update_groups = """ UPDATE [dbo].[RPT_GROUPS]
        SET [RECIPIENTS] = ?
        WHERE [TARGET] = ? AND [USAGE] = ? 
    """

get_recipients = """ SELECT [RECIPIENTS]
    FROM [RPT_GROUPS] 
    WHERE [TARGET] = ? AND [USAGE] = ? 
    """
get_facility_info = """ SELECT SHORT_NAME, f.DNAME  FROM CIPS.dbo.FAC f
	LEFT JOIN PGR p ON f.PGR_ID = p.ID
WHERE f.DCODE = ? """

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
            ,[REASON_CODE]
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
        ,[WHOLESALE] = ?
        ,[OTHER] =  ?
        ,[TECH_ID] =  ?
        ,[RPH_ID] =  ?
        ,[REASON_CODE] =  ?
        ,[EXPLANATION] =  ?
        ,[UPDATED_AT] = GETDATE()
        ,[UPDATED_BY] = ?
        ,[TECH_REQ_VERIFY] = ?
        ,[RPH_REQ_VERIFY] = ?
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
    WHERE [ACTIVE] = 1
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
        ,[EMAIL] = ?
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
            ,[EMAIL]
            ,r.[ROLE_ID]
			,r.DESCRIPTION as ROLE_NAME
    FROM [dbo].[RPT_USERS] u LEFT JOIN 
    (SELECT * FROM CTE) r
    on u.[ID] = r.[USER_ID]
    WHERE [ROW_NUM] = 1 AND [ACTIVE] = 1
    AND [USERNAME] = ?"""

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
            ,[EMAIL]
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
    FROM [dbo].[FAC]
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
