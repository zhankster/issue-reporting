-- show advanced options
EXEC sp_configure 'show advanced options', 1
GO
RECONFIGURE
GO
 
-- enable Database Mail XPs
EXEC sp_configure 'Database Mail XPs', 1
GO
RECONFIGURE
GO
 
-- check if it has been changed
EXEC sp_configure 'Database Mail XPs'
GO
 
-- hide advanced options
EXEC sp_configure 'show advanced options', 0
GO
RECONFIGURE
GO

Execute sysmail_add_profile_sp 
@profile_name =  'BH Mail'  
    , @description =  'Local email DB'


	
Execute sysmail_add_account_sp   
@account_name =   'BH Mail',  
@email_address =  'hank.d.allen@gmail.com' ,  
    @display_name =  'DB Mail' ,    
    @replyto_address =  'hank.d.allen@gmail.com' ,    
    @description =  'DB Email' ,    
@mailserver_name =  'smtp.gmail.com',   
@mailserver_type =  'SMTP',   
@port =  587,    
@username =  'hank.d.allen@gmail.com',    
@password =  'smzbh4791',       
@enable_ssl =   1


Execute sysmail_add_profileaccount_sp  
@profile_name =  'BH Mail'  ,  
@account_name =  'BH Mail'  ,
@sequence_number =  0


execute msdb.dbo.sp_send_dbmail 
    @profile_name =   'BH Mail'    
  ,   	@recipients =   'zrefugee@gmail.com'        
  ,   	@from_address =   'hank.d.allen@gmail.com'    
  ,   	@reply_to =   'hank.d.allen@gmail.com'     
  ,   	@subject =   'Express Test'
  ,   	@body =   '<h1>Express Test</h1><h3>It Works</h2>'  
  ,   	@body_format =   'HTML'    


execute sp_send_dbmail 
    @profile_name =   'BH Mail'    
  ,   	@recipients =   'zrefugee@gmail.com'    
  ,   	@copy_recipients =   'copy recipient;'    
  ,   	@blind_copy_recipients =   'blind copy recipient;'    
  ,   	@from_address =   'from address'    
  ,   	@reply_to =   'reply to'     
  ,   	@subject =   'subject'     
  ,   	@body =   'body'     
  ,   	@body_format =   'body format'    
  ,   	@importance =   'importance'    
  ,   	@sensitivity =   'sensitivity'    
  ,   	@file_attachments =   'attachment;'

  EXEC msdb.dbo.sp_addrolemember @rolename = 'DatabaseMailUserRole', @membername = 'IIS APPPOOL\RxApps'
  DatabaseMailUserRole', @membername = 'machinename\ASPNET'

  
    SQL MANAGEMENT STUDIO > MANAGEMENT > DATABASE MAIL > right click and select CONFIGURE… > select MANAGE PROFILE SECURITY > SQL MANAGEMENT
    put a check on PUBLIC option
    click on DEFAULT PROFILE and set it to YES
    STUDIO > DATABASES > SYSTEM DATABASES > right click on MSDB and select NEW QUERY > then enter > grant execute on sp_send_dbmail to public and click OK
