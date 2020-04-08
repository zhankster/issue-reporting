DROP Table

USE [RXBackend]
GO

/****** Object:  Table [dbo].[DEPARTMENTS]    Script Date: 4/3/2020 8:08:45 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[RPT_ACTIVITY](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[CREATED] DATETIME,
	[ACTIVITY] [varchar](30) NOT NULL,
	[USER] int NOT NULL,
	[DESCRIPTION] [varchar](256) NULL,
 CONSTRAINT [PK_RPT_ACTIVITY] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

ALTER TABLE [dbo].[RPT_ACTIVITY] ADD  CONSTRAINT [DF_RPT_ACTIVITY_CREATED]  DEFAULT (getdate()) FOR [CREATED]
GO

select * from [dbo].[RPT_ACTIVITY] order by CREATED desc

update RPT_ACTIVITY set ALT_USER = '0' where ALT_USER = '' or ALT_USER is null
update RPT_OCCUR set RPH_VERIFY_DATE = null, TECH_VERIFY_DATE = null
select * from RPT_USERS

INSERT INTO [dbo].[RPT_ACTIVITY]
           ([CREATED]
           ,[ACTIVITY]
           ,[USER]
           ,[DESCRIPTION])
     VALUES
           (<CREATED, datetime,>
           ,<ACTIVITY, varchar(30),>
           ,<USER, int,>
           ,<DESCRIPTION, varchar(256),>)
GO

USE [RXBackend]
GO

/****** Object:  Table [dbo].[RPT_USERS]    Script Date: 4/3/2020 8:16:13 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[RPT_USERS](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[USERNAME] [varchar](50) NOT NULL,
	[FIRST_NAME] [varchar](20) NOT NULL,
	[LAST_NAME] [varchar](20) NOT NULL,
	[POSITION] [varchar](30) NOT NULL,
	[PASSWORD] [varchar](160) NOT NULL,
	[SALT] [varchar](50) NOT NULL,
	[CREATED_AT] [datetime] NULL,
	[CREATED_BY] [nchar](6) NULL,
	[UPDATED_AT] [datetime] NULL,
	[UPDATED_BY] [nchar](6) NULL,
	[ACTIVE] [bit] NOT NULL,
	[INITIALS] [nchar](6) NULL,
	[EMAIL] [varchar](128) NOT NULL,
 CONSTRAINT [PK_RPT_USER] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[INITIALS] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[RPT_USERS] ADD  CONSTRAINT [DF_RPT_USERS_CREATED_AT]  DEFAULT (getdate()) FOR [CREATED_AT]
GO

ALTER TABLE [dbo].[RPT_USERS] ADD  CONSTRAINT [DF_RPT_USERS_ACTIVE]  DEFAULT ((1)) FOR [ACTIVE]
GO

ALTER TABLE [dbo].[RPT_USERS] ADD  CONSTRAINT [DF_RPT_USERS_email]  DEFAULT ('') FOR [EMAIL]
GO



GO

USE [RXBackend]
GO

/****** Object:  Table [dbo].[RPT_OCCUR]    Script Date: 4/3/2020 8:09:50 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[RPT_OCCUR](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[USER_ID] [int] NOT NULL,
	[DISCOVER_DATE] [datetime] NOT NULL,
	[OCCUR_DATE] [datetime] NOT NULL,
	[USERNAME] [varchar](50) NOT NULL,
	[FACILITY_CODE] [nchar](6) NOT NULL,
	[PATIENT_NAME] [varchar](50) NULL,
	[PERSON_REPORTING] [varchar](50) NULL,
	[PHONE] [varchar](20) NULL,
	[PERSON_COMPLETING] [int] NULL,
	[ORDER_INTAKE] [int] NULL,
	[MEDICATION] [int] NULL,
	[SHIPPING] [int] NULL,
	[DELIVERY] [int] NULL,
	[BILLING] [int] NULL,
	[COOKING] [int] NULL,
	[OTHER] [int] NULL,
	[REASON_CODE] [int] NOT NULL,
	[TECH_ID] [int] NULL,
	[RPH_ID] [int] NULL,
	[EXPLANATION] [varchar](3000) NOT NULL,
	[VALID] [int] NOT NULL,
	[CREATED_AT] [datetime] NULL,
	[CREATED_BY] [nchar](6) NULL,
	[UPDATED_AT] [datetime] NULL,
	[UPDATED_BY] [nchar](6) NULL,
	[ATTACHMENT] [varchar](50) NULL,
	[TIMESTAMP] [varchar](50) NULL,
	[UPLOAD] [varchar](50) NULL,
	[TECH_REQ_VERIFY] [bit] NOT NULL,
	[RPH_REQ_VERIFY] [bit] NOT NULL,
	[TECH_VERIFY_DATE] [datetime] NULL,
	[RPH_VERIFY_DATE] [datetime] NULL,
 CONSTRAINT [PK_RPT_OCCUR] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[RPT_OCCUR] ADD  CONSTRAINT [DF_RPT_OCCUR_PERSON_COMPLETING]  DEFAULT ((0)) FOR [PERSON_COMPLETING]
GO

ALTER TABLE [dbo].[RPT_OCCUR] ADD  CONSTRAINT [DF_RPT_OCCUR_ORDER_INTAKE]  DEFAULT ((0)) FOR [ORDER_INTAKE]
GO

ALTER TABLE [dbo].[RPT_OCCUR] ADD  CONSTRAINT [DF_RPT_OCCUR_MEDICATION]  DEFAULT ((0)) FOR [MEDICATION]
GO

ALTER TABLE [dbo].[RPT_OCCUR] ADD  CONSTRAINT [DF_RPT_OCCUR_SHIPPING]  DEFAULT ((0)) FOR [SHIPPING]
GO

ALTER TABLE [dbo].[RPT_OCCUR] ADD  CONSTRAINT [DF_RPT_OCCUR_DELIVERY]  DEFAULT ((0)) FOR [DELIVERY]
GO

ALTER TABLE [dbo].[RPT_OCCUR] ADD  CONSTRAINT [DF_RPT_OCCUR_BILLING]  DEFAULT ((0)) FOR [BILLING]
GO

ALTER TABLE [dbo].[RPT_OCCUR] ADD  CONSTRAINT [DF_RPT_OCCUR_COOKING]  DEFAULT ((0)) FOR [COOKING]
GO

ALTER TABLE [dbo].[RPT_OCCUR] ADD  CONSTRAINT [DF_RPT_OCCUR_REASON_CODE]  DEFAULT ((0)) FOR [REASON_CODE]
GO

ALTER TABLE [dbo].[RPT_OCCUR] ADD  CONSTRAINT [DF_RPT_OCCUR_VALID]  DEFAULT ((1)) FOR [VALID]
GO

ALTER TABLE [dbo].[RPT_OCCUR] ADD  CONSTRAINT [DF_RPT_OCCUR_UPLOAD]  DEFAULT ('') FOR [UPLOAD]
GO

ALTER TABLE [dbo].[RPT_OCCUR] ADD  DEFAULT ((0)) FOR [TECH_REQ_VERIFY]
GO

ALTER TABLE [dbo].[RPT_OCCUR] ADD  DEFAULT ((0)) FOR [RPH_REQ_VERIFY]
GO



