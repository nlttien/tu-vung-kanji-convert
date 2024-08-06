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

response = requests.post(url, headers=headers, json=dataRequest)

def convert_to_string(data):
    # Lấy nghĩa của kanji theo thứ tự
    kanji_meanings = [result['mean'] for result in data['results']]
    
    kanji_meanings.reverse()

    # List comprehension để lấy phần đầu tiên của mỗi nghĩa
    first_meanings = [meaning.split(', ')[0] for meaning in kanji_meanings]

    # Nối các nghĩa lại thành một chuỗi và thêm dấu ngoặc 「」 vào đầu và cuối
    result_string = ' '.join(first_meanings)
    return f'「{result_string}」'

# Gọi hàm và in kết quả
if response.status_code == 200:
# In kết quả trả về
    print("Response JSON:",convert_to_string(response.json()) )
else:
    print("Failed to retrieve data:", response.status_code)