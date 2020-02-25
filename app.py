import os
import collections
import json
import pyodbc
import time

from flask import Flask, render_template, url_for, request, redirect, jsonify, session, make_response
# Flask-LoginManager
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import urllib 
import db_scripts as dbs

# GLOBALS
RX_CONNECTION_STRING='DRIVER={SQL Server};SERVER=localhost;DATABASE=RXBackend;Trusted_Connection=yes'
CIPS_CONNECTION_STRING='DRIVER={SQL Server};SERVER=localhost;DATABASE=CIPS;Trusted_Connection=yes'
REPORTNG_VERSION = '0.5'

## Init APP
app = Flask(__name__)
app.secret_key = 'super secret string'
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


@app.route("/occur", methods=["GET", "POST"])
@login_required
def occur():
    page_title = "Occurences" 
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    # print(session['userid'])
    
    if request.method == 'POST':
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
                request.form['selPerComp'], 
                int(request.form['selIntake']), 
                int(request.form['selMed']), 
                int(request.form['selShipping']), 
                int(request.form['selDelivery']), 
                int(request.form['selBilling']), 
                int(request.form['selCooking']), 
                int(request.form['selOther']), 
                int(request.form['selTechInv']), 
                int(request.form['selRphInv']), 
                request.form['txtExp'],
                session['initials']))
            # print(params)
            cur.execute(sql, params)
            conn.commit()
        elif request.form['op-code'] == 'delete':
            cur.execute("DELETE FROM dbo.RPT_REASONS WHERE ID=?", request.form['del_code'])
            conn.commit()
        elif request.form['op-code'] == 'update':
            sql = dbs.update_occurence
            params=((int(session['userid']), 
            request.form['dateReport'], 
            request.form['dateOccur'],
            current_user.id,  
            request.form['selFac'], 
            request.form['txtPatient'], 
            request.form['txtPerRept'], 
            request.form['txtPhone'], 
            request.form['selPerComp'], 
            int(request.form['selIntake']), 
            int(request.form['selMed']), 
            int(request.form['selShipping']), 
            int(request.form['selDelivery']), 
            int(request.form['selBilling']), 
            int(request.form['selCooking']), 
            int(request.form['selOther']), 
            int(request.form['selTechInv']), 
            int(request.form['selRphInv']), 
            request.form['txtExp'],
            session['initials'],
            int(request.form['id']) ))
            # print(params)
            cur.execute(sql, params)
            conn.commit()
    
    sql = dbs.get_reasons_by_category
    cur.execute(sql) 
    
    print(current_user.id)
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
        
    return render_template('occur.html', page_title = page_title, users=user_list, reasons=reason_list, facilities=facility_list)

@app.route('/getSearch', methods=['POST'])
def getSearch():
        sql = request.form['sql']
        items = dbs.get_json(sql)        
        items = jsonify(items)

        return items

@app.route('/login', methods=["GET", "POST"])
def login():
    errors=None
    if request.method == 'GET':
        return render_template('login.html', errors=errors)
    
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
    
    if check_password_hash(u['password'], request.form['password']):		
        user = User()
        user.id = username
        session['role'] = u['role']
        session['initials'] = str.strip(u['initials'])
        session['userid'] = u['userid']
        login_user(user)

        return redirect(url_for('index'))
    else:
        errors = "Invalid Username or Password"
        return render_template('login.html', errors=errors, page_title = page_title) 

@app.route("/admin/codes", methods=["GET", "POST"])
@login_required
def admin_codes():
    if session['role'] != 'Administrator':
        return redirect(url_for('pending'))
    
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
            return redirect(url_for('pending'))
    page_title = "User Manager"
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    
    if request.method == "POST":
        if request.form['op-code'] == 'update':
            if len(request.form['txtPassword']) > 0:
                password=generate_password_hash(request.form['txtPassword'])
            sql = "{CALL dbo.rpt_update_user (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)}"
            params= ((request.form['txtUsername'], request.form['txtFirstname'], request.form['txtLastname'], request.form['selPosition'], generate_password_hash(request.form['txtPassword']), int(request.form['selRole']), request.form['txtInitials'], int(request.form['active']),session['initials'], int(request.form['user-id']) ))  
            cur.execute(sql, params)
            conn.commit()
        elif request.form['op-code'] == 'delete':			
            cur.execute("DELETE FROM RPT_USERS WHERE ID=?", int(request.form['del_user_id']))
            conn.commit()
        else:
            sql = "{CALL rpt_put_user (?, ?, ?, ?, ?, ?, ?, ?)}" 
            params = ((request.form['txtUsername'], request.form['txtFirstname'], request.form['txtLastname'], request.form['selPosition'],generate_password_hash(request.form['txtPassword']), int(request.form['selRole']), request.form['txtInitials'], session['initials']))			
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
        objects_list.append(d)

    return render_template('admin/users.html', users=objects_list, page_title = page_title)

@app.route('/logout')
def logout():	
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
    app.run(debug=True)
    
# if __name__ == "__main__":
#     app.run(host= '0.0.0.0')