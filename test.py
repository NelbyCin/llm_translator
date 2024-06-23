import numpy as np
from sklearn.feature_extraction.text import CountVectorizer


def calculate_similarity(text1, text2):
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])
    similarity = np.dot(vectors[0], vectors[1]) / (np.linalg.norm(vectors[0]) * np.linalg.norm(vectors[1]))
    return similarity


def find_lowest_similarity(file1, file2):
    with open(file1, 'r',encoding='utf-8') as f1, open(file2, 'r',encoding='utf-8') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

        min_similarity = 1
        min_index = None

        for i in range(len(lines2)):
            similarity = calculate_similarity(lines1[i].strip(), lines2[i].strip())
            if similarity < min_similarity:
                min_similarity = similarity
                min_index = i

        return min_index, min_similarity


# 使用示例
file1 = "en-zh.txt"
file2 = "en-zh-no.txt"
index, similarity = find_lowest_similarity(file1, file2)
print(f"相似度最低的行: {index}")
print(f"相似度: {similarity}")
