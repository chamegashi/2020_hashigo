import os, time
from selenium import webdriver

driver = webdriver.Firefox()

default_path = "https://sitesearch.asahi.com/.cgi/sitesearch/sitesearch.pl?Keywords=%E6%94%BF%E6%B2%BB"
article_num = 0
file_num = 0

# 取得

for i in range(0, 1001):

    text = ""

    if(i == 0):
        driver.get("https://sitesearch.asahi.com/.cgi/sitesearch/sitesearch.pl?Keywords=%E6%94%BF%E6%B2%BB")
    else:
        driver.get("https://sitesearch.asahi.com/.cgi/sitesearch/sitesearch.pl?Keywords=%E6%94%BF%E6%B2%BB" + "&start=" + str(article_num))

    a_tag = driver.find_elements_by_class_name('read')


    for a in a_tag:
        text = text + a.text + '\n'

    file_path = './all_sentence/all_sentence_' + str(file_num) + '.txt'

    with open(file_path, mode='a', encoding='utf-8') as f:
        f.write(text)


    print("INFO: finish to read " + str(article_num) + " to " + str(article_num + 20) + " article")
    article_num = article_num + 20

    if(i % 100 == 0 and i != 0):
        print("INFO: update the file num " + str(file_num) + " to " + str(file_num + 1) + " article")
        file_num = file_num + 1


    time.sleep(1)





driver.close()
