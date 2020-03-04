/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [DISCOVERED_DATE]
      ,[OCCURENCE_DATE]
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
      ,[EXPLANATION]
  FROM [RXBackend].[dbo].[Occurence]

  select * from RPT_CATEGORIES 
BILL                	Billing                                                                                             	ALL                 
COOK                	Cooking                                                                                             	ALL                 
DEL                 	Delivery                                                                                            	ALL                 
MED                 	Medication                                                                                          	ALL                 
ORDIN               	Order Entry                                                                                         	ALL                 
SHIP                	Shipping                                                                                            	ALL                 
OU                  	Other\Uncategorized   

select * from RPT_REASONS
where CATEGORY_CODE = 'ORDIN'
order by CATEGORY_CODE, SORT_ORDER

  select max(len(explanation)) FROM [RXBackend].[dbo].[Occurence]
  select * FROM [RXBackend].[dbo].[Occurence] WHERE [ORDER_INTAKE_T] IS NOT NULL

  UPDATE Occurence set
       [ORDER_INTAKE] = 0
      ,[MEDICATION] = 0 
      ,[SHIPPING] = 0
      ,[DELIVERY] = 0
      ,BILLING = 0
      ,[COOKING] = 0

	SELECT DISTINCT [ORDER_INTAKE_T] FROM Occurence WHERE upper(ORDER_INTAKE_T) LIke '%ORDER%'
	OR upper(ORDER_INTAKE_T) LIke '%ACTIVE%'
	OR upper(ORDER_INTAKE_T) LIke '%ARX%'
	SELECT DISTINCT [MEDICATION_T] FROM Occurence 
	--where [MEDICATION_T] is not null
	where UPPER([MEDICATION_T]) LIke '%FOR%'
	SELECT DISTINCT [SHIPPING_T] FROM Occurence 
	where upper(SHIPPING_T) LIke '%D%' and upper(SHIPPING_T) LIke '%WRONG%'
	--where [SHIPPING_T] is not null
	SELECT DISTINCT [DELIVERY_T] FROM Occurence where [DELIVERY_T] is not null
	SELECT DISTINCT [BILLNG_T] FROM Occurence where [BILLNG_T] is not null
	SELECT DISTINCT [COOKING_T] FROM Occurence where [COOKING_T] is not null

UPDATE Occurence 
	SET COOKING = CASE 
		WHEN COOKING_T IN ('Each dose not cooked on separte card') --Each dose not cooked on separte card
			THEN 19
		WHEN COOKING_T IN ('Label does not match drug') --Label does not match drug
			THEN 2
		WHEN COOKING_T IN ('Wrong Qty') --Wrong Qty
			THEN 8
		ELSE
			0
		END

