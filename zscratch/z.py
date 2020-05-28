def report_viewer_file(rpt):
    page_title = "Report Viewer"
    pdf_file = '/static/export/' + rpt
    if rpt == 'none' : 
        pdf_file = 'none'
    print('PDF:' + pdf_file)
    # {{url_for('static', filename='rpt/OPP2.pdf')}}
    return render_template('report_viewer.html',page_title = page_title, pdf_file = pdf_file  )
# logger = logging.getLogger('werkzeug')
# handler = logging.FileHandler('log/demo.log')
# logger.addHandler(handler)
# logging.basicConfig(filename='log/info.log',
# level=logging.INFO,
# format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# logging.basicConfig(filename='log/error.log',
# level=logging.ERROR,
# format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


# @app.route("/report_viewer/pdf")
# @login_required
# def report_viewer_pdf():
#     page_title = "Report Viewer"
#     report = request.args['rpt']
#     pdf_file = '/static/export/' + report
#     print('PDF:' + pdf_file)
#     # {{url_for('static', filename='rpt/OPP2.pdf')}}
#     return render_template('report_viewer.html',page_title = page_title, pdf_file = pdf_file  )
        
    
    rpt = ' -F ' + reports_path  + 'OP1.rpt'
    pdf = ' -O '+ export_path + 'OPP2.pdf -E pdf '
    params = '-A Fac:DJ -A "Date Range:(05-01-2020,05-26-2020)"'
    print(exe  +  dsnRx + rpt   + pdf   + params )
    subprocess.Popen(exe  +  dsnRx + rpt   + pdf   + params , shell=True)

    return redirect(url_for('report_viewer_file', pdf_file = pdf_file))
        return redirect('/occur/signoff/' + user_data)
    
    @app.route("/report_viewer/<rpt>", methods=[ "GET"])
@login_required


    if rpt_id != '0':
        return getOccurItems(rpt_id)
    else:
        return getOccurItems("0") 

@app.route('/upload', methods=['POST','GET'])
def upload():
    dt = datetime.now()
    date_rpt = None
    id_rpt = None
    facility = None
    page_title = "File Upload"
    
    if request.method == 'POST':
        if request.form['attDate'] == 'upload':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No file selected for uploading')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                id_rpt = request.form['attID'] 
                date_rpt = request.form['attDate']
                facility = request.form['attFac']  
                file.filename =  id_rpt + '_' + dt.strftime('%H%M%S%f') + '.pdf'
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('File successfully uploaded')
                # return redirect(url_for('upload'))
                return redirect('/upload')
            else:
                flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
                return redirect(request.url)
        else:
            date_rpt = request.form['attDate']
            id_rpt = request.form['attID']
            facility = request.form['attFac']
            return render_template('upload.html', facility=facility, id_rpt=id_rpt, date_rpt=date_rpt, page_title=page_title )

    return render_template('upload.html', facility=facility, id_rpt=id_rpt, date_rpt=date_rpt)


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
                    int(request.form['selIntake']), 
                    int(request.form['selMed']), 
                    int(request.form['selShipping']), 
                    int(request.form['selDelivery']), 
                    int(request.form['selBilling']), 
                    int(request.form['selCooking']), 
                    int(request.form['selOther']), 
                    int(request.form['selTechInv']), 
                    int(request.form['selRphInv']), #currentRCode
                    int(request.form['currentRCode']),
                    request.form['txtExp'],
                session['initials'])


@app.route("/ul")
def ul():
    return render_template('ul.html')

@app.route("/handleUpload", methods=['POST'])
def handleFileUpload():
    if 'photo' in request.files:
        photo = request.files['photo']
        val = request.files['val']
        if photo.filename != '':            
            # photo.save(os.path.join('C:/Temp', photo.filename))
            photo.save(os.path.join('C:/Temp',val + "_" + photo.filename ))
    return redirect(url_for('ul'))