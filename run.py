# coding: utf-8

import os
from flask import Flask, render_template, request, jsonify
import subprocess
from tf_idf import tf_idf, idf_factory

class Node:
    def __init__(self, word, to_num, sentence_num): #コンストラクタ
        self.word = word #ノードが持つ文節
        self.to_num = to_num #ノードがもつ数値
        self.sentence_num = sentence_num # 文節番号
        self.divided = 0 # 切断値
        self.child = []
        self.left = None #左エッジ
        self.right = None #右エッジ

def insert(node1, node2):
    node1.child.append(node2)

def node_print(node):
    if(node.child != []):
        print("word: %s divided: %d, child:" % (node.word, node.divided))
        for child in node.child:
            print(child.word)
        for child in node.child:
            node_print(child)
    else:
        print("word: %s divided: %d" % (node.word, node.divided))

def set_divided(tree):
    ret_dictionary = {}
    tree.divided = 100

    ret_dictionary[tree.sentence_num] = tree.divided

    if(len(tree.child) == 0):
        pass
    elif(len(tree.child) == 1):
        tmp_dictionary = set_divided_tmp(ret_dictionary, tree.child[0], 100, tree.sentence_num, True)
        ret_dictionary.update(tmp_dictionary)
    else:
        for child in tree.child:
            tmp_dictionary = set_divided_tmp(ret_dictionary, child, 100, tree.sentence_num, False)
            ret_dictionary.update(tmp_dictionary)

    return ret_dictionary

def set_divided_tmp(ret_dictionary, node, divided, before_num, is_only):

    if(is_only):
        node.divided = divided
    else:
        if(abs(before_num - node.sentence_num) == 1):
            node.divided = divided - 2
        else:
            node.divided = divided - 1

    ret_dictionary[node.sentence_num] = node.divided

    if(len(node.child) == 0):
        pass
    elif(len(node.child) == 1):
        tmp_dictionary = set_divided_tmp(ret_dictionary, node.child[0], node.divided, node.sentence_num, True)
        ret_dictionary.update(tmp_dictionary)
    else:
        for child in node.child:
            tmp_dictionary = set_divided_tmp(ret_dictionary, child, node.divided, node.sentence_num, False)
            ret_dictionary.update(tmp_dictionary)

    return ret_dictionary

def escape_text(text):
    text = text.replace("\n", "")
    text = text.replace(" ", "")
    text = text.replace("　", "")
    text = text.replace("   ", "")
    return text

def make_word_list(cabocha_array):
    word_list = []
    word = ''
    to_sentence_number = 0
    accent_flag = False
    is_append = False
    length_array = []
    length = 0

    for cabocha in cabocha_array:
        for output in cabocha:
            print(output)

            if not (output):
                continue

            # accent pattern                
            if "固有名詞" in output:
                accent_flag = True

            if(output[0] == '*'):
                if(is_append):
                    if(to_sentence_number == -1):
                        accent_flag = True
                        length_array.append(length + 1)
                        length = -1

                    word_list.append([word, to_sentence_number, accent_flag])
                    word = ''
                    is_append = False
                    accent_flag = False
                    length = length + 1

                output_split = output.split(' ')
                to_sentence_number = int(output_split[2][:-1])

            elif(output == 'EOS'):
                break

            else:
                output_split = output.split('\t')
                word = word + output_split[0]
                is_append = True

    word_list.append([word, to_sentence_number, True])
    length_array.append(length)

    length_num = 0

    print(length_array)

    for word in word_list:
        if(word[1] == length_array[length_num] - 1):
            word[2] = True
        
        if(word[1] == -1):
            length_num = length_num + 1
        


    return word_list

def make_accent_array(text):
    text = escape_text(text)
    text_array = text.split('。')

    for array in text_array:
        array = array + "。"

    path = "./text.txt"
    result_array = []

    for text_data in text_array:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text_data)
            result = subprocess.Popen(['cabocha', 'text.txt', '-f1'], stdout=subprocess.PIPE)

        result = result.communicate()[0]
        result = result.decode('utf-8')
        output_list = result.split('\r\n')
        result_array.append(output_list)

    return make_word_list(result_array)


app = Flask(__name__, static_folder='./front/dist/static', template_folder='./front/dist/')

