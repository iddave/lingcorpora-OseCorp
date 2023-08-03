from .arkhangelskiy_corpora import PageParser

language = 'udmurt'
results = 'http://web-corpora.net/UdmurtCorpus/search/results.php'

TEST_DATA = {'test_single_query': {'query': 'кыл'},
             'test_multi_query': {'query': ['кыл', 'яра']}
             }

__author__ = 'ustya-k'
__doc__ = \
"""
Udmurt Сorpus
=============
    
API for Udmurt corpus (http://web-corpora.net/UdmurtCorpus/search/).
    
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

    corp = lingcorpora.Corpus('udm')
    results = corp.search('кыл', n_results=10)
    for result in results:
        for i, target in enumerate(result):
            print(i+1, target.text)

.. parsed-literal::

    "кыл": 100%|██████████| 10/10 [00:01<00:00,  5.64docs/s]

    1 Клубен кивалтӥсь Нина Анатольевна Кузнецова но паймемын.- Кинлы кулэ ни милям клубмы? - лулӟе со. - Юртэз колхозлэн, кыл кутӥсез - нокин но уг сюры.
    2 Отысь клубез радъян пумысен вераськон ёросысь вылӥ кивалтӥсьёсмылэн но кыл йылазы ялан берга.
    3 Номыр понна кыл уд кутӥськы.
    4 Калыкен одӥг кыл шедьтыны секыт ӧвӧл.
    5 Чеберлыко литератураез лыдӟыны ӧдъяй, озьы вераськонме волятӥ, кыл шыкысме узырмытӥ.
    6 Ву тудӟонэз пумитаны дасьлык понна нырысь ик кыл куто кар но ёрос кивалтӥсьёс.
    7 ЮЛИЯ ОЛЮНИНА УДМУРТ КУН УНИВЕРСИТЕТЫСЬ УДМУРТ ФИЛОЛОГИ ФАКУЛЬТЕТЫН ДЫШЕТСКИСЬ:«Чошатоно ке удмурт кылын, китай кыл со туж секыт ми понна, малы ке шуоно, отын портэм интонациосты соблюдать кароно.
    8 Со ваньмыз понна кыл кутыны уг кышка.
    9 Малы?- Туала арын туж модной кыл вань - кризис, - валэктэ Людмила Королёва. - Милемды но со шуккиз, лэся.
    10 А. Ф. Лесун кыл сётӥз коньдон но лэсьтӥськон пумысен Удмурт Элькунлэн Президентэныз пыр-поч кенешыны, ивортэ «Можгинские вести » газет.

"""


class PageParser(PageParser):

    def __init__(self, *args, **kwargs):
        super().__init__(language, results, *args, **kwargs)
