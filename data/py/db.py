import collections
import json
import pyodbc

RX_CONNECTION_STRING='DRIVER={SQL Server};SERVER=localhost;DATABASE=RXBackend;Trusted_Connection=yes'
CIPS_CONNECTION_STRING='DRIVER={SQL Server};SERVER=localhost;DATABASE=CIPS;Trusted_Connection=yes'
# fac_code, address, arx
def insert_fac_email_arx():
    return  """INSERT INTO [dbo].[FAC_EMAIL]
        ([FAC_CODE]
        ,[ADDRESS]
        ,[ARX]
        ,[IOU]
        ,[Billing])
    VALUES
        (?
        ,?
        ,?
        ,0
        ,0)"""

# fac_code, address, iou

def insert_fac_email_iou() :
    return """INSERT INTO [dbo].[FAC_EMAIL]
        ([FAC_CODE]
        ,[ADDRESS]
        ,[ARX]
        ,[IOU]
        ,[Billing])
    VALUES
        (?
        ,?
        ,0
        ,?
        ,0)"""
        
        
def update_fac_arx():
    return""" UPDATE [FAC_EMAIL]
    SET 
    [ARX] = ?
    WHERE [FAC_CODE] = ? """        
        
def update_fac_iou():
    return""" UPDATE [FAC_EMAIL]
    SET 
    [IOU] = ?
    WHERE [FAC_CODE] = ? """
    

def email_exists(code, email):
    sql = """ SELECT count(FAC_CODE) cnt
            FROM FAC_EMAIL
            WHERE LTRIM(RTRIM(FAC_CODE)) = ?
            AND           
            LTRIM(RTRIM(ADDRESS)) = ?"""
    params=(( code, email ))
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    cur.execute(sql, params)
    row = cur.fetchone()
    cnt= str(row[0])
    return int(cnt)
        
# arx = insert_fac_email_arx()
# iou = insert_fac_email_arx()
# print(arx)
# print(iou)

sql = ("SELECT top 7 * FROM FAC_ALT WHERE LEN(IOU_EMAIL) > 4 OR  LEN(EMAIL) > 4 ")
# sql = ("SELECT top 1 * FROM FAC_ALT WHERE LEN(EMAIL) > 4 ")
# sql = ("SELECT top 5 * FROM FAC_ALT WHERE LEN(IOU_EMAIL) > 4 OR LEN(EMAIL) > 4 ")
sql = ("SELECT  * FROM FAC_ALT  where DCODE in ('1C', '1F', '000', '2L', '2LF') ORDER BY DCODE")
conn = pyodbc.connect(RX_CONNECTION_STRING)
cur = conn.cursor()
cur.execute(sql) 
    
rows = cur.fetchall()
fac = []
cnt = 0
for row in rows:
    code = row.DCODE
    arx_email = str(row.EMAIL).split(';')
    c = 0
    f = []
    for ar in arx_email:
        a = collections.OrderedDict()
        # print(str(c)  + 'arx: ' + str(ar).strip() + " -- " + code)
        if str(ar).strip() != "" and ar != "None":
            # print(str(c)  + 'arx: ' + str(ar).strip() + " -- " + code)
            a['code'] = code.strip()
            a['email'] = str(ar).strip()
            a['notify'] = True
            a['type'] = 'arx'
            c += 1
            fac.append(a)
            f.append(a)
    iou_email = str(row.IOU_EMAIL).split(';')
    iou_notify = row.IOU_NOTIFY
    c = 0
    for iou in iou_email:
        i = collections.OrderedDict()
        # print(str(c) + 'iou: ' +  str(iou).strip() + " -- " + code)
        if str(iou).strip() != "" and iou != 'None':
            # print(str(c) + 'iou: ' +  str(iou).strip() + " -- " + code)
            i['code'] = code.strip()
            i['email'] = str(iou).strip()
            i['notify'] = iou_notify
            i['type'] = 'iou'
            c += 1
            fac.append(i)
            f.append(i)
    # print('----------------------------------------------')
    # print('#################################')
    # print(f)
    # cnt += 1
# print(fac)
    # print(f)
conn = pyodbc.connect(RX_CONNECTION_STRING)
for e in fac:
    code = e['code']
    email = e['email']
    typ = e['type']
    notify = int(e['notify'])
    # print(code, email, typ, notify)
    em = email_exists(code, email) 
    # print(em)
    # # print(str(int(e) > 1) + code, email)
    # print(em  < 1) 
    sql = ''     
    # print('"Email":' +code, email, typ, notify)  
    if em  < 1:
        if typ  == 'arx':
            sql = insert_fac_email_arx()
        else:
            sql = insert_fac_email_iou()
        params=(( code, email, notify))
        print(sql, params, typ)
        cur = conn.cursor()
        cur.execute(sql,params) 
        conn.commit()
    else:
        if typ  == 'arx':
            sql = update_fac_arx()
        else:
            sql = update_fac_iou()
        params=(( notify, code))
        print(sql, params, typ)
        cur = conn.cursor()
        cur.execute(sql,params) 
        conn.commit()
        pass
            
# cnt = email_exists('000', 'g@gmail.com')
# print(cnt)



