from ExtractLanguage import extract_lines
import requests
import os
import logging
import time
import nltk
from nltk.translate.bleu_score import corpus_bleu
from nltk.translate.bleu_score import SmoothingFunction

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def translate(text, source_lang, target_lang, file):
    api_key = 'fk226350-fK249RFhhXv7T2n3xZRcfCAofU6c7lf6'
    # url = 'https://oa.api2d.net/v1/chat/completions'
    url = 'http://10.244.197.144:6006/v1/chat/completions'
    refer_str = extract_lines(source_lang, target_lang)
    prompt = """You should translate [{src}] into [{trc}] based on the reference example.
           reference:{refer_str}
           translate this [{src}] sentence into [{trc}]:{text}
           You should only return the translation result.""".format(src=source_lang, trc=target_lang,
                                                                    refer_str=refer_str,
                                                                    text=text)
    # prompt = f"You should translate [{source_lang}] into [{target_lang}]\n" \
    #          f"translate this [{source_lang}] sentence into [{target_lang}]:{text}\n"\
    #          f"You should only return the translation result."
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
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

    retry_attempts = 10
    for attempt in range(retry_attempts):
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                response_data = response.json()
                assistant_message = response_data['choices'][0]['message']['content']
                with open(file, 'a', encoding='utf-8') as f:
                    f.write(assistant_message + '\n')
                logging.info(f"Translated: {text} -> {assistant_message}")
                return
            else:
                logging.warning(f"Failed to translate (status {response.status_code}): {text}")
        except requests.RequestException as e:
            logging.error(f"Client error: {e}")

        time.sleep(2 ** attempt)  # Exponential backoff

    logging.error(f"Failed to translate after {retry_attempts} attempts: {text}")


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


def translate_lines(src_lines, src, tgt, translate_file):
    for line in src_lines:
        translate(line, src, tgt, translate_file)


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

    return  bleu_scores


if __name__ == '__main__':
    score = Bleu('zh', 'en', 'zh-en-glm4-no.txt')
    print(f"BLEU score: {score}")
