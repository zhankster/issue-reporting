import os
import collections
import json
import pyodbc
import time

from flask import Flask, flash, render_template, url_for, request, redirect, jsonify, session, make_response
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
# from xlrd import open_workbook
import urllib 
import pdfkit
path_wkhtmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

import db_scripts as dbs
import util as pr

import logging
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
# logger = logging.getLogger('werkzeug')
# handler = logging.FileHandler('log/demo.log')
# logger.addHandler(handler)
# logging.basicConfig(filename='log/info.log',
# level=logging.INFO,
# format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# logging.basicConfig(filename='log/error.log',
# level=logging.ERROR,
# format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
# GLOBALS
RX_CONNECTION_STRING='DRIVER={SQL Server};SERVER=localhost;DATABASE=RXBackend;Trusted_Connection=yes'
CIPS_CONNECTION_STRING='DRIVER={SQL Server};SERVER=localhost;DATABASE=CIPS;Trusted_Connection=yes'
REPORTNG_VERSION = '0.5'
UPLOAD_FOLDER = r'C:/inetpub/wwwroot/RxApps/static/pdf'
# UPLOAD_FOLDER = r'D:/Dev/FLW/Occurrence/static/pdf'

## Init APP
app = Flask(__name__)
app.secret_key = 'super secret string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
login_manager = LoginManager()
login_manager.session_protection='basic'
login_manager.init_app(app)

general_users = ('Administrator','User')
pharm_redirect = "iou"


def check_role(roles):
    if session['role'] not in roles:
        print(roles)
        return 'false'
    return 'true'
    
class User(UserMixin):
    pass

@app.route("/", methods=["GET"])
def index():
    return redirect(url_for('occur'))

ALLOWED_EXTENSIONS = set([ 'pdf'])
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route('/upload', methods=['POST','GET'])
def upload():
    dt = datetime.now()
    date_rpt = None
    id_rpt = None
    facility = None
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    
    if request.method == 'POST':
        if request.form['attDate'] == 'null':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No file selected for uploading')
                return redirect(request.url)
            if file and allowed_file(file.filename):                              
                id_rpt = request.form['attID'] 
                date_rpt = request.form['attDateRet'] 
                facility = request.form['attFac'] 
                file.filename =  id_rpt + '_' + dt.strftime('%H%M%S%f') + '.pdf'
                sql = 'UPDATE dbo.RPT_OCCUR SET UPLOAD = ? WHERE ID = ?'
                params = (( file.filename, int(id_rpt) ))
                cur.execute(sql, params)
                conn.commit()
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('File successfully uploaded')
                dbs.add_activity('UPLOAD ',session['userid'], filename, 'RPT_OCCUR', '0', id_rpt )
                # return redirect(url_for('upload'))
                # return redirect('/upload')
                return render_template('upload.html', facility=facility, id_rpt=id_rpt, date_rpt=date_rpt)
            else:
                flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
                return redirect(request.url)
        else:
            date_rpt = request.form['attDate']
            id_rpt = request.form['attID']
            facility = request.form['attFac']
            return render_template('upload.html', facility=facility, id_rpt=id_rpt, date_rpt=date_rpt)

    return render_template('upload.html', facility=facility, id_rpt=id_rpt, date_rpt=date_rpt)


@app.route("/occur/", defaults={'rpt_id': '0'})
@app.route("/occur/<rpt_id>", methods=["GET"])
@login_required
def occur_get(rpt_id):
    return getOccurItems(rpt_id)

