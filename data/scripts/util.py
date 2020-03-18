# from xlrd import open_workbook
import xlrd
import pyodbc

import pdfkit
path_wkhtmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

from flask import render_template, make_response
from werkzeug.security import generate_password_hash, check_password_hash

RX_CONNECTION_STRING='DRIVER={SQL Server};SERVER=localhost;DATABASE=RXBackend;Trusted_Connection=yes'
CIPS_CONNECTION_STRING='DRIVER={SQL Server};SERVER=localhost;DATABASE=CIPS;Trusted_Connection=yes'

def print_report(report, template, rpt_id):
    rpt_files = []
    rendered = render_template(template, report=report )
    rendered = rendered.encode()
    rpt_filename = "rpt_" + rpt_id + ".html"
    rpt_files.append("temp/" + rpt_filename)
    with open("temp/" + rpt_filename,"wb") as fo:
        fo.write(rendered)
        
    pdfkit.from_file(rpt_files, "static/pdf/" + rpt_id + ".PDF", configuration=config)
    

def readXLS(xFile):
    workbook = xlrd.open_workbook(xFile)
    workbook = xlrd.open_workbook(xFile, on_demand = True)
    worksheet = workbook.sheet_by_index(0)
    first_row = [] # The row where we stock the name of the column
    for col in range(worksheet.ncols):
        first_row.append( worksheet.cell_value(0,col) )
    # tronsform the workbook to a list of dictionnary
    data =[]
    for row in range(1, worksheet.nrows):
        elm = {}
        r = ''
        for col in range(worksheet.ncols):
            elm[first_row[col]]=worksheet.cell_value(row,col)
            r += str(col) + ':  ' + str(elm[first_row[col]]) + '  '
        print(str(r))
        data.append(elm)
        
def read_users(xFile):
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    sql = "{CALL dbo.rpt_update_user (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)}"
    workbook = xlrd.open_workbook(xFile)
    workbook = xlrd.open_workbook(xFile, on_demand = True)
    worksheet = workbook.sheet_by_index(0)
    username = ''
    first_name = ''
    last_name= ''
    pw = ''
    i=''
    pos=''
    email=''
    role=''
    first_row = [] # The row where we stock the name of the column
    for col in range(worksheet.ncols):
        first_row.append( worksheet.cell_value(0,col) )
    # tronsform the workbook to a list of dictionnary
    data =[]
    for row in range(1, worksheet.nrows):
        elm = {}
        vals = [] 
        r = ''
        for col in range(worksheet.ncols):
            elm[first_row[col]]=worksheet.cell_value(row,col)
            r += str(col) + ':  ' + str(elm[first_row[col]]) + '  '
            vals.append(str(elm[first_row[col]]))
        
        params = ((vals[0],vals[2],vals[3],vals[6],generate_password_hash(vals[1].strip().replace('.0', '')),int(vals[7].replace('.0','')),vals[5], 'SYS', vals[4] ))
        # params = ((request.form['txtUsername'], request.form['txtFirstname'], request.form['txtLastname'], 
        #             request.form['selPosition'],generate_password_hash(request.form['txtPassword']), 
        #             int(request.form['selRole']), request.form['txtInitials'], session['initials'],  
        #             request.form['txtEmail'] ))
        sql = "{CALL rpt_put_user (?, ?, ?, ?, ?, ?, ?, ?, ?)}" 
        cur.execute(sql, params)
        conn.commit() 
        print(vals[1].strip().replace('.0', ''))  
        print(params)
        # print(str(r))
        data.append(elm)

def import_users(userame,first_name,last_name,position,pw,role,initials,created_by,email):
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    sql = "{CALL dbo.rpt_update_user (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)}"
    params = (( userame,first_name,last_name,position,pw,int(role),initials,created_by,email ))
    cur.execute(sql, params)
    conn.commit()


def iou_reprint():
    iou_files = []
    iou_id = request.form['id']
    batch = request.form['batch']
    facility = request.form['facility']
    medication = request.form['medication']
    name = request.form['name']
    kop = request.form['kop']
    org_qty = request.form['org_qty']
    iou_qty = request.form['iou_qty']
    user = request.form['user']
    ship = request.form['ship']
    tech = request.form['tech']
    fill_date = request.form['fill_date'] 
    logo = "../static/images/ihs-pharmacy-logo.png"  
    print(id,batch,facility,medication,name,kop, org_qty,iou_qty, user, fill_date,ship,tech)
    # return id
    rendered = render_template('iou_delivery.html', batch=batch, facility = facility, medication = medication, name = name, org_qty = org_qty, iou_qty = iou_qty, pharm_tech = tech, fill_date = fill_date, logo=logo, ship = ship, tech = tech, iou_user = user )
    iou_filename = "iou_" + iou_id + ".html"
    iou_files.append("temp/" + iou_filename)
    with open("temp/" + iou_filename,"wb") as fo:
        fo.write(rendered)
    
    pdfkit.from_file(iou_files, "static/pdf/" + iou_id + ".pdf", configuration=config)

    return 'True'

read_users('employee_mod_import.xlsx') #employee_mod_import.xlsx
# read_users('UsersTest.xlsx')