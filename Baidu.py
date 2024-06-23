# -*- coding: utf-8 -*-

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document

import requests
import random
import json
from hashlib import md5
import os
import nltk
from nltk.translate.bleu_score import corpus_bleu
from nltk.translate.bleu_score import SmoothingFunction
# Set your own appid/appkey.
appid = '20230511001673922'
appkey = '1BLSHILVMG6xO7VoQuLa'


def baidu_translate(text, from_lang, to_lang):
    # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`

    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    query = text

    # Generate salt and sign
    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    print(result)
    if result.get('error_code'):
        return ''
    else:
    # Show response
        return result['trans_result'][0]['dst']

language_file_dict = {
    'zh': 'flores101_dataset/devtest/zho_simpl.devtest',
    'en': 'flores101_dataset/devtest/eng.devtest',
    'spa': 'flores101_dataset/devtest/spa.devtest',
    'fra': 'flores101_dataset/devtest/fra.devtest',
    'de': 'flores101_dataset/devtest/deu.devtest',
    'ru': 'flores101_dataset/devtest/rus.devtest',
    'pt': 'flores101_dataset/devtest/por.devtest',
    'jp': 'flores101_dataset/devtest/jpn.devtest',
    'kor': 'flores101_dataset/devtest/kor.devtest',
    'it': 'flores101_dataset/devtest/ita.devtest',
}


def translate_lines(src_lines, src, tgt, file):
    translate_result = ""
    for line in src_lines:
        translate_result += baidu_translate(line, src, tgt)
        translate_result += '\n'
    with open(file, 'a', encoding='utf-8') as f:
        f.write(translate_result)


def Bleu(src, tgt, translate_file):
    if not os.path.exists(translate_file):
        src_lines = []
        with open(language_file_dict[src], "r", encoding='utf-8', errors='ignore') as file:
            for line in file:
                src_lines.append(line.strip())

        # Ensure the translation file is empty before starting
        with open(translate_file, 'w', encoding='utf-8') as file:
            file.write('')

        translate_lines(src_lines, src, tgt, translate_file)
    ref = open(language_file_dict[tgt], 'r', encoding='utf-8').read().splitlines()

    hyp = []
    with open(translate_file, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            hyp.append(line.strip())

    reference_lines = [ref.strip().split() for ref in ref]
    candidate_lines = [cand.strip().split() for cand in hyp]

    # 准备参考翻译和候选翻译的数据结构
    references = [[ref] for ref in reference_lines]  # corpus_bleu需要每个参考翻译是一个列表
    candidates = candidate_lines

    # 定义不同n-gram的权重
    weights = {
        'BLEU-1': (1.0, 0, 0, 0),
        'BLEU-2': (0.5, 0.5, 0, 0),
        'BLEU-3': (0.3333, 0.3333, 0.3333, 0),
        'BLEU-4': (0.25, 0.25, 0.25, 0.25)
    }

    # 计算不同n-gram的BLEU分数
    bleu_scores = []
    smoothie = SmoothingFunction().method1
    for key, weight in weights.items():
        bleu_score = corpus_bleu(references, candidates, weight, smoothing_function=smoothie)
        print(f"{key} Score: {bleu_score:.4f}")
        bleu_scores.append(bleu_score)

    return bleu_scores


if __name__ == '__main__':
    score = Bleu('zh', 'en', 'zh-en-baidu.txt')
    print(f"BLEU score: {score}")

