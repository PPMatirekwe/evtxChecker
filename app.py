from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import xmltodict
from evtx.Evtx import Evtx
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'files'

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "EVTX File Upload API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/upload', methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file and allowed_file(file.filename):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(file_path)

        try:
            json_data = process_evtx(file_path)
            return jsonify(json_data), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Only .evtx files are allowed"}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'evtx'

def process_evtx(file_path):
    with Evtx(file_path) as log:
        records = []
        for record in log.records():
            xml_data = record.xml()

            try:
                # Convert XML to a dictionary (JSON-compatible format)
                json_record = xmltodict.parse(xml_data)
                records.append(json_record)
            except Exception as e:
                # If there’s an error, include the original XML for debugging
                records.append({"error": "Invalid JSON data", "xml": xml_data})

    return records

@app.route('/static/swagger.json')
def send_swagger_json():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'swagger.json')

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
