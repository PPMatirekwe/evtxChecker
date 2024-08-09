from flask import Flask, render_template, request, jsonify, abort, send_from_directory
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'files'

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'  # Path to your swagger.json file
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "File Upload API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/upload', methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"])
def upload():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data  # First grab the file
        if allowed_file(file.filename):
            file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(file_path)
            
            # Process the .evtx file to extract data
            #json_data = process_evtx(file_path)
            return  "File uploaded"  # Return the JSON response
        else:
            abort(400, description="Sorry, only Windows Event Log (.evtx) files are permitted")
    
    return render_template('index.html', form=form)

def allowed_file(filename):
    ALLOWED_EXT = ['evtx']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT



# Serve the swagger.json file
@app.route('/static/swagger.json')
def send_swagger_json():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'swagger.json')

if __name__ == "__main__":
    app.run(debug=True)
