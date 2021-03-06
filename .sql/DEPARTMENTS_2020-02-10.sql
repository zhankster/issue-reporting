USE [RXBackend]
GO

/****** Object:  Table [dbo].[DEPARTMENTS]    Script Date: 2/10/2020 12:43:59 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[DEPARTMENTS](
	[CODE] [nchar](20) NOT NULL,
	[DESCRIPTION] [nchar](30) NOT NULL,
 CONSTRAINT [PK_DEPARTMENTS] PRIMARY KEY CLUSTERED 
(
	[CODE] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

USE [RXBackend]
GO

INSERT INTO [dbo].[DEPARTMENTS]([CODE] ,[DESCRIPTION])
VALUES('RX','Pharmacy')

INSERT INTO [dbo].[DEPARTMENTS]([CODE] ,[DESCRIPTION])
VALUES('TECH','Pharmacy Tech')

INSERT INTO [dbo].[DEPARTMENTS]([CODE] ,[DESCRIPTION])
VALUES('SHIP','Shipping')

INSERT INTO [dbo].[DEPARTMENTS]([CODE] ,[DESCRIPTION])
VALUES('ACCT','Accounting')

INSERT INTO [dbo].[DEPARTMENTS]([CODE] ,[DESCRIPTION])
VALUES('ALL','All')

SELECT * FROM DEPARTMENTS






