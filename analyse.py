
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings. ӕз бинонты

import lingcorpora
import json

with open(r'attributes.json', 'r', encoding="utf-8") as j:
    json_data = json.load(j)

def Convert(str):
    list = str.split(',')
    new_list=[]
    new_list.append("Словарная форма: "+list[0])
    i = 0
    for tag in list:
        if tag in json_data:
            new_list.append(json_data[tag])
        i+=1

    return "\n".join(new_list)

#results = corp.search('ӕз', n_results=1, get_analysis = True)
def get_tags(word, lang):
    corp = lingcorpora.Corpus(lang)
    results = corp.search(word, n_results=1, get_analysis = True)
    for result in results:
        for i, target in enumerate(result):
            if target != False:
                for tok in target.analysis:
                        print(tok)
                        translation=""
                        if tok['transl'] != '': translation = '\nПеревод: '+ tok['transl']

                        yield Convert(tok['lemma']+','+tok['PoS'] +','+ tok['tag']) + translation

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