@app.route("/occur", methods=[ "POST"])
@login_required
def occur():
    page_title = "Occurences"
    report_items = []
    dt = datetime.now()
    id_rpt = ''
    pdf = None
    mmg = ''
    rpt_ts = dt.strftime('%H%M%S%f')
    rpt_ts = str(round(datetime.utcnow().timestamp(),3))
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    # print(session['userid'])
    
    if request.method == 'POST':
        if request.form['op-code'] == 'insert' or request.form['op-code'] == 'reprint':
            sql = dbs.get_facility_info
            params=(( request.form['selFac'] ))
            cur.execute(sql, params)
            row = cur.fetchone()
            mmg = row.SHORT_NAME
            
            d = collections.OrderedDict()
            d['dateReport'] = request.form['dateReport']
            d['dateOccur'] = request.form['dateOccur']
            d['facCode'] = request.form['selFac']
            d['facName'] = request.form['facName']
            d['patient'] = request.form['txtPatient']
            d['phone'] = request.form['txtPhone']
            d['perCompName'] = request.form['perCompName']
            d['dept'] = request.form['currentDept']
            d['perRpt'] = request.form['txtPerRept']
            d['reason'] = request.form['currentReason']
            d['techName'] = request.form['techName']
            d['rphName'] = request.form['rphName']
            d['explanation'] = request.form['txtExp']
            d['logo'] = '../static/images/ihs-pharmacy-logo.png'
            d['mmg'] = mmg
            
            report_items.append(d)
            
        if request.form['op-code'] == 'insert': 
            sql = dbs.insert_occurence
            params=((int(session['userid']), 
                    request.form['dateReport'], 
                    request.form['dateOccur'],
                    current_user.id,  
                    request.form['selFac'], 
                    request.form['txtPatient'], 
                    request.form['txtPerRept'], 
                    request.form['txtPhone'], 
                    int(request.form['selPerComp']), 
                    int(request.form['selTechInv']), 
                    int(request.form['selRphInv']), #currentRCode
                    int(request.form['currentRCode']),
                    request.form['txtExp'],
                    session['initials'],
                    rpt_ts + '.PDF',
                    int(request.form['reqTech']),
                    int(request.form['reqRph'])
                    ))
            sql = "{CALL dbo.rpt_put_occurence (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,? )}"
            cur.execute(sql, params)
            conn.commit()
            print("Commit: ")
            return retOccur(cur, rpt_ts,report_items)
            sql = """SELECT ID FROM RPT_OCCUR WHERE TIMESTAMP = ?"""
            params=(( rpt_ts ))
            print(sql, params)
            cur.execute(sql, params)
            row = cur.fetchone()
            id_rpt = str(row[0])
            pr.print_report(report_items,'occur_rpt.html', rpt_ts)
            objects_list = []
            temp = {}
            temp['id_rpt'] = id_rpt
            temp['pdf'] = rpt_ts + '.PDF'
            objects_list.append(temp)
            return jsonify(objects_list)
            
        elif request.form['op-code'] == 'delete':
            cur.execute("DELETE FROM dbo.RPT_REASONS WHERE ID=?", request.form['del_code'])
            conn.commit()
        elif request.form['op-code'] == 'update':  #bbbb
            sql = dbs.update_occurence
            pdf = request.form['pdf']
            params=((int(session['userid']), 
            request.form['dateReport'], 
            request.form['dateOccur'],
            current_user.id,  
            request.form['selFac'], 
            request.form['txtPatient'], 
            request.form['txtPerRept'], 
            request.form['txtPhone'], 
            int(request.form['selPerComp']), 
            int(request.form['selIntake']), 
            int(request.form['selMed']), 
            int(request.form['selShipping']), 
            int(request.form['selDelivery']), 
            int(request.form['selBilling']), 
            int(request.form['selCooking']), 
            int(request.form['selWsale']),
            int(request.form['selOther']), 
            int(request.form['selTechInv']), 
            int(request.form['selRphInv']), 
            int(request.form['currentRCode']),
            request.form['txtExp'],
            session['initials'],
            int(request.form['reqTech']),
            int(request.form['reqRph']), 
            int(request.form['id']) ))
            
            d = collections.OrderedDict()
            d['dateReport'] = request.form['dateReport']
            d['dateOccur'] = request.form['dateOccur']
            d['facCode'] = request.form['selFac']
            d['facName'] = request.form['facName']
            d['patient'] = request.form['txtPatient']
            d['phone'] = request.form['txtPhone']
            d['perCompName'] = request.form['perCompName']
            d['dept'] = request.form['currentDept']
            d['perRpt'] = request.form['txtPerRept']
            d['reason'] = request.form['currentReason']
            d['techName'] = request.form['techName']
            d['rphName'] = request.form['rphName']
            d['explanation'] = request.form['txtExp']
            d['logo'] = '../static/images/ihs-pharmacy-logo.png'
            d['mmg'] = mmg
            
            report_items.append(d)
            # print(params)
            cur.execute(sql, params)
            conn.commit()
            dbs.add_activity('UPDATE ',session['userid'], 'Report', 'RPT_OCCUR','0', request.form['id'])
            
            pr.print_report(report_items,'occur_rpt.html', pdf.replace('.PDF', ''))
    
    return getOccurItems('0')

