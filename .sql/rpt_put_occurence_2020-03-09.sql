USE [RXBackend]
GO
/****** Object:  StoredProcedure [dbo].[rpt_put_occurence]    Script Date: 3/9/2020 12:24:57 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[rpt_put_occurence]
		@USER_ID INT
		,@DISCOVER_DATE DATETIME
		,@OCCUR_DATE DATETIME
		,@USERNAME NCHAR(6)
		,@FACILITY_CODE VARCHAR(50)
		,@PATIENT_NAME VARCHAR(50)
		,@PERSON_REPORTING VARCHAR(50)
		,@PHONE VARCHAR(20)
		,@PERSON_COMPLETING INT
		,@TECH_ID INT
		,@RPH_ID INT
		,@REASON_CODE INT
		,@EXPLANATION VARCHAR(3000)
		,@CREATED_BY NCHAR(6)
		,@PDF_RPT VARCHAR(20)
AS
BEGIN

DECLARE 
@CURR_DATE DATETIME
,@tableHTML NVARCHAR(MAX)
,@RECIPIENTS VARCHAR(4000)
,@SUBJECT VARCHAR(256)
,@FAC_NAME VARCHAR(256)
,@PER_COMP VARCHAR(50)
,@TECH_NAME VARCHAR(50)
,@RPH_NAME VARCHAR(50)
,@URL VARCHAR(128)
,@MMG_NAME VARCHAR(50);

SET @URL = 'http://127.0.0.1:5000/static/pdf/' + @PDF_RPT;

SELECT @CURR_DATE = GETDATE();
SELECT @RECIPIENTS = RECIPIENTS FROM RPT_GROUPS WHERE [TARGET] = 'occurrence' AND USAGE = 'email';

SELECT @FAC_NAME = DNAME, @MMG_NAME = SHORT_NAME FROM CIPS.dbo.FAC f
	LEFT JOIN PGR p ON f.PGR_ID = p.ID
WHERE f.DCODE = @FACILITY_CODE;

SELECT @PER_COMP = FIRST_NAME + ' ' + LAST_NAME FROM RPT_USERS WHERE ID = @PERSON_COMPLETING;
SELECT @TECH_NAME = FIRST_NAME + ' ' + LAST_NAME FROM RPT_USERS WHERE ID = @TECH_ID;
SELECT @RPH_NAME = FIRST_NAME + ' ' + LAST_NAME FROM RPT_USERS WHERE ID = @RPH_ID;
SET @SUBJECT = 'Occurence Report Summary for: ' + @FACILITY_CODE + '-' + @FAC_NAME;

INSERT INTO [dbo].[RPT_OCCUR]
        ([USER_ID]
        ,[DISCOVER_DATE]
        ,[OCCUR_DATE]
        ,[USERNAME]
        ,[FACILITY_CODE]
        ,[PATIENT_NAME]
        ,[PERSON_REPORTING]
        ,[PHONE]
		,[PERSON_COMPLETING]
        ,[TECH_ID]
        ,[RPH_ID]
        ,[REASON_CODE]
        ,[EXPLANATION]
        ,[CREATED_AT]
        ,[CREATED_BY])
        VALUES
        (
		 @USER_ID
		,@DISCOVER_DATE
		,@OCCUR_DATE
		,@USERNAME
		,@FACILITY_CODE
		,@PATIENT_NAME
		,@PERSON_REPORTING
		,@PHONE
		,@PERSON_COMPLETING
		,@TECH_ID
		,@RPH_ID
		,@REASON_CODE
		,@EXPLANATION
		,@CURR_DATE
		,@CREATED_BY 
		)

		SET @tableHTML =
		--Medical Management Group
		N'<p>' + @SUBJECT + '</p>' + CHAR(10) + 
		N'<p>Medical Management Group: ' + ISNULL(@MMG_NAME, '') + '</p><br />' + CHAR(10) +
		N'<p>Completed by: ' + ISNULL(@PER_COMP, '') + '</p>' + CHAR(10) +
		N'<p>Date Reported: ' + CONVERT(VARCHAR(10), CAST(@DISCOVER_DATE AS DATE), 101) + '</p>' + CHAR(10) +
		N'<p>Patient involved: ' + ISNULL(@PATIENT_NAME, ' ') + '</p>' + CHAR(10) +
		N'<p>Date Reported: ' + CONVERT(VARCHAR(10), CAST(@OCCUR_DATE AS DATE), 101) + '</p>' + CHAR(10) +
		N'<p>Reported By: ' + ISNULL(@PERSON_REPORTING, ' ') + '</p><br />' + CHAR(10) +
		N'<p><strong>Tech Invovled: ' + ISNULL(@TECH_NAME, ' ') + '</strong></p>' + CHAR(10) +
		N'<p><strong>RPH Invovled: ' + ISNULL(@RPH_NAME, ' ') + '</strong></p>' +CHAR(10) +
		N'<p>' + @EXPLANATION + '</p><br />' + CHAR(10) +
		N'<p><a href="' + @URL + '">Complete Report<a></p><br />' +CHAR(10) +
		N'<p>
		CONFIDENTIALITY NOTICE: This email message, including any attachments, is for the sole use of the intended recipient(s) and may contain confidential and privileged 
		information or otherwise be protected by law. Any unauthorized review, use, disclosure or distribution is prohibited. if you are not the intended recipient, please contact the 
		sender by reply email and destroy all copies of the original message.
		</p>';
		--INSERT INTO _TEST(HTML) VALUES (@tableHTML)

		EXEC msdb.dbo.sp_send_dbmail
		@profile_name = 'IHS Email',
		@recipients = @RECIPIENTS,
		@subject = @SUBJECT,
		@body = @tableHTML,
		@body_format = 'HTML' ;

		print @tableHTML;

END