@app.route('/make_sentence', methods=["POST"])
def show():
    text = request.form["sentence"]
    max_words = int(request.form["max_words"])
    devide_num = int(request.form["devide_num"])

    # text 処理

    text = text.replace("\n", "")
    text = text.replace(" ", "")
    text = text.replace("　", "")
    text = text.replace("   ", "")

    path = "./text.txt"
    result = ''

    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

        result = subprocess.Popen(['cabocha', 'text.txt', '-f1'], stdout=subprocess.PIPE)

    result = result.communicate()[0]
    result = result.decode('utf-8')
    output_list = result.split('\r\n')

    word_list = []

    word = ''
    to_sentence_number = 0
    is_append = False

    for output in output_list:
        if not (output):
            continue
        if(output == 'EOS'):
            word_list.append([word, to_sentence_number])
            break
        if(output[0] == '*'):
            if(is_append):
                word_list.append([word, to_sentence_number])
                word = ''
                is_append = False

            output_split = output.split(' ')
            to_sentence_number = int(output_split[2][:-1])


        else:
            output_split = output.split('\t')
            word = word + output_split[0]
            is_append = True

    print_word_list = []
    print_word = ''
    word_nums = 0
    i = 0

    for word in word_list:
        effective_num = word[1] - i

        if(word[1] == -1):
            print_word = print_word + word[0]
            print_word_list.append(print_word)
            print_word = ''

        elif(effective_num > devide_num):
            if(word_nums > max_words):
                print_word_list.append(print_word)
                print_word = ''
                word_nums = 0

            print_word = print_word + word[0]
            word_nums = word_nums + 1

            print_word_list.append(print_word)
            print_word = ''
            word_nums = 0

        elif(effective_num <= devide_num):
            if(word_nums > max_words):
                print_word_list.append(print_word)
                print_word = ''
                word_nums = 0

            print_word = print_word + word[0]
            word_nums = word_nums + 1             

        i = i + 1

    return jsonify({"result":print_word_list})

@app.route('/make_tree_dev', methods=["POST"])
def make_tree_func_dev():
    text = request.form["sentence"]
    max_length = int(request.form["max_length"])
    tf_idf_flag = int(request.form["tf_idf"])

    # text 処理

    text = text.replace("\n", "")
    text = text.replace(" ", "")
    text = text.replace("　", "")
    text = text.replace("   ", "")

    # cabocha 処理

    path = "./text.txt"
    result = ''

    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

        result = subprocess.Popen(['cabocha', 'text.txt', '-f1'], stdout=subprocess.PIPE)

    result = result.communicate()[0]
    result = result.decode('utf-8')
    output_list = result.split('\r\n')

    word_list = []

    word = ''
    to_sentence_number = 0
    is_append = False

    for output in output_list:
        if not (output):
            continue
        if(output == 'EOS'):
            word_list.append([word, to_sentence_number])
            break
        if(output[0] == '*'):
            if(is_append):
                word_list.append([word, to_sentence_number])
                word = ''
                is_append = False

            output_split = output.split(' ')
            to_sentence_number = int(output_split[2][:-1])


        else:
            output_split = output.split('\t')
            word = word + output_split[0]
            is_append = True

    # 構文解析木作成

    wait_node_list = []
    now_number = 0

    for word in word_list:        # 最初のみ
        if(now_number == 0):
            wait_node_list.append(Node(word[0], word[1], now_number))
            now_number = now_number + 1
            continue

        this_node = Node(word[0], word[1], now_number)
        new_wait_node_list = []

        for node in wait_node_list:
            if(node.to_num == now_number):
                insert(this_node, node)
            else:
                new_wait_node_list.append(node)

        new_wait_node_list.append(this_node)
        wait_node_list = new_wait_node_list

        now_number = now_number + 1

    tree = wait_node_list[0]

    # 構文木探索で、切断値を代入し、dictionaly を製作

    divided_dictionaly = set_divided(tree)

    # LineWidthList 作成
    line_width_list = []
    line_incriment = 0
    for word in word_list:
        line_width_list.append({"word": word[0], "divided": divided_dictionaly[line_incriment]})
        line_incriment = line_incriment + 1

    # divided_dictionaly を基に並び替え

    print_index_word_list = []
    print_word_list = []
    print_stack_list = []
    insert_list = []
    print_word = ""
    now_length = 0

    for word in word_list:
        now_length = now_length + len(word[0])

        if(now_length < max_length):
            print_stack_list.append(word)
            print_word = print_word + word[0]
            continue

        if(now_length >= max_length):

            if(len(print_word) == 0):
                print_word_list.append(print_word)
                now_length = 0
                continue

            else:
                max_divided = 0
                divided_word = ""

                for stack_word in print_stack_list:
                    if(divided_dictionaly[stack_word[1]] >= max_divided):
                        max_divided = divided_dictionaly[stack_word[1]]
                        divided_word = stack_word[0]

                print_word = ""
                stack_print_word = ""
                is_dividied = False
                new_print_stack_list = []

                for stack_word in print_stack_list:

                    if(stack_word[0] != divided_word):
                        if(is_dividied):
                            new_print_stack_list.append(stack_word)
                            stack_print_word = stack_print_word + stack_word[0]
                        else:
                            insert_list.append(stack_word[0])
                            print_word = print_word + stack_word[0]

                    else:
                        insert_list.append(stack_word[0])
                        print_word = print_word + stack_word[0]
                        is_dividied = True

                print_word_list.append(print_word)
                print_word = stack_print_word

                print_index_word_list.append(insert_list)

                print_stack_list = new_print_stack_list
                print_stack_list.append(word)

                insert_list = []
                print_word = print_word + word[0]
                now_length = len(print_word)

    print_word_list.append(print_word)
    print_index_word_list.append([print_word])



    # make accest word list
    accent_array = make_accent_array(text)
    print_accent_word_list = []
    accent_num = 0

    # for word_array in print_index_word_list:
    #     word_list_tmp = []
    #     for word in word_array:
    #         if(accent_num == 0):
    #             accent_num = accent_num + 1
    #         print("word: %s accent_array: %s" % (word, accent_array[accent_num]))
    #         word_list_tmp.append({"word": word, "accent": accent_array[accent_num][2]})
    #         accent_num = accent_num + 1

    #     print_accent_word_list.append(word_list_tmp)

    tf_idf_result = []
    td_idf_num = 0

    if(tf_idf_flag):
        os.chdir("./tf_idf/")
        tf = tf_idf.make_tf(text)
        tf_idf_result_data = idf_factory.read_idf(tf)
        tf_idf_result = tf_idf_result_data[0]
        td_idf_num = tf_idf_result_data[1]
        os.chdir("../")

    tf_result = []
    accent = False

    for word_array in print_index_word_list:
        word_list_tmp = []
        for word in word_array:
            for tf_idf_dic in tf_idf_result:
                if(list(tf_idf_dic.keys())[0] in word and list(tf_idf_dic.values())[0] >= td_idf_num):
                    accent = True

            word_list_tmp.append({"word": word, "accent": accent})
            accent = False

        tf_result.append(word_list_tmp)

    # print(tf_result)

    return jsonify({"result":print_word_list, "vib_result":print_index_word_list, "accent_result": print_accent_word_list, 'tf_idf_result': tf_result, "width_array":line_width_list})

