# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn 
from firebase_admin import initialize_app
import pykakasi
from flask import jsonify
import json

initialize_app()

# Khởi tạo đối tượng Kakasi
kakasi = pykakasi.kakasi()

@https_fn.on_request()
def convert_tu_vung(req: https_fn.Request) -> https_fn.Response:
    data = req.get_json()
    if 'query' not in data:
        return jsonify({"error": "No query provided"}), 400
    
    query = data['query']
    
    result = kakasi.convert(query)

    hira_values = [entry['hira'] for entry in result]

    # Nối các giá trị 'hira' lại với nhau
    joined_hira = ''.join(hira_values)
    
    return https_fn.Response(json.dumps(result, ensure_ascii=False))
