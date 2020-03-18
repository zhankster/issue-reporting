USE [RXBackend]
GO

/****** Object:  Table [dbo].[RPT_ROLES]    Script Date: 3/5/2020 3:45:08 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[RPT_GROUPS](
	[TARGET] [varchar](30) NOT NULL,
	[USAGE] [varchar](30) NOT NULL,
	[RECIPIENTS] [varchar] (4000) NULL,
	[SENDER] [varchar] (256) NULL,
	[CONTENT] [varchar] (4000) NULL,
	[SUBJECT] [varchar] (256) NULL,
	[HEADER] [varchar] (4000) NULL,
	[FOOTER] [varchar] (4000) NULL
)

UPDATE [dbo].[RPT_GROUPS]
   SET [RECIPIENTS] = ''
 WHERE [TARGET] = ? AND [USAGE] = ?

 SELECT * from [RPT_GROUPS]