@app.route('/make_divided', methods=["POST"])
def makediviedOnry():
    text = request.form["sentence"]

    # text 処理

    text = text.replace("\n", "")
    text = text.replace(" ", "")
    text = text.replace("　", "")
    text = text.replace("   ", "")

    # cabocha 処理

    path = "./text.txt"
    result = ''

    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

        result = subprocess.Popen(['cabocha', 'text.txt', '-f1'], stdout=subprocess.PIPE)

    result = result.communicate()[0]
    result = result.decode('utf-8')
    output_list = result.split('\r\n')

    word_list = []

    word = ''
    to_sentence_number = 0
    is_append = False

    for output in output_list:
        if not (output):
            continue
        if(output == 'EOS'):
            word_list.append([word, to_sentence_number])
            break
        if(output[0] == '*'):
            if(is_append):
                word_list.append([word, to_sentence_number])
                word = ''
                is_append = False

            output_split = output.split(' ')
            to_sentence_number = int(output_split[2][:-1])


        else:
            output_split = output.split('\t')
            word = word + output_split[0]
            is_append = True

    # 構文解析木作成

    wait_node_list = []
    now_number = 0

    for word in word_list:        # 最初のみ
        if(now_number == 0):
            wait_node_list.append(Node(word[0], word[1], now_number))
            now_number = now_number + 1
            continue

        this_node = Node(word[0], word[1], now_number)
        new_wait_node_list = []

        for node in wait_node_list:
            if(node.to_num == now_number):
                insert(this_node, node)
            else:
                new_wait_node_list.append(node)

        new_wait_node_list.append(this_node)
        wait_node_list = new_wait_node_list

        now_number = now_number + 1

    tree = wait_node_list[0]

    # 構文木探索で、切断値を代入し、dictionaly を製作
    divided_dictionaly = set_divided(tree)

    # LineWidthList 作成
    line_width_list = []
    line_incriment = 0
    for word in word_list:
        line_width_list.append({"word": word[0], "divided": divided_dictionaly[line_incriment]})
        line_incriment = line_incriment + 1

    return jsonify({"result": line_width_list})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

@app.after_request
def after_request(response):
    # response.headers.add('Access-Control-Allow-Origin', 'https://0acd7f1602f3.ngrok.io')
    return response

if __name__ == "__main__":
    app.run(port=8080)
    # app.run(port=58533)
    
# ngrok http -host-header=rewrite localhost:58533
