# python3
# coding=<UTF-8>

from lxml import etree
import urllib.request as ur

from ..params_container import Container
from ..target import Target
from ..exceptions import EmptyPageException

__author__ = 'akv17, maria-terekhina'
__doc__ = \
"""
National Corpus of Russian: Parallel Subcorpus
==============================================

API for parallel subcorpus of National Corpus of Russian (http://ruscorpora.ru/search-para-en.html)

**Search Parameters**

query: str or list([str]):
    query or queries (currently only exact search by word or phrase is available)
n_results: int, default 100
    number of results wanted
kwic: bool, default True
    kwic format (True) or a sentence (False)
get_analysis: bool, default False
    whether to collect grammatical tags for target word or not
subcorpus: str, default 'rus'
    subcorpus ('rus' - search query over all subcorpora).
    Valid: ['rus', 'eng', 'bel', 'bul', 'bua', 'esp', 'ita',
            'zho', 'lav', 'ger', 'pol', 'ukr',
            'fra', 'sve', 'est']
    query_language: str
        language of the 'query'

Example
-------

.. code-block:: python

    corp = lingcorpora.Corpus('rus_parallel')
    results = corp.search('авось', n_results=10, query_language='rus')
    for result in results:
        for i, target in enumerate(result):
            print(i+1, target.transl.strip(), '\n', target.text.strip())

.. parsed-literal::

    "авось": 100%|██████████| 10/10 [00:00<00:00, 20.01docs/s]

    1 — Un Russe, ça tient sur trois béquilles: “on sait jamais”, “on verra bien”, et “on s'en sortira toujours”. 
     – Русский человек крепок на трех сваях – «авось», «небось» и «как-нибудь».
    2 – Да ви кажа, не ми се вярва… – Порфирий Петрович махна с ръка. – И нищо няма да излезе от цялата работа Съвсем безнадежден случай… Но впрочем идете.    Може да извадите по-голям късмет от мен.    И позна. 
     – Я признаться уж не верю-с… – Порфирий Петрович махнул рукой. – Ничего мы тут не зацепим. Кругом одна безнадежность… А впрочем сходите.    Авось вам больше моего повезет.    И ведь как в воду смотрел.
    3 Руският злодей е пламенен и недалновиден, убива както дойде. 
     Русский злодей горяч и нерасчетлив, крушит на авось.
    4 Първо, престъплението се оказа все пак не европейско, а руско, стремглаво. 
     Во-первых, преступление все-таки оказалось не европейское, а русское, на авось.
    5 И сложете на всекиго номер.    Да се надяваме, че няма да ги объркаме.    Вече ги научих всички наизуст. 
     Да еще нумер каждому проставьте.    Ничего, авось не перепутаем-с.    Я их всех уж наизусть успел выучить.
    6 Nikt, rzecz jasna, nie zabroni waszej dostojności słać dalszych epistoł, kropla wszak drąży skałę, kto wie, może któryś z kardynałów wreszcie ulegnie, może wreszcie mnie odwołają? 
     Никто, естественно, не запретит вашей милости кропать новые эпистолы, ибо капля камень точит, как знать, авось кто-нибудь из кардиналов наконец поддастся, возможно, меня наконец отзовут.
    7 Становішча яго, канешне, было зусім ахавае, хаця ў глыбіні сьвядомасьці ўсё ж таілася маленькая спадзёўка.    На авось ці, можа, на цуд.    Калі іншага не было, звычайна спадзяваліся на цуд, мабыць, так было заўжды. 
     Положение его, конечно, аховое, но в глубине сознания все-таки теплилась маленькая надежда.    На авось или, может, на чудо.    Когда другого не находилось, обычно полагались на чудо, так было всегда.
    8 Становішча яго, канешне, было зусім ахавае, хаця ў глыбіні сьвядомасьці ўсё ж таілася маленькая спадзёўка.    На авось ці, можа, на цуд.    Калі іншага не было, звычайна спадзяваліся на цуд, мабыць, так было заўжды. 
     Положение его, конечно, аховое, но в глубине сознания все-таки теплилась маленькая надежда.    На авось или, может, на чудо.    Когда другого не находилось, обычно полагались на чудо, так было всегда.
    9 Цуд, вядома, памагаў рэдка, болей падводзіў, асабліва атэістаў-бальшавікоў, якія, быццам не ведаючы таго, цяпер так дружна рушылі да хрысьціянскіх цудаў.    Авось паможа!    Калі памаліцца Богу, абразам, паклікаць царкоўных іерархаў на шматлюдныя прапагандовыя шоу. 
     Чудо, конечно, выручало редко, больше подводило, особенно атеистов-большевиков, которые теперь так дружно стали взывать к христианскому чуду.    Авось выручит!    ―
    10 Цуд, вядома, памагаў рэдка, болей падводзіў, асабліва атэістаў-бальшавікоў, якія, быццам не ведаючы таго, цяпер так дружна рушылі да хрысьціянскіх цудаў.    Авось паможа!    Калі памаліцца Богу, абразам, паклікаць царкоўных іерархаў на шматлюдныя прапагандовыя шоу. 
     Чудо, конечно, выручало редко, больше подводило, особенно атеистов-большевиков, которые теперь так дружно стали взывать к христианскому чуду.    Авось выручит!    ―

"""


