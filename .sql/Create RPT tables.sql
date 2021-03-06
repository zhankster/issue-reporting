CREATE TABLE [dbo].[RPT_CATEGORIES](
	[CODE] [nchar](20) NOT NULL,
	[DESCRIPTION] [nchar](100) NOT NULL,
	[DEPT_CODE] [nchar](20) NOT NULL
) ON [PRIMARY]

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
	[PERSON_COMPLETING] [varchar](50) NULL,
	[ORDER_INTAKE] [int] NULL,
	[MEDICATION] [int] NULL,
	[SHIPPING] [int] NULL,
	[DELIVERY] [int] NULL,
	[BILLING] [int] NULL,
	[COOKING] [int] NULL,
	[OTHER] [int] NULL,
	[TECH_ID] [int] NULL,
	[RPH_ID] [int] NULL,
	[EXPLANATION] [varchar](3000) NOT NULL,
	[CREATED_AT] [datetime] NULL,
	[CREATED_BY] [nchar](6) NULL,
	[UPDATED_AT] [datetime] NULL,
	[UPDATED_BY] [nchar](6) NULL,
 CONSTRAINT [PK_RPT_OCCUR] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
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


CREATE TABLE [dbo].[RPT_REASONS](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[CATEGORY_CODE] [nvarchar](20) NOT NULL,
	[DESCRIPTION] [nvarchar](100) NOT NULL,
	[SORT_ORDER] [int] NULL,
	[CREATED_BY] [nchar](10) NOT NULL,
	[CREATED] [datetime] NOT NULL,
	[LAST_USER] [nchar](10) NULL,
	[LAST_UPDATE] [datetime] NULL,
	[ACTIVE] [bit] NOT NULL,
 CONSTRAINT [PK_RPT_REASONS_1] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[RPT_REASONS] ADD  CONSTRAINT [DF_RPT_REASONS_SORT_ORDER]  DEFAULT ((1)) FOR [SORT_ORDER]
GO

ALTER TABLE [dbo].[RPT_REASONS] ADD  CONSTRAINT [DF_RPT_REASONS_CREATED]  DEFAULT (getdate()) FOR [CREATED]
GO

ALTER TABLE [dbo].[RPT_REASONS] ADD  CONSTRAINT [DF_RPT_REASONS_ACTIVE]  DEFAULT ((1)) FOR [ACTIVE]
GO

CREATE TABLE [dbo].[RPT_ROLES](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[DESCRIPTION] [varchar](50) NOT NULL,
 CONSTRAINT [PK_RPT_ROLES] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[DESCRIPTION] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO


CREATE TABLE [dbo].[RPT_USER_ROLE](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[USER_ID] [int] NOT NULL,
	[ROLE_ID] [int] NOT NULL,
 CONSTRAINT [PK_RPT_USER_ROLE] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
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


CREATE PROC [dbo].[rpt_put_user]
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
GO

CREATE PROC [dbo].[rpt_update_user]
	 @USERNAME VARCHAR(50)
	,@FIRST_NAME VARCHAR(20)
	,@LAST_NAME VARCHAR(20)
	,@POSITION VARCHAR(30)
	,@PASSWORD VARCHAR(160)
	,@ROLE INT
	,@INITIALS nchar(6)
	,@ACTIVE BIT
	,@OP VARCHAR(50)
	,@USER_ID INT
as

BEGIN
UPDATE [dbo].[RPT_USERS]
    SET [USERNAME] = @USERNAME
        ,[FIRST_NAME] = @FIRST_NAME
        ,[LAST_NAME] = @LAST_NAME
        ,[POSITION] = @POSITION
        ,[PASSWORD] = @PASSWORD
        ,[UPDATED_AT] = GETDATE()
        ,[UPDATED_BY] = @OP
        ,[ACTIVE] = @ACTIVE
        ,[INITIALS] = @INITIALS
    WHERE ID = @USER_ID

	IF NOT EXISTS (SELECT USER_ID, ROLE_ID FROM dbo.RPT_USER_ROLE WHERE USER_ID = @USER_ID AND ROLE_ID = @ROLE )
	BEGIN
	DELETE FROM RPT_USER_ROLE WHERE USER_ID = @USER_ID

	INSERT INTO [dbo].[RPT_USER_ROLE]
			   ([USER_ID]
			   ,[ROLE_ID])
		 VALUES
			   (
			   @USER_ID
			   ,@ROLE
			   )
	END
END
GO
