# Accept report
@app.route("/occur/accept", methods=[ "POST"])
@login_required
def occur_accept():
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    
    user_type =  request.form['user_type']
    rpt_id = request.form['rpt_id']
    user_id = request.form['user_id']
    witness_type = request.form['witness_type']
    sql = """ UPDATE [RPT_OCCUR]
        SET  """ + user_type + """ = GETDATE(),
        """ + witness_type + """ =""" + str(session['userid'] ) + """ 
        WHERE ID =  """ + rpt_id
    
    cur.execute(sql)
    conn.commit()
    session['accept'] = 'none'
    dbs.add_activity('ACCEPT ',session['userid'], 'Accept Occurrence report' , 'RPT_OCCUR', user_id, rpt_id )
    
    return redirect(url_for('admin_signoff'))

# Goes to login for sign off
@app.route("/occur/signoff/user/<user_data>", methods=[ "GET"])
@login_required
def occur_signoff_user(user_data):
    page_title = "Sign Off Login"
    errors = None
    vals = user_data.split("_")
    rpt_id = vals[0]
    user_id = vals[1]
    typ  = vals[2]
    username = vals[3]
    return render_template('login_signoff.html', errors=errors, 
            page_title=page_title, user_data=user_data,rpt_id=rpt_id,user_id=user_id, typ=typ, username=username,)

# Login for report to accept
@app.route("/occur/signoff/login", methods=[ "POST"])
@login_required
def occur_signoff_login():
    username = request.form['txtUsername']
    password = request.form['txtPassword']
    accept_login = session['accept']
    user_data = request.form['user_data']
    vals = user_data.split("_")
    rpt_id = vals[0]
    user_id = vals[1]
    typ  = vals[2]
    
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    sql = dbs.get_users_username
    cur.execute(sql, username)
    
    rows = cur.fetchall()
    if len(rows) <= 0:
        errors = "Invalid Username or Password"
        return render_template('login_signoff.html', errors=errors, user_data=user_data,rpt_id=rpt_id,user_id=user_id, typ=typ)
    
    u = {}
    for row in rows:
        u['password'] = row.PASSWORD
        u['username'] = row.USERNAME
        u['role'] = row.ROLE_NAME
        u['initials'] = row.INITIALS
        u['userid'] = row.ID
        
        # print(user_id, row.ID)
    if user_id.strip() != str(row.ID):
        errors = "User does not match the id for sign off document"
        return render_template('login_signoff.html', errors=errors,user_data=user_data,
                rpt_id=rpt_id,user_id=user_id, typ=typ)
    
    session['accept'] = user_id
    dbs.add_activity('LOGIN_A ',session['userid'], 'Login for report accept', 'RPT_OCCUR', user_id , rpt_id)
    
    return redirect('/occur/signoff/' + user_data)
    
# Goes to report to accept
@app.route("/occur/signoff/<rpt_id>", methods=[ "GET"])
@login_required
def occur_sign(rpt_id):
    page_title = "Sign Off Form"
    accept_login = session['accept']
    vals = rpt_id.split("_")
    rpt_id = vals[0]
    user_id = vals[1]
    typ  = vals[2]
    
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    sql = dbs.get_signoff_users(' AND RPT_OCCUR.ID=' + rpt_id)
    cur.execute(sql)
    rows = cur.fetchall()
    
    report = []
    for row in rows:
        d = collections.OrderedDict()
        d['dateReport'] = row.DISCOVER_DATE
        d['dateOccur'] = row.OCCUR_DATE
        d['facCode'] = row.FACILITY_CODE
        d['facName'] = row.DNAME
        d['patient'] = row.PATIENT_NAME
        d['phone'] = row.PHONE
        d['perCompName'] = row.PER_COMP
        d['dept'] = row.DEPT
        d['perRpt'] = row.PERSON_REPORTING
        d['reason'] = row.REASON
        d['techName'] = row.TECH
        d['rphName'] = row.RPH
        d['explanation'] = row.EXPLANATION
        d['logo'] = '../../static/images/ihs-pharmacy-logo.png'
        d['mmg'] =  ''
        report.append(d)
        
    return render_template('occur_rpt.html', page_title = page_title, report=report, user_id=user_id, typ=typ, rpt_id=rpt_id, accept_login=accept_login)

