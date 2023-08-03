from .arkhangelskiy_corpora import PageParser

language = 'yiddish'
results = 'http://web-corpora.net/YNC/search/results.php'

TEST_DATA = {'test_single_query': {'query': 'קאַץ'},
             'test_multi_query': {'query': ['קאַץ', 'ליבע']}
             }

__author__ = 'ustya-k'
__doc__ = \
"""
Modern Yiddish Corpus
=====================

API for Modern Yiddish corpus (http://web-corpora.net/YNC/search/).
    
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

    corp = lingcorpora.Corpus('yid')
    results = corp.search('zikh', n_results=10)
    for result in results:
        for i, target in enumerate(result):
            print(i+1, target.text, sep='\n')

.. parsed-literal::

    "zikh": 100%|██████████| 10/10 [00:01<00:00,  5.17docs/s]

    1
    דערנאָך הייבט ער זיך שטיל אויף און גייהט ווייטער מיט אַ שמייכעלע צוריק אין אַלקיריל אַריין; זי שטעלט זיך אויף, שטייהט אַ וויילע און קוקט איהם נאָך,׳ ביז ער פערמאַכט אונטער זיך דאָס טהירעל.
    2
    למך׳ל זיצט אין אַלקיריל ביי זיך.
    3
    אונטער׳ן ווענטיל שושקעט מען און מען סוד׳עט זיך; און אַ פערשטיקט געלעכטער הערט זיך, און די זעלנערקע האַלט עפיס איין דעם עולם: “מאָרגען”, זאָגט זי אַלץ־אין־איינעם, “מאָרגען!
    4
    ווייסט גנענדיל פין דעם אַלעס, זי מאַכט זיך יאָ, צי זי מאַכט זיך נישט דערפין, שווייגען שווייגט זי...
    5
    שלענדערט זיך די גרויסע גענענדיל איבער׳ן מאַרק, איבער די גאַסען...
    6
    עס געפֿינען זיך דאָ אויך ניט־יידישע פאמיליעס.
    7
    אַלע איינוווינער זיינען קרובימ צווישן זיך: פֿעטערס, מומעס, פלימעניקעס(צעם), שוועסטער־קינדער אד״גל, פארנעמען זיך מיט לאַנדווירטשאפֿט און אַ טייל מיט פֿורמאנעריי ווי אַ צוגאב, זיינען מקיים דעם “בזעת אפיך” אין די גאנצע הונדערט פראצענט.
    8
    פֿון מאיאנטעקס פֿון זיך, אַן דער דערלויבעניש פֿון דער מאכט.
    9
    ביי היינטיקן טאג, ווען עס זיינען אריבער שוין צען יאר זינט די קאלאניזירונג האָט זיך אנגעהויבן, קען מען שוין אונטערפירן אַ שטיקל סך־הכל.
    10
    וויל שוין גנענדיל מודה זיין אויפ׳ן אמת, זאָל זיין אַיין עק פון אָבקומעניש פאַר׳ן אָבנאַרען, צוליעב אַ נאַרישער בושה; עפענט זיך אָבער באותו הרגע אויף די טהיר, הערט זיך איהר

"""


class PageParser(PageParser):

    def __init__(self, *args, **kwargs):
        super().__init__(language, results, *args, **kwargs)
