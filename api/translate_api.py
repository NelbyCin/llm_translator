from ExtractLanguage import extract_lines
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from doctranslate import translate_pdf
from doctranslate import translate_docx
from doctranslate import translate_txt
from StyleTranslation import text_style_transformation
import os

app = Flask(__name__)
CORS(app)

def load_config(config_file_path):
    # 从指定路径加载config.json文件
    with open(config_file_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
    return config_data


# 翻译函数
def translate(text, source_lang, target_lang,url_dict,api_key):
    base_url = url_dict['base_url']
    url = url_dict['url']
    split_style = target_lang.split("-")
    style = None
    if len(split_style) > 1:
        target_lang, style = split_style
    if source_lang != target_lang:
        refer_str = extract_lines(source_lang, target_lang)
        prompt = """You should translate [{src}] into [{trc}] based on the reference example.
        reference:{refer_str}
        translate this [{src}] sentence into [{trc}]:{text}
        You should only return the translation result.""".format(src=source_lang, trc=target_lang, refer_str=refer_str,
                                                                 text=text)
        # 定义请求头
        headers = {
            'Authorization': 'Bearer ' + api_key,  # 请替换为有效的Bearer令牌
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json'
        }
        # 定义请求体
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "safe_mode": False,
            'temperature': 0.0
        }

        # 发送POST请求
        response = requests.post(url, headers=headers, json=data)
        # 检查请求是否成功
        if response.status_code == 200:
            # 解析响应内容
            response_data = response.json()

            assistant_message = response_data['choices'][0]['message']['content']
        else:
            return f"请求失败，状态码: {response.status_code}"
    else:
        assistant_message = text
    if style is not None:
        assistant_message = text_style_transformation(base_url, api_key, assistant_message,style,target_lang)
    return {'from': source_lang, 'to': target_lang, 'trans_result': {'dst': assistant_message, 'src': text}}


@app.route('/translate', methods=['POST'])
def api_translate():
    data = request.get_json()
    text = data.get('text')
    source_lang = data.get('source_lang')
    target_lang = data.get('target_lang')
    model_name= data.get("model_name")
    config_data = load_config('config.json')
    if model_name == 'chatglm3':
        url_dict =  config_data['chatglm3'],
    elif model_name == 'chatglm4':
        url_dict =  config_data['chatglm4'],
    elif model_name == 'chatgpt':
        url_dict =  config_data['chatgpt'],
    else:
        url_dict = config_data['chatgpt'],
    if text and source_lang and target_lang:
        result = translate(text, source_lang, target_lang,url_dict,config_data['api_key'])
        return jsonify(result), 200
    else:
        return jsonify({"error": "缺少必要的参数"}), 400


@app.route('/doctranslate', methods=['POST'])
def doc_translate():
    data = request.form
    source_lang = data.get('source_lang')
    target_lang = data.get('target_lang')
    model_name = data.get('model_name')
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    # 如果用户没有选择文件，浏览器可能会提交一个空的字段
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 获取文件扩展名
    file_extension = file.filename.rsplit('.', 1)[1].lower()
    if file_extension not in ['pdf', 'docx', 'txt']:
        return jsonify({"error": "File type not allowed"}), 400
    else:
        file_path = 'static/input_file/' + file.filename
        file.save(file_path)
        output_file_path = 'NULL'
        if file_extension == 'pdf':
            output_file_path = translate_pdf(file_path, source_lang, target_lang,model_name)
        elif file_extension == 'docx':
            output_file_path = translate_docx(file_path, source_lang, target_lang,model_name)
        elif file_extension == 'txt':
            output_file_path = translate_txt(file_path, source_lang, target_lang,model_name)
        if output_file_path == "too large":
            return jsonify({"from": source_lang, "to": target_lang, "link": output_file_path}), 333
        else:
            return jsonify({"from": source_lang, "to": target_lang, "link": output_file_path}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
