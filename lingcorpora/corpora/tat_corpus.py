from .arkhangelskiy_corpora import PageParser

language = 'tatar'
results = 'http://web-corpora.net/TatarCorpus/search/results.php'

TEST_DATA = {'test_single_query': {'query': 'туган'},
             'test_multi_query': {'query': ['туган', 'мәхәббәт']}
             }

__author__ = 'ustya-k'
__doc__ = \
"""
Tatar Corpus
============

API for Tatar corpus (http://web-corpora.net/TatarCorpus/).
    
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

    corp = lingcorpora.Corpus('tat')
    results = corp.search('теле', n_results=10)
    for result in results:
        for i, target in enumerate(result):
            print(i+1, target.text)

.. parsed-literal::

    "теле": 100%|██████████| 10/10 [00:02<00:00,  4.85docs/s]

    1 Теле авызына бәйләнгән диярсең, ник бер сүз ката алсын.
    2 Гармун күреген шап итеп тарттырып куйгач, Касыймның теле ачылды.
    3 Теле йөрәгенә түгел, акылына буйсынырга тырышты.
    4 Колак очларына ут капкан Нәкыя терсәге белән егеткә төртеп алды:.Теле шушының.
    5 1939 елның көзендә читтән торып Мәскәү педагогика институтының рус теле һәм әдәбияты факультетына укырга керә.
    6 Соңыннан, Сталинабад(Дүшәмбе) шәһәренә күчеп, таҗиклар арасында яши башлагач, ул әлеге телдә дә матур гына аңлаша, институтта укыганда немец теле белән дә кызыксына.
    7 Кызганыч, бүген мәчетләргә урыс теле үтеп керә башлады.
    8 Бу легионда тәрҗемәче һәм немец теле укытучысы сыйфатында Фридрих Биддер хезмәт итә.
    9 шигырьләрендә дә җәмгыятьнең кешелексезлеген, иҗтимагый-сәяси вазгыятьне «эзоп» теле аша тасвирлау урын ала.  «
    10 «Хәзерге татар теле кириллицага нигезләнгән» дип әйтү дә логиканы боза.

"""


class PageParser(PageParser):

    def __init__(self, *args, **kwargs):
        super().__init__(language, results, *args, **kwargs)
