from flask import Flask, render_template, request, jsonify, abort
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from Evtx.Evtx import Evtx
from Evtx.Views import evtx_file_xml_view


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'files'

class UploadFileForm(FlaskForm):
    file = FileField("File" , validators=[InputRequired()])
    submit = SubmitField("Uploaded File")

@app.route('/upload', methods=["GET","POST"])
@app.route('/', methods=["GET","POST"])

def upload():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data #First grab the file
        if allowed_file(file.filename):
            file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(file_path)
            
            #process the .evtx file to extract data
            json_data = process_evtx(file_path)
            return jsonify(json_data)  # Return the JSON response
        else:
            abort(400, description="Sorry, only Windows Event Log (.evtx) files are permitted")
    
    return render_template('index.html', form=form)

def allowed_file(filename):
    ALLOWED_EXT = ['evtx']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

def process_evtx(file_path):
    records = []
    with Evtx(file_path) as evtx:
        xml_string = evtx_file_xml_view(evtx.get_file_header())  # Get the XML representation
        # Parse the XML and extract relevant information 
        # For simplicity, storing it as a list of XML strings
        records.append(xml_string)
    return records  # Return the data to be JSONified


if __name__ == "__main__":
    app.run(debug=True)