def retOccur(cur, rpt_ts, report_items):
    sql = """SELECT ID FROM RPT_OCCUR WHERE TIMESTAMP = ?"""
    params=(( rpt_ts ))
    # print(sql, params)
    cur.execute(sql, params)
    row = cur.fetchone()
    id_rpt = str(row[0])
    pr.print_report(report_items,'occur_rpt.html', rpt_ts)
    objects_list = []
    temp = {}
    temp['id_rpt'] = id_rpt
    temp['pdf'] = rpt_ts + '.PDF'
    objects_list.append(temp)
    return jsonify(objects_list)


def getOccurItems(rpt_id):
    page_title = "Occurences"
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    sql = dbs.get_reasons_by_category
    cur.execute(sql) 
    
    rows = cur.fetchall()
    reason_list = []
    for row in rows:
        d = collections.OrderedDict()
        # print(row.CODE)
        d['id'] = row.ID
        d['code'] = row.CODE
        d['reason_desc'] = row.REASON_DESC
        d['category_desc'] = row.CATEGORY_DESC
        d['sort_order'] = row.SORT_ORDER
        d['category_code'] = row.CATEGORY_CODE
        reason_list.append(d)
        
    sql = dbs.get_users
    cur.execute(sql) 
    
    rows = cur.fetchall()
    user_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['id'] = row.ID
        d['useranme'] = row.USERNAME
        d['firstname'] = row.FIRST_NAME
        d['lastname'] = row.LAST_NAME
        d['username'] = row.USERNAME
        d['position'] = row.POSITION
        d['role'] = row.ROLE_NAME
        user_list.append(d)
    sql = dbs.get_facilities
    conn = pyodbc.connect(CIPS_CONNECTION_STRING)
    cur = conn.cursor()
    cur.execute(sql) 
    
    rows = cur.fetchall()
    facility_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['id'] = row.ID
        d['code'] = row.DCODE
        d['name'] = row.DNAME
        facility_list.append(d)
        
    return render_template('occur.html', page_title = page_title, users=user_list, current_id=session['userid'],
                        reasons=reason_list, facilities=facility_list, rpt_id=rpt_id)

@app.route('/getSearch', methods=['POST'])
def getSearch():
    sql = request.form['sql']
    items = dbs.get_json(sql)        
    items = jsonify(items)

    return items
    
@app.route('/updateStatus', methods=['POST'])
def updateStatus():
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    sql = request.form['sql']
    rpt_id = request.form['id']
    status = request.form['status']
    # msg = 'Report Voided' if '0' else 'Report Set Valid'
    msg = "Status"
    
    cur.execute(sql)
    conn.commit()
    dbs.add_activity('UPDATE ',session['userid'], 'RPT_OCCUR, ID:' + rpt_id + ', for  void(' + status + ')', '', '0', '0')

    return msg

@app.route('/login', methods=["GET", "POST"])
def login():
    errors=None
    page_title = "Sign Off Login"
    if request.method == 'GET':
        return render_template('login.html', errors=errors, page_title=page_title )
    
    username = request.form['username']
    page_title = "Login"
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    sql = dbs.get_users_username
    cur.execute(sql, username)
    
    rows = cur.fetchall()
    if len(rows) <= 0:
        errors = "Invalid Username or Password"
        return render_template('login.html', errors=errors)
    u = {}
    for row in rows:
        u['password'] = row.PASSWORD
        u['username'] = row.USERNAME
        u['role'] = row.ROLE_NAME
        u['initials'] = row.INITIALS
        u['userid'] = row.ID
    print(u['password'])
    print(request.form['password'])
    print(check_password_hash(u['password'], request.form['password']))
    if check_password_hash(u['password'], request.form['password']):		
        user = User()
        user.id = username
        session['role'] = u['role']
        session['initials'] = str.strip(u['initials'])
        session['userid'] = u['userid']
        session['accept'] = 'none'
        dbs.add_activity('LOGIN',u['userid'], 'Main login', '', '0' , '0')
        app.logger.info('%s logged in successfully', user.id)
        login_user(user)

        return redirect(url_for('index'))
    else:
        errors = "Invalid Username or Password"
        return render_template('login.html', errors=errors, page_title = page_title) 

