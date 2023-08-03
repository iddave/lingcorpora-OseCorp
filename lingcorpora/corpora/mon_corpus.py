from .arkhangelskiy_corpora import PageParser

language = 'mongolian'
results = 'http://web-corpora.net/MongolianCorpus/search/results.php'

TEST_DATA = {'test_single_query': {'query': 'муур'},
             'test_multi_query': {'query': ['муур', 'хайр']}
             }

__author__ = 'ustya-k'
__doc__ = \
"""
Mongolian Corpus
================

API for Mongolian corpus (http://web-corpora.net/MongolianCorpus/search/).
    
**Search Parameters**

query: str or list([str])
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

    corp = lingcorpora.Corpus('mon')
    results = corp.search('гээд', n_results=10)
    for result in results:
        for i, target in enumerate(result):
            print(i+1, target.text)

.. parsed-literal::

    "гээд": 100%|██████████| 10/10 [00:00<00:00, 89.05docs/s]

    1 .Гэлээ гээд өөр орох оронгүй дөч хүрч яваа Дагва жаргаж чадсангүй.
    2 , - Би ч азтай яваа юм байна гээд муухан инээмсэглэх аядав.
    3 \?Миний яаж шаналж,махаа идэж явсныг чи даанч мэдэхгүй л дээ гээд Дэнсмаагийн хоолой зангирч,нүүрээ дарав.
    4 . - Өө нээрэн,за алив баяр хүргэе гээд Хорлоог түүн тийш эргэхэд Мөнхцэцэг босч очин баруун хацраа өгч үнсүүлээд буцан ирж суудалдаа суун,
    5 .Гээд сүргийн эх тэр хөгшин нугарсангүй.
    6 - Хүү минь овоо болж билээ гээд Дагва санаа алдав.
    7 .Хариуд нь би юм дуугаралгүй байж чадсан боловч толгой маань донжгос гээд дохичихдог байгаа.
    8 .Бага дээр нь дарж ав гээд эмийн мөнгө өгсөн л дөө.
    9 . - Хандивлачихсан гээд учраа хэлбэл ухаан алдаад унаад өглөө.
    10 .Нийлчих байх гээд мордсон

"""


class PageParser(PageParser):

    def __init__(self, *args, **kwargs):
        super().__init__(language, results, *args, **kwargs)
