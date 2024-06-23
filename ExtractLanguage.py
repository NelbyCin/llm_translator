import random


def extract_lines(src,tgt,evaluate=False):
    if evaluate:
        language_file_dict = {
            'zh': ['flores101_dataset/dev/zho_simpl.dev'],
            'zh(trad)': ['flores101_dataset/dev/zho_trad.dev'],
            'en': ['flores101_dataset/dev/eng.dev'],
            'spa': ['flores101_dataset/dev/spa.dev'],
            'fra': ['flores101_dataset/dev/fra.dev'],
            'de': ['flores101_dataset/dev/deu.dev'],
            'ru': ['flores101_dataset/dev/rus.dev'],
            'pt': ['flores101_dataset/dev/por.dev'],
            'jp': ['flores101_dataset/dev/jpn.dev'],
            'kor': ['flores101_dataset/dev/kor.dev'],
            'it': ['flores101_dataset/dev/ita.dev']
        }
    else:
        # 根据翻译，获取数据集索引目录
        language_file_dict = {
            'zh': ['flores101_dataset/dev/zho_simpl.dev', 'flores101_dataset/devtest/zho_simpl.devtest'],
            'zh(trad)': ['flores101_dataset/dev/zho_trad.dev', 'flores101_dataset/devtest/zho_trad.devtest'],
            'en': ['flores101_dataset/dev/eng.dev', 'flores101_dataset/devtest/eng.devtest'],
            'spa': ['flores101_dataset/dev/spa.dev', 'flores101_dataset/devtest/spa.devtest'],
            'fra': ['flores101_dataset/dev/fra.dev', 'flores101_dataset/devtest/fra.devtest'],
            'de': ['flores101_dataset/dev/deu.dev', 'flores101_dataset/devtest/deu.devtest'],
            'ru': ['flores101_dataset/dev/rus.dev', 'flores101_dataset/devtest/rus.devtest'],
            'pt': ['flores101_dataset/dev/por.dev', 'flores101_dataset/devtest/por.devtest'],
            'jp': ['flores101_dataset/dev/jpn.dev', 'flores101_dataset/devtest/jpn.devtest'],
            'kor': ['flores101_dataset/dev/kor.dev', 'flores101_dataset/devtest/kor.devtest'],
            'it': ['flores101_dataset/dev/ita.dev', 'flores101_dataset/devtest/ita.devtest']
        }
    # 按行加载数据，不同语言之间每行对应相同翻译的句子
    src_lines = []
    for file in language_file_dict[src]:
        with open(file, "r", encoding='utf-8') as f:
            src_lines += f.readlines()
    tgt_lines = []
    for file in language_file_dict[tgt]:
        with open(file, "r", encoding='utf-8') as f:
            tgt_lines += f.readlines()

    # 随机选取 8 * 2 行句子，对应相同索引（对应翻译）
    selected_indices = random.sample(range(len(src_lines)), 8)
    selected_src_lines = [src_lines[i] for i in selected_indices]
    selected_tgt_lines = [tgt_lines[i] for i in selected_indices]

    # 去除换行符
    def remove_newlines(lines):
        return [line.replace("\n", "") for line in lines]

    selected_src_lines = remove_newlines(selected_src_lines)
    selected_tgt_lines = remove_newlines(selected_tgt_lines)
    # 构造reference字符串<x>=<y>
    refer_str = ''
    for x,y in zip(selected_src_lines,selected_tgt_lines):
        refer_str += "'"+x+"'="+"'"+y+"'"
    return refer_str


if __name__ == '__main__':
    refer_str = extract_lines('zh(smp)', 'en')
    print(refer_str)
