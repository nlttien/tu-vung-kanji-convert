# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn 
from firebase_admin import initialize_app
import pykakasi
from flask import jsonify
import json
import requests

url = 'https://mazii.net/api/search'

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'vi,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,ja;q=0.6',
    'Priority': 'u=1, i',
    'Sec-CH-UA': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
    'Sec-CH-UA-Mobile': '?0',
    'Sec-CH-UA-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    # 'Cookie': '...'  # Bạn có thể thêm cookie nếu cần
    'Referer': 'https://mazii.net/vi-VN/search',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
}

dataRequest = {
    "dict": "javi",
    "type": "kanji",
    "query": "勉強し",
    "page": 1
}

# Khởi tạo đối tượng Kakasi
kakasi = pykakasi.kakasi()

@https_fn.on_request()
def convert_tu_vung(req: https_fn.Request) -> https_fn.Response:
    data = req.get_json()
    if 'query' not in data:
        return jsonify({"error": "No query provided"}), 400
    
    query = data['query']
    dataRequest["query"] =  query
    response = requests.post(url, headers=headers, json=dataRequest)
    
    result = kakasi.convert(query)

    hira_values = [entry['hira'] for entry in result]
    
    # Nối các giá trị 'hira' lại với nhau
    joined_hira = ''.join(hira_values)
    
    if response.status_code == 200:
    # In kết quả trả về
        response_json = {
            "joined_hira": joined_hira,
            "converted_data": convert_to_string(response.json())
        }
    else:
        response_json = {
            "joined_hira": joined_hira
        }

    return https_fn.Response(json.dumps(response_json, ensure_ascii=False))

def convert_to_string(data):
    # Lấy nghĩa của kanji theo thứ tự
    kanji_meanings = [result['mean'] for result in data['results']]
    
    kanji_meanings.reverse()

    # List comprehension để lấy phần đầu tiên của mỗi nghĩa
    first_meanings = [meaning.split(', ')[0] for meaning in kanji_meanings]

    # Nối các nghĩa lại thành một chuỗi và thêm dấu ngoặc 「」 vào đầu và cuối
    result_string = ' '.join(first_meanings)
    return f'「{result_string}」'