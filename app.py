from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
from Evtx.Evtx import Evtx
from Evtx.Views import evtx_file_xml_view
import xmltodict
import json
import os
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/upload', methods=['POST'])
@swag_from({
    'tags': ['File Upload'],
    'description': 'Upload a .evtx file and get JSON output',
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'The .evtx file to be uploaded'
        }
    ],
    'responses': {
        200: {
            'description': 'The JSON representation of the .evtx file',
            'examples': {
                'application/json': {
                    'Log': {
                        'Event': 'Details'
                    }
                }
            }
        },
        400: {
            'description': 'Invalid file type or no file uploaded'
        },
        500: {
            'description': 'Internal server error'
        }
    }
})
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if not file.filename.endswith('.evtx'):
        return jsonify({"error": "Invalid file type. Only .evtx files are allowed."}), 400
    
    filename = secure_filename(file.filename)
    file.save(filename)

    try:
        with Evtx(filename) as evtx:
            xml_view = evtx_file_xml_view(evtx.get_file_header())
            xml_dict = xmltodict.parse(xml_view)
            json_data = json.dumps(xml_dict)
            return jsonify(json.loads(json_data))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
