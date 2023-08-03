# python3
# coding=<UTF-8>

from lxml import html

from ..params_container import Container
from ..target import Target
from ..exceptions import EmptyPageException

__author__ = 'maria-terekhina'
__doc__ = \
"""
Polish-Russian Parallel Corpus
==============================

API for Polish-Russian Parallel Corpus (http://pol-ros.polon.uw.edu.pl/)
    
**Search Parameters**

query: str or list([str]):
    query or queries (currently only exact search by word or phrase is available)
n_results: int, default 100
    number of results wanted
kwic: bool, default True
    kwic format (True) or a sentence (False)
subcorpus: list
    subcorpus (all of the mentioned below by default).
    Valid: ['non-fiction', 'fiction<1945', 'fiction>1945', 'press', 'law', 'religious', 
            'russian', 'foreign', 'polish']

Example
-------

.. code-block:: python

    corp = lingcorpora.Corpus('rus_pol')
    results = corp.search('лягушка', n_results=10, query_language='rus')
    for result in results:
        for i, target in enumerate(result):
            print(i+1, target.transl.strip(), '\n', target.text.strip())
            
.. parsed-literal::

    "лягушка": 100%|██████████| 10/10 [00:00<00:00, 42.38docs/s]
            
    1 Na sąsiednią mogiłę wskoczyła wielka żaba. 
     На соседнюю могилу запрыгнула огромная лягушка.
    2 - Jasne, brekek - powiedziała żaba. 
     – Само собой, брекекек, – сказала лягушка.
    3 O mój Mowgli - bo będę cię odtąd nazywała Mowglim, czyli Żabą - nadejdzie czas, kiedy zapolujesz na Shere Khana, jak on dziś polował na ciebie! 
     Да, да, я назову тебя Маугли - лягушка... и когда-нибудь ты будешь охотиться на Шер Хана, как он охотился на тебя.
    4 Cóż złego może nam wyrządzić ta goła żaba? 
     Какой вред может принести нам безволосая лягушка?
    5 - W imieniu Mowgliego, czyli Żaby. 
     - Я Маугли-лягушка.
    6 Wziąłem go za rękę wprowadzając na ciemne schody, aby uchronić od uderzenia się o cośkolwiek. Wilgotny chłód tej ręki tak był przenikliwy i przykry, iż była chwila, żem chciał ją wypuścić z mych dłoni... i uciec. 
     Я повел его за руку по темной лестнице, чтобы он не стукнулся обо что-нибудь головой; рука была на ощупь такой влажной и холодной – совсем как лягушка! – что мне захотелось оттолкнуть ее и убежать.
     
"""


TEST_DATA = {'test_single_query': {'query': 'стул', 'query_language': 'rus'},
             'test_multi_query': {'query': ['стул', 'стол'], 'query_language': 'rus'}
            }


class PageParser(Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.subcorpus is None:
            self.subcorpus = ['1', '2', '3', '4', '5', '6', 'russian', 'foreign', 'polish']
        elif not isinstance(self.subcorpus, list):
            raise TypeError('This corpus is special: parameter subcorpus should be list type!')
        else:
            synon = {'non-fiction': '6',
                     'fiction<1945': '1',
                     'fiction>1945': '5',
                     'press': '2',
                     'law': '4',
                     'religious': '3'
                     }
            corpora = list()
            for i, corp in enumerate(self.subcorpus):
                if corp in synon:
                    corpora.append(synon[corp])
                elif corp in ['russian', 'foreign', 'polish']:
                    corpora.append(corp)
                else:
                    raise ValueError('Invalid subcorpus! Please choose from: \'non-fiction\', \'fiction<1945\',' +
                                     ' \'fiction>1945\', \'press\', \'law\', \'religious\',' +
                                     ' \'russian\', \'foreign\', \'polish\'.')
            self.subcorpus = corpora

        if self.query_language is None:
            raise ValueError('Please specify query language. It migth be \'rus\' or \'pol\'.')
        elif self.query_language is 'pol':
            self.query_language = 'pl'
        elif self.query_language is 'rus':
            self.query_language = 'ru'

        self.__dom = 'http://pol-ros.polon.uw.edu.pl/searchresults/searchw' + self.query_language + '.php?'
        self.__post = ''
        self.__stop_flag = False
        self.__c_page = 0
        self.__targets_seen = 0
        self.__xpath = '/html/body/table/tr'

    def get_page(self):
        """
        return documents tree
        """
        params = {'string' + self.query_language: self.query,
                  'limit' + self.query_language.title(): str(self.n_results)}

        for corpus in self.subcorpus:
            params[corpus] = 'on'

        for key in params:
            self.__post += key
            self.__post += '='
            self.__post += params[key]
            self.__post += '&'

        return html.parse(self.__dom + self.__post[:-1])

    def __parse_docs(self, tree):
        """
        a generator over documents tree
        """

        # iter over original-translation pairs
        for para in tree:
            cells = para.getchildren()

            _text = str()
            _transl = str()
            _idx = 0
            _target_idxs = list()
            _ana = None
            _lang = str()
            _meta = str()

            snip_ql = cells[1].getchildren()
            snip_tl = cells[2].getchildren()

            _meta = snip_ql[1].text + ', ' + snip_tl[1].text
            _text = snip_ql[0].text
            _transl = snip_tl[0].text

            _target_idxs.append([len(_text.split(self.query)[0]), len(_text.split(self.query)[0]) + len(self.query)])

            if self.query_language is 'ru':
                _lang = 'pol'
            else:
                _lang = 'rus'


            if _target_idxs:
                for i, ixs in enumerate(_target_idxs):
                    yield _text, ixs, _meta, _ana, self.gr_tags, _transl, _lang
            else:
                continue

    def get_results(self):
        """
        iterate over results and yield Target objects to extract() method
        """
        docs_tree = self.page.xpath(self.__xpath)

        if not docs_tree:
            raise EmptyPageException

        for doc in self.__parse_docs(docs_tree):
            self.__targets_seen += 1
            if self.__targets_seen <= self.n_results:
                yield Target(*doc)
            else:
                self.__stop_flag = True
                return

    def extract(self):
        """
        streamer to Query
        """
        try:
            self.page = self.get_page()
            yield from self.get_results()

        except EmptyPageException:
            self.__stop_flag = True
