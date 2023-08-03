# python3
# coding=<UTF-8>

from lxml import etree

from ..params_container import Container
from ..target import Target
from ..exceptions import EmptyPageException

__author__ = 'maria-terekhina'
__doc__ = \
'''
JuKuu: Chinese-English Subcorpus
================================

API for Chinese-English subcorpus of JuKuu corpus (http://www.jukuu.com/)

**Search Parameters**

query: str or list([str])
    query or queries (currently only exact search by word or phrase is available)
n_results: int, default 100
    number of results wanted (100 by default, also 100 is the maximum possible amount for this corpus)
kwic: bool, default True
    kwic format (True) or a sentence (False)
query_language: str
    language of the 'query'
    
Example
-------

.. code-block:: python

    corp = lingcorpora.Corpus('zho_eng')
    results = corp.search('语', n_results=10, query_language ='zho')
    for result in results:
        for i, target in enumerate(result):
            print(i+1, target.text)

.. parsed-literal::

    "语": 100%|██████████| 10/10 [00:01<00:00,  9.00docs/s]

    1  在现代图形用户界面中，这些原语包括指向、单击和拖动。 
    2  图13-3  图形用户界面易于使用的主要原因在于推行有限的交互词汇，由指向、单击和拖动这些极少量的原语组成复杂的习惯用法。 
    3  ((委婉语.古))妊娠,怀孕 
    4  避免用缩略语，如果必须，要用标准缩略语。 
    5  避免用缩略语，如果必须，要用标准缩略语。 
    6  "海底电报"一词是混合语,半为拉丁语,半为希腊语。 
    7  "海底电报"一词是混合语,半为拉丁语,半为希腊语。 
    8  "海底电报"一词是混合语,半为拉丁语,半为希腊语。 
    9  学习外国语切莫望文生义。 
    10  书面语比口语往往更加一致。 

'''

TEST_DATA = {'test_single_query': {'query': 'table', 'query_language': 'eng'},
             'test_multi_query': {'query': ['table', 'chair'], 'query_language': 'eng'}
             }


class PageParser(Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__seed = ''
        self.__temp = 'temptree.xml'
        self.__xpath = ".//*[@class='e'] | .//*[@class='c']"
        self.__dpp = 100
        self.__stop_flag = False
        self.__c_page = 0
        self.__targets_seen = 0

        self.__dom = 'http://www.jukuu.com/show-'
        self.__post = '%s-%d.html'

        if self.query_language is None:
            raise ValueError('Please specify "query_language" parameter')

    def __parse_docs(self, docs_tree, analyses=True):
        """
        a generator over documents tree
        """
        _text = str()
        _transl = str()
        _target_idxs = list()
        _ana = []
        _lang = str()
        _meta = str()
        lq = len(self.query)

        if self.query_language is 'zho':
            original = False
        else:
            original = True

        for el in docs_tree:
            if original:
                _text = "".join(el.getchildren()[1].itertext()).strip()

                for k, sym in enumerate(_text):
                    if _text[k:k + lq] == self.query:
                        _target_idxs.append((k, k + lq))

                original = False

            else:
                _transl = "".join(el.getchildren()[1].itertext()).strip()
                if el.attrib['class'] == 'e':
                    _lang = 'zho'
                else:
                    _lang = 'eng'
                original = True

            if _target_idxs and (_transl != str()):
                for ixs in _target_idxs:
                    yield _text, ixs, _meta, _ana, self.gr_tags, _transl, _lang
                _text = str()
                _transl = str()
                _target_idxs = list()

            else:
                continue

    def get_page(self):
        """
        return documents tree
        """
        params = (self.query,
                  self.__c_page)

        post = self.__post % (params)
        parser = etree.HTMLParser(recover=True)
        return etree.parse(self.__dom + post, parser=parser)

    def get_results(self):
        docs_tree = self.page.xpath(self.__xpath)

        if not docs_tree:
            raise EmptyPageException

        for doc in self.__parse_docs(docs_tree, analyses=self.get_analysis):
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

        while not self.__stop_flag:
            try:
                self.page = self.get_page()
                yield from self.get_results()

            except EmptyPageException:
                self.__stop_flag = True

            self.__c_page += 1

            if self.__c_page > 9:
                self.__stop_flag = True
                return
