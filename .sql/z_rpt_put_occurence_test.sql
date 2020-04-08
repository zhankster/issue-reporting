--DECLARE 
--@CURR_DATE DATETIME
--,@tableHTML NVARCHAR(MAX)

--		SET @tableHTML =
--		<p>  @SUBJECT  </p><br /> 

--		<p>Completed by:   @SUBJECT  </p> 
--		<p>Date Reported:   CAST(@DISCOVER_DATE AS VARCHAR)  </p> 
--		<p>Patient involved:   @PATIENT_NAME  </p> 
--		<p>Date Reported:   CAST(@OCCUR_DATE AS VARCHAR)  </p> 
--		<p>Reported By:   @PERSON_REPORTING  </p><br /> 

--		<p><strong>Tech Invovled:   @TECH_NAME  </strong></p> 
--		<p><strong>RPH Invovled:   @RPH_NAME  </strong></p><br /> 

--		<p>  @EXPLANATION  </p><br /><br /> 

--		<p>
--		CONFIDENTIALITY NOTICE: This email message, including any attachments, is for the sole use of the intended recipient(s) and may contain confidential and privileged 
--		information or otherwise be protected by law. Any unauthorized review, use, disclosure or distribution is prohibited. if you are not the intended recipient, please contact the 
--		sender by reply email and destroy all copies of the original message.
--		</p>'

	 --print(rounddatetime.datetime.utcnow().timestamp()),2))
	 -- print(round(datetime.datetime.utcnow().timestamp(),3))
TRUNCATE TABLE RPT_USER_ROLE
	TRUNCATE TABLE RPT_USERS


	UPDATE dbo.RPT_OCCUR SET UPLOAD = '' where upload = '150'
	UPDATE dbo.RPT_USERS SET EMAIL= '' --where upload = '150'
	SELECT * FROM RPT_USER_ROLE
	SELECT * FROM RPT_USERS 
	SELECT * FROM RPT_OCCUR order by CREATED_AT desc
	SELECT * FROM CIPS.dbo.FAC

	SELECT CREATED_AT,ATTACHMENT, UPLOAD,TECH_REQ_VERIFY, TECH_VERIFY_DATE, RPH_REQ_VERIFY,RPH_VERIFY_DATE,
	TECH_ID,RPH_ID, * FROM RPT_OCCUR  --where id in (1216,1212)
	order by RPT_OCCUR.CREATED_AT desc

	SELECT CREATED_AT,TECH_REQ_VERIFY, TECH_VERIFY_DATE,TECH_WITNESS, RPH_REQ_VERIFY,RPH_VERIFY_DATE,RPH_WITNESS,
	TECH_ID,RPH_ID, * FROM RPT_OCCUR  where  RPH_VERIFY_DATE is not null or TECH_VERIFY_DATE is not null
	order by RPT_OCCUR.CREATED_AT desc

	select * from RPT_ACTIVITY order by created desc

	select CONVERT(VARCHAR(10), CAST(GETDATE() AS DATE), 101)
	select * from _TEST order  by UPDATED desc

	exec rpt_put_occurence
		 @USER_ID = 4
		,@DISCOVER_DATE = '2020-03-03'
		,@OCCUR_DATE = '2020-03-01'
		,@USERNAME = 4
		,@FACILITY_CODE = 'DJ'--AL' --'DJ'
		,@PATIENT_NAME = 'Slim Shady'
		,@PERSON_REPORTING = 'Bob Woodward'
		,@PHONE = '888-888-8888'
		,@PERSON_COMPLETING = 4
		,@TECH_ID = 5
		,@RPH_ID = 6
		,@REASON_CODE = 5
		,@EXPLANATION = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor 
		incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation 
		ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in 
		voluptate'
		,@CREATED_BY = 'jparker'
		,@PDF_RPT = '111851434343.pdf';

		127.0.0.1:5000/static/pdf/111851434343.pdf

		2
	

ALTER TABLE RPT_OCCUR
ADD ATTACHMENT VARCHAR(50) NULL;