# Displays list of users who need to sign off
@app.route('/admin/signoff',  methods=["GET"])
@login_required
def admin_signoff():
    if session['role'] != 'Administrator':
        return redirect(url_for('occur'))
    page_title = "Occurrence Sign Off"
    
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    sql = dbs.get_signoff_users('') 
    # print(sql)
    cur.execute(sql)
    rows = cur.fetchall()
    
    signoff= []
    for row in rows:
        d = collections.OrderedDict()
        d['rph_name'] = row.RPH_NAME
        d['rph_username'] = row.RPH_USERNAME
        d['rph_id_sign'] = row.RPH_ID_SIGN
        d['tech_name'] = row.TECH_NAME
        d['tech_username'] = row.TECH_USERNAME
        d['tech_id_sign'] = row.TECH_ID_SIGN
        d['discover_date'] = row.DISCOVER_DATE
        d['person_reporting'] = row.PERSON_REPORTING
        d['occur_date'] = row.OCCUR_DATE
        d['dept'] = row.DEPT
        d['reason'] = row.REASON
        d['rpt_id'] = row.ID
        signoff.append(d)
    
    return render_template('admin/signoff.html',  page_title = page_title, signoff=signoff, witness=session['userid']) 
    
@app.route("/admin/email", methods=["GET", "POST"])
@login_required
def admin_email():
    if session['role'] != 'Administrator':
        return redirect(url_for('occur'))
    
    page_title = "Email Groups"
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    
    if request.method == 'POST':
        if request.form['usage'] == 'email':
            params=(( request.form['recipients'],request.form['target'],request.form['usage'] ))
            sql = dbs.update_groups
            # print(request.form['recipients'],request.form['target'],request.form['usage'])
            # print(sql)
            cur.execute(sql, params)
            conn.commit()
            dbs.add_activity('EMAIL ',session['userid'], 'Occurrence group update' , '', '0', '0')
    
    sql = dbs.get_recipients
    params=(( 'occurrence','email' ))
    cur.execute(sql, params)
    row = cur.fetchone()
    occ_recip = row[0].split(';')
    print(occ_recip)
    
    return render_template('admin/email.html',occ_recip = occ_recip ,page_title = page_title) 

@app.route("/admin/codes", methods=["GET", "POST"])
@login_required
def admin_codes():
    if session['role'] != 'Administrator':
        return redirect(url_for('occur'))
    
    page_title = "Reason Codes"
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    sql = dbs.insert_reasons
    category_code = ''
    op_code = ''
    
    if request.method == 'POST':
        if request.form['op-code'] == 'insert':
            sql = dbs.insert_reasons
            params=((str.rstrip(request.form['selCategory']),request.form['txtDesc'],int(request.form['txtSort']), session['initials']))
            cur.execute(sql, params)
            conn.commit()
        elif request.form['op-code'] == 'delete':
            op_code = 'delete'
            category_code = request.form['delCatCode']
            cur.execute("DELETE FROM dbo.RPT_REASONS WHERE ID=?", request.form['del_code'])
            conn.commit()
        elif request.form['op-code'] == 'edit':
            sql = dbs.update_reasons
            params= ((str.rstrip(request.form['selCategory']),request.form['txtDesc'],int(request.form['txtSort']),
                session['initials'], int(request.form['active']) , int(request.form['code-id'])))
            # print(params)
            cur.execute(sql, params)
            conn.commit()
            dbs.add_activity('UPDATE',session['userid'], '' , 'RPT_CODES',  '0', request.form['code-id'])
    
    sql = dbs.reason_codes('')
    cur.execute(sql)
    rows = cur.fetchall()
    
    code_list = []
    cnt = 0
    for row in rows:
        d = collections.OrderedDict()
        if cnt == 1 and category_code != '':
            category_code = row.CATEGORY_CODE
        d['code'] = row.ID
        d['description'] = row.DESCRIPTION
        d['sort_order'] = row.SORT_ORDER
        d['category_code'] = row.CATEGORY_CODE
        d['active'] = row.ACTIVE
        d['category'] = row.CATEGORY
        d['user'] = session['initials']
        cnt = cnt + 1
        code_list.append(d)

    # print(category_code)
    sql_c = dbs.category_codes
    cur.execute(sql_c)
    rows_c = cur.fetchall()
    
    category_list = []
    for row in rows_c:
        c = collections.OrderedDict()
        c['code'] = row.CODE
        c['description'] = row.DESCRIPTION
        # print(c['description'] )
        category_list.append(c)

    
    return render_template('admin/codes.html', codes=code_list, categories=category_list, category_code=category_code,page_title = page_title )


