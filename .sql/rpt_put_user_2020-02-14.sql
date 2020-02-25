USE [RXBackend]
GO
ALTER PROC [dbo].[rpt_put_user]
	 @USERNAME VARCHAR(50)
	,@FIRST_NAME VARCHAR(20)
	,@LAST_NAME VARCHAR(20)
	,@POSITION VARCHAR(30)
	,@PASSWORD VARCHAR(160)
	,@ROLE INT
	,@INITIALS nchar(6)
	,@CREATED_BY nchar(6)
as

BEGIN
	INSERT INTO [dbo].[RPT_USERS]
			   ([USERNAME]
			   ,[FIRST_NAME]
			   ,[LAST_NAME]
			   ,[POSITION]
			   ,[PASSWORD]
			   ,[SALT]
			   ,[INITIALS]
			   ,[CREATED_BY])
		 VALUES
			   (@USERNAME
			   ,@FIRST_NAME
			   ,@LAST_NAME 
			   ,@POSITION
			   ,@PASSWORD
			   ,'NOTIMPLEMENTED'
			   ,@INITIALS
			   ,@CREATED_BY
			   )

	INSERT INTO [dbo].[RPT_USER_ROLE]
			   ([USER_ID]
			   ,[ROLE_ID])
		 VALUES
			   (SCOPE_IDENTITY()
			   ,@ROLE
			   )

END

------------------------------------------------------

INSERT INTO RPT_ROLES values('Administrator')
INSERT INTO RPT_ROLES values('PharmTech')
INSERT INTO RPT_ROLES values('ShipTech')
SELECT * FROM RPT_ROLES
pbkdf2:sha256:50000$tM7IW167$8a1dfeb0fc648485fbc8cb1b29fa813de9d66930d9cfc836378e9b2226032ce7
pbkdf2:sha256:150000$8fLPDdIq$af60c887df2cd50b775f6262e446b341763e7d7ca6c4c7ccf6b12d3464f70dfc

EXEC dbo.rpt_put_user 'hanka','Hank', 'Allen', 'Dev', 'pbkdf2:sha256:50000$tM7IW167$8a1dfeb0fc648485fbc8cb1b29fa813de9d66930d9cfc836378e9b2226032ce7'
		,1,'HDA','hanka'

SELECT * from RPT_USERS
SELECT * from RPT_USER_ROLE

;WITH CTE AS (
SELECT USER_ID, ROLE_ID,
ROW_NUMBER ( )   OVER (PARTITION BY USER_ID ORDER BY USER_ID, ROLE_ID ) as [ROW_NUM]
FROM [dbo].[RPT_USER_ROLE] r
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
  FROM [dbo].[RPT_USERS] u LEFT JOIN 
 (SELECT * FROM CTE) r
  on u.[ID] = r.[USER_ID]
  WHERE [ROW_NUM] = 1
  


  ;WITH CTE AS (
  SELECT USER_ID, ROLE_ID,
  ROW_NUMBER ( )   OVER (PARTITION BY USER_ID ORDER BY USER_ID, ROLE_ID ) as [ROW]
  FROM [dbo].[RPT_USER_ROLE] r
  )
  SELECT * FROM CTE





