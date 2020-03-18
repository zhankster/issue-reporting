BEGIN TRAN

DROP TABLE HourlyTechCount

SELECT TECH, FNAME, LNAME, NEW, REFILLS, PROFILES, NEW_WHOLESALE
INTO HourlyTechCount
FROM (
SELECT 
	COUNT(FIL.ID) as FILL_COUNT
	,FIL.TECH
	,USR.FNAME
	,USR.LNAME
	,'NEW' as [TYPE]
--	,FIL.SYS_TIME_HOUR
--	,FIL.*
FROM FIL
JOIN USR
	ON FIL.TECH_USR_ID = USR.ID
WHERE CAST(FIL_DATE as date) = CAST(GETDATE() as date) 
	AND FIL.SYS_TIME_HOUR < DATEPART(hour, GETDATE())
	--AND FIL.TECH = 'JLG'
	AND (FIL.SEQ_NUM = 0 AND FIL.[STATUS] <> 'V' AND FIL.QTY_DSP <> 0)
GROUP BY 
	FIL.TECH
	,FIL.TECH_USR_ID
	,USR.LNAME
	,USR.FNAME
--	,FIL.SYS_TIME_HOUR

UNION ALL
SELECT 
	COUNT(FIL.ID) as FILL_COUNT
	,FIL.TECH
	,USR.FNAME
	,USR.LNAME
	,'REFILLS'
--	,FIL.SYS_TIME_HOUR
--	,FIL.*
--INTO HourlyTechCount
FROM FIL
JOIN USR
	ON FIL.TECH_USR_ID = USR.ID
WHERE CAST(FIL_DATE as date) = CAST(GETDATE() as date) 
	AND FIL.SYS_TIME_HOUR < DATEPART(hour, GETDATE())
	--AND FIL.TECH = 'JLG'
	AND (FIL.SEQ_NUM <> 0 and FIL.KOP <> 'P' and FIL.[STATUS] <> 'V')
GROUP BY 
	FIL.TECH
	,FIL.TECH_USR_ID
	,USR.LNAME
	,USR.FNAME
--	,FIL.SYS_TIME_HOUR
UNION ALL
SELECT 
	COUNT(FIL.ID) as FILL_COUNT
	,FIL.TECH
	,USR.FNAME
	,USR.LNAME
	,'PROFILES'
--	,FIL.SYS_TIME_HOUR
--	,FIL.*
FROM FIL
JOIN USR
	ON FIL.TECH_USR_ID = USR.ID
WHERE CAST(FIL_DATE as date) = CAST(GETDATE() as date) 
	AND FIL.SYS_TIME_HOUR < DATEPART(hour, GETDATE())
	--AND FIL.TECH = 'JLG'
	AND (FIL.SEQ_NUM = 0 and FIL.NET_QTY_DSP = 0 and FIL.[STATUS] <> 'V')
GROUP BY 
	FIL.TECH
	,FIL.TECH_USR_ID
	,USR.LNAME
	,USR.FNAME
--	,FIL.SYS_TIME_HOUR
UNION ALL 
SELECT 
	COUNT(FIL.ID) as FILL_COUNT
	,FIL.TECH
	,USR.FNAME
	,USR.LNAME
	,'NEW_WHOLESALE' as [TYPE]
--	,FIL.SYS_TIME_HOUR
--	,FIL.*
FROM CIPS_WHOLESALE.dbo.FIL FIL
JOIN CIPS_WHOLESALE.dbo.USR USR
	ON FIL.TECH_USR_ID = USR.ID
WHERE CAST(FIL_DATE as date) = CAST(GETDATE() as date) 
	AND FIL.SYS_TIME_HOUR < DATEPART(hour, GETDATE())
	--AND FIL.TECH = 'JLG'
	AND (FIL.SEQ_NUM = 0 AND FIL.[STATUS] <> 'V' AND FIL.QTY_DSP <> 0)
GROUP BY 
	FIL.TECH
	,FIL.TECH_USR_ID
	,USR.LNAME
	,USR.FNAME
) AS SRC
PIVOT
(
SUM(FILL_COUNT)
FOR [TYPE] IN (NEW, REFILLS, PROFILES, NEW_WHOLESALE)
) PVT
ORDER BY TECH

COMMIT TRAN
--SELECT FIL.ID, COUNT(SEQ_NUM) FROM FIL WHERE CAST(FIL_DATE as date) > CAST(GETDATE()-365 as date) GROUP BY FIL.ID HAVING COUNT(SEQ_NUM) > 1

--Add email
IF EXISTS (
SELECT 
	1
FROM HourlyTechCount
		)
	
BEGIN

	DECLARE @tableHTML  NVARCHAR(MAX) ;

	SET @tableHTML =
		N'<H1>HourlyTechCount</H1>' +
		N'<table border="1">' +
		N'<tr>' +
	--Insert Code from Excel
    N'<th>TECH</th>' +
    N'<th>FNAME</th>' +
    N'<th>LNAME</th>' +
	N'<th>NEW</th>' +
	N'<th>REFILLS</th>' +
	N'<th>PROFILES</th>' +
	N'<th>NEW_WHOLESALE</th>' +
   	--End top portion from Excel
		N'</tr>' +
	--Next Excel
    CAST ( ( SELECT td = iif(TECH is null,' ', TECH),       '',
					td = iif(FNAME is null,' ', FNAME),       '',
                    td = iif(LNAME is null,' ', LNAME),       '',
					td = iif(NEW is null,0, NEW),       '',
					td = iif(REFILLS is null,0, REFILLS),       '',
					td = iif(PROFILES is null,0, PROFILES),       '',
					td = iif(NEW_WHOLESALE is null,0, NEW_WHOLESALE),       ''
					FROM HourlyTechCount
					ORDER BY TECH
	--Finish Code from Excel
				  FOR XML PATH('tr'), TYPE 
		) AS NVARCHAR(MAX) ) +
		N'<tr>' +
			N'<td colspan="2">' + (SELECT CONVERT(nvarchar,GETDATE(),100)) + N'</td>' +
			N'<td><b>TOTALS:</b></td>' +
			N'<td>' + (SELECT ISNULL(CAST(SUM(NEW) as char),0) FROM HourlyTechCount) + N'</td>' +
			N'<td>' + (SELECT ISNULL(CAST(SUM(REFILLS) as char),0) FROM HourlyTechCount) + N'</td>' +
			N'<td>' + (SELECT ISNULL(CAST(SUM(PROFILES) as char),0) FROM HourlyTechCount) + N'</td>' +
			N'<td>' + (SELECT ISNULL(CAST(SUM(NEW_WHOLESALE) as char),0) FROM HourlyTechCount) + N'</td>' +
		N'</tr>' +
		N'</table>' ;


	EXEC msdb.dbo.sp_send_dbmail
		@profile_name = 'IHS Email',
		@recipients='danac@ihspharmacy.com;roys@ihspharmacy.com;cristiel@ihspharmacy.com;gails@ihspharmacy.com;bryant@ihspharmacy.com;mirandac@ihspharmacy.com;justing@ihspharmacy.com;cortneyb@ihspharmacy.com;sydneyk@ihspharmacy.com',
		@subject = 'HourlyTechCount',
		@body = @tableHTML,
		@body_format = 'HTML' ;

END