@app.route("/admin/users", methods=["GET", "POST"])
@login_required
def admin_users():
    if session['role'] != 'Administrator':
            return redirect(url_for('occur'))
    page_title = "User Manager"
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    
    if request.method == "POST":
        if request.form['op-code'] == 'update':
            if len(request.form['txtPassword']) > 0:
                password=generate_password_hash(request.form['txtPassword'])
            sql = "{CALL dbo.rpt_update_user (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)}"
            params= ((request.form['txtUsername'], request.form['txtFirstname'], request.form['txtLastname'], request.form['selPosition'], generate_password_hash(request.form['txtPassword']), int(request.form['selRole']), request.form['txtInitials'], int(request.form['active']),session['initials'], int(request.form['user-id']), request.form['txtEmail'] ))  
            cur.execute(sql, params)
            conn.commit()
            dbs.add_activity('UPDATE', session['userid'],'', 'RPT_USERS',  '0', request.form['user-id'] )
        elif request.form['op-code'] == 'delete':			
            cur.execute("DELETE FROM RPT_USERS WHERE ID=?", int(request.form['del_user_id']))
            conn.commit()
        else:
            sql = "{CALL rpt_put_user (?, ?, ?, ?, ?, ?, ?, ?, ?)}" 
            params = ((request.form['txtUsername'], request.form['txtFirstname'], request.form['txtLastname'], request.form['selPosition'],generate_password_hash(request.form['txtPassword']), int(request.form['selRole']), request.form['txtInitials'], session['initials'],  request.form['txtEmail'] ))			
            cur.execute(sql, params)
            conn.commit()			
    
    sql = dbs.get_users
    cur.execute(sql)
    rows = cur.fetchall()
    
    objects_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['id'] = row.ID
        d['username'] = row.USERNAME
        d['firstname'] = row.FIRST_NAME
        d['lastname'] = row.LAST_NAME
        d['position'] = row.POSITION
        d['initials'] = row.INITIALS
        d['active'] = row.ACTIVE
        d['password'] = row.PASSWORD
        d['role'] = row.ROLE_ID
        d['email'] = row.EMAIL
        objects_list.append(d)

    return render_template('admin/users.html', users=objects_list, page_title = page_title)

@app.route('/logout')
def logout():
    dbs.add_activity('LOGOUT',session['userid'], 'Main logout', '', '0', '0' )
    logout_user()
    return redirect(url_for('login'))

@login_manager.user_loader
def user_loader(username):    
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    sql = dbs.get_users_username
    cur.execute(sql, username)
    u = {}
    rows = cur.fetchall()
    if len(rows) <= 0:
        return
        
    for row in rows:
        u['username'] = row.USERNAME		
        
    user = User()
    user.id = username
    
    return user
    

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    sql = dbs.get_users_username
    cur.execute(sql, username)
    
    u = {}
    rows = cur.fetchall()
    print(rows)
    if len(rows) <= 0:
        return   
    for row in rows:
        u['username'] = row.USERNAME
        u['password'] = row.PASSWORD
    
    user = User()
    user.id = username
        
    if check_password_hash(u['password'], request.form['password']):
        user.is_authenticated = True
    else:
        return
    return user



if __name__ == "__main__":
    handler = RotatingFileHandler('log/info.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO) 
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.run(debug=True)
    
# if __name__ == "__main__":
#     handler = RotatingFileHandler('log/info.log', maxBytes=10000, backupCount=1)
#     handler.setLevel(logging.INFO) 
#     formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#     handler.setFormatter(formatter)
#     app.logger.addHandler(handler)
#     app.run(host= '0.0.0.0')