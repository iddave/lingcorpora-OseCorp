from requests import get
from bs4 import BeautifulSoup
from ..params_container import Container
from html import unescape
from ..target import Target

TEST_DATA = {'test_single_query': {'query': 'kɔdɔ'},
             'test_multi_query': {'query': ['alu', 'kɔdɔ']}
            }

__author__ = 'kategerasimenko'
__doc__ = \
"""
Maninka Corpus
==============

API for Maninka corpus (http://maslinsky.spb.ru/emk/run.cgi/first_form).
    
**Search Parameters**

query: str or List([str])
    query or queries (currently only exact search by word or phrase is available).
n_results: int, default 100
    number of results wanted.
kwic: bool, default True
    kwic format (True) or a sentence (False).
subcorpus: str, default 'cormani-brut-lat'
    subcorpus. Available options:
        * 'cormani-brut-lat'
        * 'corbama-brut-nko'
writing_system: str
    writing system for examples.
    Available options:
        * 'nko',
        * 'latin'.
    Bug: only 'latin' for 'corbama-brut-nko' subcorpus.

Example
-------

.. code-block:: python

    corp = lingcorpora.Corpus('emk')
    results = corp.search('tuma bɛɛ', n_results=10, writing_system='latin', kwic=False)
    for result in results:
        for i, target in enumerate(result):
            print(i+1, target.text)

.. parsed-literal::

    "tuma bɛɛ": 100%|██████████| 10/10 [00:01<00:00,  9.62docs/s]
    
    1 14 alu tɛdɛ alu ladɛla alla tara kanma tuma bɛɛ .
    2 ‹ n ka faama ye n ɲɛ tuma bɛɛ .
    3 alu kan ko : « cɛ nin ye kuma juu fɔla yɔrɔ saniman nin ma tuma bɛɛ , ka kuma juu fɔ kela musa la sariya fanan ma .
    4 1 wo tuma , sɔli tɛdɛ faama isa la karandennu la ɲanamaya masilanna tuma bɛɛ .
    5 moso wo tɛdɛ koɲuma kɛla tuma bɛɛ ka fantannu dɛmɛn .
    6 a tɛdɛ yahudiya fantannu sɔla kosɛbɛ , ka alla tara tuma bɛɛ .
    7 17 kɔnin a tɛdɛ a jɛdɛ yidakala alu la tuma bɛɛ ala kewaliɲumalu fɛ .
    8 16 wo le dɔ , n ye n dɔjala tuma bɛɛ sa n kɔnɔgbɛyanɛn di to .
    9 wo le dɔ , a tɛdɛ pɔli kilila tuma bɛɛ ka bado kɛ a fɛ .
    10 29 n ye a fɛ le jusu wo ɲɔɔn ye kɛ alu bolo tuma bɛɛ ka silan n ɲɛ ka nna jamarililu bɛɛ latelen , sa alu ni alu kɔmɔɔlu bɛɛ di hɛrɛ sɔdɔn kadawu .

"""

class PageParser(Container):
    """
    TODO: 
    tackle emerging latin in nko subcorp
    view funcs (tags, context length)
    """
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if self.subcorpus is None:
            self.subcorpus = 'cormani-brut-lat'
        if self.writing_system is None or self.subcorpus.endswith(self.writing_system[:3]):
            self.writing_system = ''
        if self.kwic:
            self.__viewmode = 'kwic'
        else:
            self.__viewmode = 'sen'
            
        self.__page = None
        self.__pagenum = 1
        
 
    def get_results(self):
        """
        create a query url and get results for one page
        """
        params = {
            "corpname": self.subcorpus,
            "fromp": self.__pagenum,
            "viewmode": self.__viewmode,
            "attrs": self.writing_system,
            "ctxattrs": self.writing_system,
        }
        #params differ in case of multi-word query
        if len(self.query.split()) > 1:
            params['iquery'] = self.query
        else:
            params['iquery'] = ''
            params['word'] = self.query
            params['queryselector'] = 'wordrow'
        r = get('http://maslinsky.spb.ru/emk/run.cgi/first', params)
        return unescape(r.text)


    def parse_page(self):
        """
        find results (and total number of results) in the page code
        """
        soup = BeautifulSoup(self.__page, 'lxml')
        if soup.select('div#error'):
            return []
        res = soup.find('table')
        res = res.find_all('tr')
        if self.__pagenum == 1:
            self.n_results = min(int(soup.select('strong[data-num]')[0].text),self.n_results)
        return res      
        
   
    def parse_result(self,result):
        if self.kwic:
            lc = ' '.join([x.text.strip() for x in result.select('td.lc span.nott')]).strip()
            rc = ' '.join([x.text.strip() for x in result.select('td.rc span.nott')]).strip()
        else:
            lc = result.select('span.nott')[0].string.strip()
            rc = result.select('span.nott')[-1].string.strip()
        final_kws = result.select('div.token span.nott')[0].string.strip()
        idx = (len(lc) + 1, len(lc) + 1 + len(final_kws))
        text = lc + ' ' + final_kws + ' ' + rc
        t = Target(text.strip(), idx, '', None)
        return t

        
    def extract(self):
        n = 0
        while n < self.n_results:
            self.__page = self.get_results()
            rows = self.parse_page()
            if not rows:
                break
            r = 0
            while n < self.n_results and r < len(rows):
                yield self.parse_result(rows[r])
                n += 1
                r += 1
            self.__pagenum += 1
