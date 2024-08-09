from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
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
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
            #then save the file
            return "File has been uploaded"
        else:
            return "Sorry only Windows log files permitted"
    return render_template('index.html', form=form)

def allowed_file(filename):
    ALLOWED_EXT = ['evtx']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

if __name__ == "__main__":
    app.run(debug=True)

