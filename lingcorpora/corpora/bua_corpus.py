from .arkhangelskiy_corpora import PageParser

language = 'buryat'
results = 'http://web-corpora.net/BuryatCorpus/search/results.php'

TEST_DATA = {'test_single_query': {'query': 'хөөшхэ'},
             'test_multi_query': {'query': ['хөөшхэ', 'дурлаха']}
             }

__author__ = 'ustya-k'
__doc__ = \
"""
Buryat Сorpus
=============

API for Buryat corpus (http://web-corpora.net/BuryatCorpus/search/).
    
**Search Parameters**

query: str or list([str]):
    query or queries
n_results: int, default 100
    number of results wanted
kwic: bool, default True
    kwic format (True) or a sentence (False)
get_analysis: bool, default False
    tags shown (True) or not (False)

Example
-------

.. code-block:: python

    corp = lingcorpora.Corpus('bua')
    results = corp.search('хэлэн', n_results=10)
    for result in results:
        for i, target in enumerate(result):
            print(i+1, target.text)

.. parsed-literal::

    "хэлэн": 100%|██████████| 10/10 [00:02<00:00,  4.14docs/s]

    1 Фатэр гэжэ үгэ немец хэлэн дээрэ эсэгэ гэһэн үгэ юм, — гэжэ Насаг эсэгэдээ юундэшьеб дураа гутаад, уруу дуруу зогсоһон басагандаа ойлгуулаад, хүхюунээр энеэбхилбэ.— Немец хүбүүн!
    2 Али эжынгээ угаажа үгэхэдэнь, хатаажа байна гүт? — гэжэ магтаһан болиһон хоёрой хоорондо хэлэн асууба.— Эжымни хүндөөр үбшэлөөд, хэбтэридээ орошонхой.
    3 Мнацаканян окоп соогуур гүйн, унтажа байһан гурбанай хамсыһаа ябууд татажа:— Нүхэр лейтенант, танкнууд! — гэжэ мэгдүүгээр хэлэн һэрюулбэ.
    4 Младша сержант Насаг Бадараев, — гэжэ элидхэһэнэй һүүлдэ, аалиханаар хэлэн нэмэбэ. — Сэрэгшэд Абдулаев, Макаров байлдаанда алдалан унаа.
    5 Саад, яслида гансал ород хэлэн дээрэ хөөрэлдэнэ ха юм.
    6 Олоһон мүнгөөрөө хойто жэл Москва ошожо ерэхэбди, — гэжэ Сэпэлмаа һайрхуугаар хэлэн, шэмээгүй байдал таһалба.— Тиигэ, тиигэ.
    7 Насаг тэрээнһээ телеграммаяа абамсаараа, ямар нэгэ юумэ һанажа, шара нюдөөрөө ошо сасаруулан, энэрхы уриханаар энеэбхилээд:— Хүбүүн,«эсэгэ » гэжэ үгэ немец хэлэн дээрэ «Фатэр » гэнэ гүш? — гэжэ асууба.— Тиимэ...
    8 Амидыгаар баригты, — гэжэ немецкэ офицер өөрынгөө хэлэн дээрэ хашхаран байжа, солдадуудаа захирна.— Намайе амидыгаар барижа шадахагүйт.
    9 Юундэб гэхэдэ, Зэбзэмаагай хэлэн өөрынгөө хүзүү орёогоогүй, харин хэнтэг зан гаргаһан Балдан-Доржын хүзүү орёоһон болоно бшуу.
    10 Һанан хэлэн дуулахадам,
     

"""


class PageParser(PageParser):

    def __init__(self, *args, **kwargs):
        super().__init__(language, results, *args, **kwargs)
