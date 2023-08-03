from .arkhangelskiy_corpora import PageParser

language = 'kalmyk'
results = 'http://web-corpora.net/KalmykCorpus/search/results.php'

TEST_DATA = {'test_single_query': {'query': 'мис'},
             'test_multi_query': {'query': ['мис', 'бәәх']}
             }

__author__ = 'ustya-k'
__doc__ = \
"""
Kalmyk Corpus
=============

API for Kalmyk corpus (http://web-corpora.net/KalmykCorpus/search/).
    
**Search Parameters**


query: str or list([str])
    query or queries
n_results: int, default 100
    number of results wanted
kwic: bool, default True
    kwic format (True) or a sentence (False) (True by default)
get_analysis: bool, default False
    tags shown (True) or not (False)

Example
-------

.. code-block:: python

    corp = lingcorpora.Corpus('kal')
    results = corp.search('келн', n_results=10)
    for result in results:
        for i, target in enumerate(result):
            print(i+1, target.text)

.. parsed-literal::

    "келн": 100%|██████████| 10/10 [00:01<00:00,  6.95docs/s]

    1 Ашлад келхд, мана таңһчд «АПК-н делгрлт» гидг келн-улсин төсв күцәлһнә йовудыг мана бәәрн һардачнр болн орн-нутгин һардвр чигн өөдәнәр үнлснь маднд омг үүдәҗ, урмд өгчәхнь лавта.
    2 Келхд, энүнлә хамдан Цугәрәсән марафонд орлцсн Троицк гимназин сурһульч Санҗ Лиджигоряев таңһчин марһанд 1-ч орм, МОУ «СШ№ 4- келн-улсин гимназин» сурһульч Маргарита Ен 2-ч орм эзләд, Адьянас түрүлв.
    3 Һурвн долан хонгин эргцд чинртә марһан болҗах Элст балһсна, хальмг келн улсин тускар цуг тивмүдт келгдх.
    4 - «АПК-н делгрлт» гидг келн-улсин төсв селәнә эдл-ахун халхар көдлҗәх баһ наста специалистнриг гер-бүүрәр тетклһнә төр бас босхҗаналм.
    5 Элстүр ирхләнь Хальмг Таңһчин Толһач сәәхн час болн «Хальмг келн-әмтнә туульс» гидг дегтр белглв.
    6 Өдгә цагт теегт мал идшлүлҗ өсклһнә, һаха, шову, заһс өсклһнә таңһчин шишлң программс, АПК-н делгрлт» гидг келн-улсин һоллгч төсв бәәдл-җирһлд күцәмҗтәһәр тохрагдҗана.
    7 Хамгин түрүнд мал өсклһнә делгрлтиг, өдгә цагин некврлә ирлцҗәх селәнә эдл-ахун баһ бизнесиг, дөңцл эдл-ахусиг болн фермсиг дөңнлһн келн-улсин төсвин һол күслнь болҗана.
    8 Мана сурһульчнрла хамдан йовсн МОУ «СШ№ 4- келн-улсин гимназин» багш Светлана Андреевна Цебекован келсәр, мана күүкд йир сәәнәр медрлән үзүлв.
    9 Путина зааврар сурһуль-эрдм келн-улсин государственн төсвд орв.
    10 Хамгин түрүн нарт делкән чемпиона нер зүүҗәх шатрчнрла, ФИДЕ-н ханьд орҗах келн-улсин федерацсла күүндвр кегдәд нег хәләц дөң олв.

"""


class PageParser(PageParser):

    def __init__(self, *args, **kwargs):
        super().__init__(language, results, *args, **kwargs)