SELECT DISTINCT [COOKING_T],
	CASE 
		WHEN COOKING_T IN ('Each dose not cooked on separte card') --Each dose not cooked on separte card
			THEN 'Each dose not cooked on separte card'--19
		WHEN COOKING_T IN ('Label does not match drug') --Label does not match drug
			THEN 'Label does not match drug'--2
		WHEN COOKING_T IN ('Wrong Qty') --Wrong Qty
			THEN 'Wrong Qty'--8
		ELSE
			'_N/A'
		END
		AS Reason
		FROM Occurence
		WHERE [COOKING_T] IS NOT NULL
		ORDER BY Reason

	UPDATE Occurence 
	SET BILLING = CASE 
		WHEN BILLNG_T IN ('Other')
			THEN 999999
		ELSE
			0
		END

	UPDATE Occurence 
	SET DELIVERY = CASE 
		WHEN DELIVERY_T IN ('Late delivery') --Late delivery
			THEN 3
		WHEN DELIVERY_T IN ('Wrong address') --Wrong address
			THEN 9
		ELSE
			0
		END

		UPDATE Occurence 
	SET SHIPPING = CASE 
		WHEN SHIPPING_T IN ('CORRECT NAME WRONG ADDRESS', 'Wrong Address') --Wrong Address
			THEN 6
		WHEN SHIPPING_T IN ('Wrong label on med box', 'Wrong NAME label on med box') --Wrong label on med box
			THEN 12
		WHEN SHIPPING_T IN ('Delivery sheet omitted') --Delivery sheet omitted
			THEN 25
		WHEN SHIPPING_T IN ('Meds NOT SHIPPED FOR SAT DELIVERY', 'Wrong DELIVERY TYPE(GRD VS AIR)') --Delivery sheet incorrect
			THEN 28
		WHEN SHIPPING_T IN ('MARS SENT TO WRONG FACILITY') --MAR not sent
			THEN 30
		WHEN SHIPPING_T IN ('Wrong MAR sent') --Wrong MAR sent
			THEN 32
		ELSE
			0
		END


		SELECT DISTINCT [SHIPPING_T],
		CASE
		WHEN SHIPPING_T IN ('CORRECT NAME WRONG ADDRESS', 'Wrong Address') --Wrong Address
			THEN 'Wrong Address' --6
		WHEN SHIPPING_T IN ('Wrong label on med box', 'Wrong NAME label on med box') --Wrong label on med box
			THEN 'Wrong label on med box'--12
		WHEN SHIPPING_T IN ('Delivery sheet omitted') --Delivery sheet omitted
			THEN 'Delivery sheet omitted'--25
		WHEN SHIPPING_T IN ('Meds NOT SHIPPED FOR SAT DELIVERY', 'Wrong DELIVERY TYPE(GRD VS AIR)') --Delivery sheet incorrect
			THEN 'Delivery sheet incorrect'--28
		WHEN SHIPPING_T IN ('MARS SENT TO WRONG FACILITY') --MAR not sent
			THEN 'MAR not sent'--30
		WHEN SHIPPING_T IN ('Wrong MAR sent') --Wrong MAR sent
			THEN 'Wrong MAR sent'--32
		ELSE
			'_N/A'
		END
		AS Reason
		FROM Occurence
		WHERE [SHIPPING_T] IS NOT NULL
		ORDER BY Reason


	--Out of meds
	UPDATE Occurence 
	SET MEDICATION = CASE 
		WHEN MEDICATION_T IN ('Out of meds') --Out of Meds
			THEN 4
		WHEN MEDICATION_T IN ('Too few meds','Too few meds(AUTOMED)','Too few meds--automed tech') --Too few meds
			THEN 10
		WHEN MEDICATION_T IN ('Expired Meds') --Expired Meds
			THEN 16
		WHEN MEDICATION_T IN ('Dosing schedule wrong','Wrong DOSING SCHEDULE') --Dosing schedule wrong
			THEN 21
		WHEN MEDICATION_T IN ('Wrong med','Wrong med--TRAY ERROR') --Wrong med
			THEN 24
		WHEN MEDICATION_T IN ('Wrong med strength') --Wrong med strength
			THEN 27
		WHEN MEDICATION_T IN ('Wrong script label') --Wrong script
			THEN 29
		WHEN MEDICATION_T IN ('Wrong start date','Wrong start date, Wrong start date') --Wrong start date
			THEN 31
		WHEN MEDICATION_T IN ('Formulary not followed') --Formulary not followed
			THEN 33
		ELSE
			0
		END

		SELECT DISTINCT [MEDICATION_T],
		CASE 
		WHEN MEDICATION_T IN ('Out of meds') --Out of Meds
			THEN 'Out of Meds'--4
		WHEN MEDICATION_T IN ('Too few meds','Too few meds(AUTOMED)','Too few meds--automed tech') --Too few meds
			THEN 'Too few meds'--10
		WHEN MEDICATION_T IN ('Expired Meds') --Expired Meds
			THEN 'Expired Meds'--16
		WHEN MEDICATION_T IN ('Dosing schedule wrong','Wrong DOSING SCHEDULE') --Dosing schedule wrong
			THEN 'Dosing schedule wrong'--21
		WHEN MEDICATION_T IN ('Wrong med','Wrong med--TRAY ERROR') --Wrong med
			THEN 'Wrong med'--24
		WHEN MEDICATION_T IN ('Wrong med strength') --Wrong med strength
			THEN 'Wrong med strength'--27
		WHEN MEDICATION_T IN ('Wrong script label') --Wrong script
			THEN 'Wrong script' --29
		WHEN MEDICATION_T IN ('Wrong start date','Wrong start date, Wrong start date') --Wrong start date
			THEN 'Wrong start date' --31
		WHEN MEDICATION_T IN ('Formulary not followed') --Formulary not followed
			THEN 'Formulary not followed' --33
		ELSE
			'_N/A'
		END
		AS Reason
		FROM Occurence
		WHERE [MEDICATION_T] IS NOT NULL
		ORDER BY Reason


	UPDATE Occurence 
	SET ORDER_INTAKE = CASE 
		WHEN ORDER_INTAKE_T IN ('no MAR', 'NO MARS', 'MONTHLY MARS NOT RECD','MARS NOT RECEIVED',
			'MAR info incorrect', 'BAD MARS','WRONG MARS') --Mar info incorrect
			THEN 5
		WHEN ORDER_INTAKE_T IN ('Active Rx not COMPLETED','ARX NOT COMPLETED IN TIME', 'ARX NOT FOLLOWED UP',
			'ARX RELEASES NOT PULLED', 'NOT RELEASED WITH ARX') --Active Rx info sent/received
			THEN 11
		WHEN ORDER_INTAKE_T IN ('FILLED UNDER WRONG INMATE/ORDERS NOT REC','Order TYPED UNDER WRONG INMATE',
			'Order was not entered correctly','Orders FILLED UNDER WRONG FACILITY','Orders not recvd/entered',
			'WRONG DOCTOR ON ORDER') --Orders not received/entered
			THEN 17
		ELSE
			0
		END

		SELECT DISTINCT [ORDER_INTAKE_T],
		CASE 
		WHEN ORDER_INTAKE_T IN ('no MAR', 'NO MARS', 'MONTHLY MARS NOT RECD','MARS NOT RECEIVED',
			'MAR info incorrect', 'BAD MARS','WRONG MARS') --Mar info incorrect
			THEN 'Mar info incorrect' --5
		WHEN ORDER_INTAKE_T IN ('Active Rx not COMPLETED','ARX NOT COMPLETED IN TIME', 'ARX NOT FOLLOWED UP',
			'ARX RELEASES NOT PULLED', 'NOT RELEASED WITH ARX') --Active Rx info sent/received
			THEN 'Active Rx info sent/received' --11
		WHEN ORDER_INTAKE_T IN ('FILLED UNDER WRONG INMATE/ORDERS NOT REC','Order TYPED UNDER WRONG INMATE',
			'Order was not entered correctly','Orders FILLED UNDER WRONG FACILITY','Orders not recvd/entered',
			'WRONG DOCTOR ON ORDER') --Orders not received/entered
			THEN 'Orders not received/entered' --17
		ELSE
			'_N/A'
		END
		AS Reason
		FROM Occurence
		WHERE [ORDER_INTAKE_T] IS NOT NULL
		ORDER BY Reason

		SELECT * FROM Occurence 
		
		UPDATE Occurence SET ORDER_INTAKE_T = NULL
		WHERE upper(ORDER_INTAKE_T) LIke '%*%'