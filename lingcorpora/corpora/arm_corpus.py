from .arkhangelskiy_corpora import PageParser

language = 'armenian1'
results = 'http://eanc.net/EANC/search/results.php'

TEST_DATA = {'test_single_query': {'query': 'նարդի'},
             'test_multi_query': {'query': ['նարդի', 'սիրով']}
             }

__author__ = 'ustya-k'
__doc__ = \
"""
Eastern Armenian Corpus
=======================
    
API for Eastern Armenian corpus (http://eanc.net).
    
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

    corp = lingcorpora.Corpus('arm')
    results = corp.search('նարդի', n_results=10)
    for result in results:
        for i, target in enumerate(result):
            print(i+1, target.text)

.. parsed-literal::

    "նարդի": 100%|██████████| 10/10 [00:08<00:00,  1.15docs/s]

    1 Միսս Ջեյնին խելքահան է արել օձի ճուտը, — մռլտաց Մուրադն ու փշրված վերադարձավ նարդի խաղացողների մոտ:
    2 Ծառի տակ փռված կարպետի վրա Սողոն ու Յապոնը նարդի էին խաղում:
    3 Էլ ո՞չ նարդի չխկացընել,
    4 Սիրում էր նաև թավլի, այսինքն նարդի խաղալ հորս հետ, ինձ հետ:
    5 Ժանդարմը գլխի շարժումով դռների առջև նստած տղամարդկանց ցույց տվեց, որ մեքենայական շարժումներով թզբեհ էին քաշում կամ նարդի խաղում:
    6 Կառքից իջնելով մոտեցան տներից մեկի անշուք մուտքին, որի առջև երկու հոգի նստած նարդի էին գցում և մերթ ընդ մերթ սուրճը փռթացնում:
    7 Նոր եկողներից մի քանիսն էլ նստելով մի փոքր հեռու՝ բերել տվին նարդի ու տամա և սկսեցին խաղալ:
    8 Կարդում էր առավելագույնը հինգ-վեց միապաղաղ նամակներ, գցում տոպրակի մեջ և գնում պարապությունից հորանջող ոստիկանների հետ սուրճ խմելու և նարդի խաղալու:
    9 — Այո, այո, «Հաղթանակ», և սա օրեցօր կզորանա, և մենք կազատագրվենք այս անբան խոսողներից, նարդի խաղացողներից, ֆուտբոլի շուրջը ժամերով վիճողներից:
    10 — Հայրիկը բակում է, նարդի է խաղում, ուզո՞ւմ, եք՝ կանչեմ:
"""


class PageParser(PageParser):

    def __init__(self, *args, **kwargs):
        super().__init__(language, results, *args, **kwargs)