TEST_DATA = {'test_single_query': {'query': 'стул', 'query_language': 'rus'},
             'test_multi_query': {'query': ['стол', 'стул'], 'query_language': 'rus'}
            }


class PageParser(Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.subcorpus is None:
            self.subcorpus = 'rus'

        if self.query_language is None:
            raise ValueError('Please specify query language')

        self.__seed = ''
        self.__temp = 'temptree.xml'
        self.__xpath = '/page/searchresult/body/result/document'
        self.__dpp = 100
        self.__stop_flag = False
        self.__c_page = 0
        self.__targets_seen = 0
            
        self.__dom = 'http://search1.ruscorpora.ru/dump.xml?'
        self.__post = 'mycorp=%s&text=%s&mode=%s&sort=%s&env=%s&req=%s&p=%s'

    def __get_ana(self, word):
        _ana = dict()
        for ana in word.findall('ana'):
            # iter over values of current ana of target (lex, sem, m, ...)
            for ana_type in ana.findall('el'):
                _ana[ana_type.attrib['name']] = [x.text for x in ana_type.findall('el-group/el-atom')]
        return _ana
    
    @staticmethod
    def _sqeeze_indexes(indexes):
        new_indexes = []
        ind = 0
        to_squeeze = []
        to_squeeze.append([])
        for i, index in enumerate(indexes):
            if not i+1 == len(indexes):
                if index[1] + 1 == indexes[i+1][0]:
                    if not index in to_squeeze:
                        to_squeeze[-1].append(index)
                    if not indexes[i+1][0] in to_squeeze:
                        to_squeeze[-1].append(indexes[i+1])
                else:
                    if not index in [ind[-1] for ind in to_squeeze if ind]:
                        new_indexes.append(index)
                        to_squeeze.append([])
            else:
                if not index in [ind[-1] for ind in to_squeeze if ind]:
                    new_indexes.append(index)
        to_squeeze.sort()
        for sq in to_squeeze:
            if sq:
                new_indexes.append([sq[0][0], sq[-1][1]])
        new_indexes.sort()
        return new_indexes

    def __parse_docs(self, docs, ql, analyses=True):
            """
            a generator over documents tree
            """
            # iter over docs
            for i, doc in enumerate(docs):
                _meta = doc.attrib['title']

                # iter over pairs in *doc*
                for para in doc.getchildren()[1:]:
                    _text = str()
                    _transl = str()
                    _idx = 0
                    _target_idxs = list()
                    _ana = list()
                    _lang = str()

                    # iter over examples in *para*
                    for snip in para.getchildren():
                        # iter over words in cur example
                        for word in snip.getchildren():
                            if word.tag == 'text':

                                if snip.attrib['language'] == ql[:-1]:
                                    _text += word.text
                                    _idx += len(word.text)
                                else:
                                    _transl += word.text

                                if snip.attrib['language'] != 'ru':
                                    _lang = snip.attrib['language']

                            if len(word.attrib) > 0:
                                # process target
                                if word.attrib.get('target') is not None:
                                    _target_idxs.append((_idx, _idx + len(word.attrib['text'])))
                                    if analyses:
                                        _ana.append(self.__get_ana(word))

                                if snip.attrib['language'] == ql[:-1]:
                                    _text += word.attrib['text']
                                    _idx += len(word.attrib['text'])
                                else:
                                    _transl += word.attrib['text']

                                if snip.attrib['language'] != 'ru':
                                    _lang = snip.attrib['language']
                    
                    _target_idxs = self._sqeeze_indexes(list(map(list, _target_idxs)))
                    if _target_idxs:
                        for i, ixs in enumerate(_target_idxs):
                            if analyses:
                                yield _text, ixs, _meta, _ana[i], self.gr_tags, _transl, _lang
                            else:
                                yield _text, ixs, _meta, _ana, self.gr_tags, _transl, _lang
                    else:
                        continue
        
    def get_page(self):
        """
        return documents tree
        """
        params = ('%28lang%3A%22'+self.subcorpus+'%22+%7C+lang_trans%3A%22'+self.subcorpus+'%22%29',
                  'lexform',
                  'para',
                  'gr_tagging',
                  'alpha',
                  ur.quote(self.query),
                  self.__c_page)

        post = self.__post % (params)
        return etree.parse(self.__dom + post)

    def get_results(self):
        docs_tree = self.page.xpath(self.__xpath)

        if not docs_tree:
            raise EmptyPageException
    
        for doc in self.__parse_docs(docs_tree, self.query_language, analyses=self.get_analysis):
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
