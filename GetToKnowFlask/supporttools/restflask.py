from flask import Flask, render_template, request, redirect, flash
from flask_restful import Resource, Api
from scripts import Worklogs, Userimport, Groupimport
from werkzeug import secure_filename
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
api = Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# This is called to check if the file is valid based on the ALLOWED_EXTENSIONS
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')

# POST: Endpoint called by the form on import.html/importwithresponse.html once the user hits Submit
@app.route('/import-users', methods=['GET', 'POST'])
def imports():
    if request.method == 'POST':

        # Checks whether file was sent
        if 'csvfile' not in request.files:
            return 'Please, upload a file.'
            return redirect(request.url)

        INSTANCE = request.form['iname']
        EMAIL = request.form['email']
        PASSWORD = request.form['pass']
        file = request.files['csvfile']

        if file.filename == '':
            return 'No selected file'
            return redirect(request.url)

        # Checker whether file is within allowed extensions
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Saves file
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Instantiating object of Userimport and calling userImport method, which runs the script
        userimport = Userimport()
        user_import = userimport.userImport(os.path.join(app.config['UPLOAD_FOLDER'], filename), INSTANCE, EMAIL, PASSWORD)

        # It deletes the file as it's no longer used
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        # Render template sending the data along
        return render_template('importwithresponse.html', userimport=user_import)

    elif request.method == 'GET':
        return render_template('import.html')

# POST: Endpoint called by the form on importgroups.html once the user hits Submit
@app.route('/import-groups', methods=['GET', 'POST'])
def import_groups():
    if request.method == 'POST':

        # Checks whether file was sent
        if 'csvfile' not in request.files:
            return 'Please, upload a file.'
            return redirect(request.url)

        INSTANCE = request.form['iname']
        EMAIL = request.form['email']
        PASSWORD = request.form['pass']
        file = request.files['csvfile']

        if file.filename == '':
            return 'No selected file'
            return redirect(request.url)

        # Checker whether file is within allowed extensions
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Saves file
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Instantiating object of Groupimport and calling groupImport method, which runs the script
        groupimport = Groupimport()
        group_import = groupimport.groupImport(os.path.join(app.config['UPLOAD_FOLDER'], filename), INSTANCE, EMAIL, PASSWORD)

        # It deletes the file as it's no longer used at this point
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        # Render template sending the data along
        return render_template('importgroupswithresponse.html', groupimport=group_import)

    elif request.method == 'GET':
        return render_template('importgroups.html')

@app.route('/worklogs', methods=['GET', 'POST'])
def worklogs():

    if request.method == 'GET':
        return render_template('worklogs.html')

    elif request.method == 'POST':
        INSTANCE = request.form['iname']
        EMAIL = request.form['email']
        PASSWORD = request.form['pass']
        ISSUE_KEY = request.form['issue']
        WORK_HOURS = request.form['work_hours']

        worklog_obj = Worklogs()
        status_code, time_tracking, worklog_obj2 = worklog_obj.getWorklogs(INSTANCE, EMAIL, PASSWORD, ISSUE_KEY, WORK_HOURS)

        # If time_tracking is ZERO, it means that it didn't get into the FOR loop on Worklogs.py, which means that no worklog object was found.
        if time_tracking == 0:
            error = "No worklogs found for "+ISSUE_KEY
            return render_template('worklogswithresponse.html', error_message=error)

        elif status_code == 200:
            return render_template('worklogswithresponse.html', worklogs=worklog_obj2, status=status_code, timetracking=time_tracking)

        else:
            error = "Something bad happened!"
            return render_template('worklogswithresponse.html', status=status_code, error_message=error)

if __name__ == '__main__':
    app.run(debug=True)

# FLASK_APP=restflask.py flask run --host=0.0.0.0