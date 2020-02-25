USE [CIPS]
GO

INSERT INTO [dbo].[_FAC]
           ([ID]
           ,[DCODE]
           ,[DNAME])
     VALUES
           (3
           ,'MCJ'
           ,'Madison County Jail')


select * from [dbo].[_FAC]
--DROP TABLE [dbo].[_FAC]

USE [CIPS]
GO

SELECT [ID]
      ,[DCODE]
      ,[DNAME]
  FROM [dbo].[_FAC]
GO



CREATE TABLE [dbo].[_FAC](
	[ID] [int] NOT NULL,
	[DCODE] [varchar](8) NOT NULL,
	[DNAME] [varchar](30) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO




USE [CIPS]
GO

INSERT INTO [dbo].[FAC]
           ([ID]
           ,[DCODE]
           ,[DNAME]
		   ,FORCE_CHG_ID_FLAG
		   ,PHR_ID
		   ,ST
		   ,KOP_PRIMARY
		   ,KOP_SECONDARY
		   ,LOCATION_TYPE
		   ,FILLING_TYPE
		   ,NF_DISPENSE_FLAG
		   ,POPULATION_TYPE
		   ,REFILL_DUE_FLAG
		   ,RFD_TYPE
		)
     VALUES
           (1
           ,'ABL'
           ,'Acme Labs'
		   ,'F'
		   ,1
		   ,'S'
		   ,1
		   ,1
		   ,'L'
		   ,'L'
		   ,'F'
		   ,'P'
		   ,'F'
		   ,'R'
)
GO


