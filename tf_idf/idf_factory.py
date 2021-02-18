import json
import pickle
import dbm

def eliminate_common_idf(eliminate_idf):

    save_words = []

    with open('wikipedia_idf.json', 'r', encoding='utf-8') as json_f:
        json_load = json.load(json_f)

        for v in json_load:
            if json_load[v] < eliminate_idf:
                save_words.append(json_load)
                if(len(save_words) > 4000):
                    break


    with open('eliminate_idf', 'wb') as f:
        pickle.dump(save_words, f)


def read_idf(input_words):

    input_words_sum = 0

    print(input_words)

    for word in input_words:
        input_words_sum = input_words_sum + list(word.values())[0]

    result_datas = []

    with open('eliminate_idf', 'rb') as json_f:

        # 4000
        load_list = pickle.load(json_f)
        now_list = 0

        # 3334158
        for load_data in load_list:
            for key in load_data.keys():
                now_data = 0
                for word in input_words:
                    if(key == list(word.keys())[0]):
                        print("done")
                        result_datas.append({key: (word[list(word.keys())[0]] / input_words_sum) * load_data[key]})
                        input_words.pop(now_data)

                    now_data = now_data + 1

            now_list = now_list + 1
            print(now_list)
            if(now_list >= 2):
                break

    print(result_datas)

    return [result_datas, 0.5/input_words_sum]

if __name__ == "__main__":
    # eliminate_common_idf(6.5)
    read_idf("")