ALTER TABLE RPT_USERS
ADD EMAIL VARCHAR(128) NULL;
UPDATE dbo.RPT_USERS SET EMAIL= ''

ALTER TABLE RPT_OCCUR
ADD UPLOAD VARCHAR(50) NULL;

ALTER TABLE RPT_OCCUR
ADD TECH_REQ_VERIFY BIT NOT NULL DEFAULT(0);

ALTER TABLE RPT_OCCUR
ADD RPH_REQ_VERIFY BIT NOT NULL DEFAULT(0);

ALTER TABLE RPT_OCCUR
ADD TECH_VERIFY_DATE DATETIME NULL;

ALTER TABLE RPT_OCCUR
ADD WHOLESALE DATETIME NULL;

ALTER TABLE RPT_OCCUR
ADD WHOLESALE INT NULL DEFAULT(0);

ALTER TABLE RPT_ACTIVITY
ADD ITEM VARCHAR(30) NULL;

ALTER TABLE RPT_ACTIVITY
ADD ALT_USER  NULL DEFAULT(0);

ALTER TABLE RPT_ACTIVITY
ADD ALT_ID INT NULL DEFAULT(0);

ALTER TABLE RPT_OCCUR
ADD TECH_WITNESS INT NULL DEFAULT(0);

ALTER TABLE RPT_OCCUR
ADD RPH_WITNESS INT NULL DEFAULT(0);




USE CIPS
CREATE TABLE [dbo].[PGR](
	[ID] [int] NOT NULL,
	[DCODE] [varchar](10) NOT NULL,
	[DTEXT] [varchar](60) NULL,
	[PRC_ID] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

ID	DCODE	DTEXT	PRC_ID
215	HOME1	ASSISTED LIVING 150+2.5 BRK	1
309	ADV CARD	CARDS ACQ +20 +2.48 (12-1-16)	1

CREATE VIEW PGR
AS
SELECT
ID 
,CASE 
WHEN DCODE LIKE '%ACHIN%' THEN 'ACH'
WHEN DCODE LIKE '%ADV AUTO%'	THEN 'ACH'
WHEN DCODE LIKE '%ADV CARD%'	THEN 'ACH'
WHEN DCODE LIKE '%CORRCARE%'	THEN 'CORRCARE'
WHEN DCODE LIKE '%H&O1%'	THEN 'HALEY & OLSEN'
WHEN DCODE LIKE '%JOB CORP%'	THEN 'JOB CORP'
WHEN DCODE LIKE '%LA WORKFOR%'	THEN 'LA WORKFORCE'
WHEN DCODE LIKE '%LASNEW%'	THEN 'LASALLE'
WHEN DCODE LIKE '%QCHC NEW%'	THEN 'QCHC'
WHEN DCODE LIKE '%QCHCPASS%'	THEN 'QCHC'
WHEN DCODE LIKE '%SCM%'	THEN 'SCM'
WHEN DCODE LIKE '%SCMFL%'	THEN 'SCM'
WHEN DCODE LIKE '%SHPLOW%'	THEN 'SHP'
WHEN DCODE LIKE '%SHPM%'	THEN 'SHP'
WHEN DCODE LIKE '%TURNKEY%'	THEN 'TURNKEY'
WHEN DCODE LIKE '%VITALCORE%'	THEN 'VITALCORE'
ELSE ''
END AS SHORT_NAME
,DCODE
,DTEXT
,PRC_ID
FROM CIPS.dbo.PGR

SELECT @FAC_NAME = DNAME FROM CIPS.dbo.FAC f
	LEFT JOIN PGR p ON f.PGR_ID = ID
WHERE DCODE = @FACILITY_CODE;

SELECT * FROM CIPS.dbo.FAC f
	LEFT JOIN PGR p ON f.PGR_ID = p.ID

	SELECT * FROM CIPS.dbo.FAC f
	LEFT JOIN PGR p ON f.PGR_ID = p.ID
WHERE f.DCODE = 'DJ'
