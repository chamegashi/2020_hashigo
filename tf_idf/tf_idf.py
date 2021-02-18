import numpy as np

from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import POSStopFilter

from sklearn.feature_extraction.text import TfidfVectorizer

def change_sentence(sentence_list, sentence):
    sentence_list[0] = sentence
    return sentence_list

def make_tf(text):
    tokenizer = Tokenizer()
    token_filters = [POSStopFilter(['記号', '助詞', '助動詞', '動詞', '接続詞'])]
    analyzer = Analyzer(tokenizer=tokenizer, token_filters=token_filters)
    tokens = analyzer.analyze(text)

    word_list = []
    for t in tokens:
        for word in word_list:
            if(t.surface == list(word.keys())[0]):
                word[t.surface] = word[t.surface] + 1
                continue

        word_list.append({t.surface: 1})

    return word_list

def make_tf_idf_result(debug, input_sentence):

    # make 字句解析機
    tokenizer = Tokenizer()
    token_filters = [POSStopFilter(['記号', '助詞', '助動詞', '動詞', '接続詞'])]
    analyzer = Analyzer(tokenizer=tokenizer, token_filters=token_filters)

    # 名詞の抽出
    file_path = "./all_sentence/all_sentence_0.txt"
    sentence_list = []
    word_list = []

    with open(file_path, encoding='utf-8') as f:
        sentence_list = f.readlines()

    if(not debug):
        sentence_list = change_sentence(sentence_list, input_sentence)

    for i in range(0, 201):
        tokens = analyzer.analyze(sentence_list[i])
        sentences_tmp = []
        for t in tokens:
            sentences_tmp.append(t.surface)

        word_list.append(" ".join(sentences_tmp))

    # nparray 化
    np_word_list = np.array(word_list)

    # ベクトル化する機器生成
    vec_tfidf = TfidfVectorizer()

    # ベクトル化
    X = vec_tfidf.fit_transform(np_word_list)

    # tf-idf と 名詞 を辞書として処理
    set_word_and_tf_idf = {}
    words = vec_tfidf.get_feature_names()
    for i, vec in zip(range(0, 1), X.toarray()):
        for w_id, tfidf in sorted(enumerate(vec), key=lambda x: x[1], reverse=True):
            word = words[w_id]
            set_word_and_tf_idf[word] = tfidf

    result_list = []

    for key in set_word_and_tf_idf.keys():
        if(set_word_and_tf_idf[key] > 0):
            print(key + ": " + str(set_word_and_tf_idf[key]))
            result_list.append({key : set_word_and_tf_idf[key]})
        else:
            break

    return result_list


def wiki_tf_idf(word_list, idf):
    tf = []

    for word in word_list:

        if(len(tf) == 0):
            tf.append({word: 1})
            continue

        for tf_instance in tf:
            print(tf_instance)
            if(list(tf_instance.keys())[0] == word):
                tf[list(tf_instance.keys())[0]] = tf[list(tf_instance.keys())[0]] + 1
                continue

        tf.append({word: 1})

    print(tf)


    result_list = []

    return result_list

if __name__ == "__main__":
    # make_tf_idf_result(True, "")
    wiki_tf_idf(["abe", "ane", "ane", "abe", "a"], "")

# 出力
# print('Vocabulary size: {}'.format(len(vec_tfidf.vocabulary_)))
# print('Vocabulary content: {}'.format(vec_tfidf.vocabulary_))
# print(X.toarray())
