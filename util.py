# from xlrd import open_workbook
import xlrd

import pdfkit
path_wkhtmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

from flask import render_template, make_response

def print_report(report, template, rpt_id):
    rpt_files = []
    rendered = render_template(template, report=report ,  typ=None)
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
            r += 'Row:  ' + elm[first_row[col]] + '  '
        print(r)
        data.append(elm)
    # print (data)


# book = xlrd.open_workbook('import.xls')

# max_nb_row = 0
# for sheet in book.sheets():
#     max_nb_row = max(max_nb_row, sheet.nrows)

# for row in range(max_nb_row):
#     for sheet in book.sheets():
#         if row < sheet.nrows:
#             print sheet.row(row)



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