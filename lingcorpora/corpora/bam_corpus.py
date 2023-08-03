from ..params_container import Container
from requests import get
from bs4 import BeautifulSoup
from html import unescape
from ..target import Target

TEST_DATA = {'test_single_query': {'query': 'walasa'},
             'test_multi_query': {'query': ['walasa', 'yɔrɔ']}
            }

__author__ = 'kategerasimenko'
__doc__ = \
"""
Bamana Corpus
=============
    
API for Bamana corpus (http://maslinsky.spb.ru/bonito/index.html).
    
**Search Parameters**

query: str or list([str])
    query or queries (currently only exact search by word or phrase is available)
n_results: int, default 100
    number of results wanted
kwic: bool, default True
    kwic format (True) or a sentence (False)
get_analysis: bool, default False
    whether to collect grammatical tags for target word or not (False by default, available only for corbama-net-non-tonal subcorpus)
subcorpus: str, default 'corbama-net-non-tonal'
    subcorpus. Available options:
        * 'corbama-net-non-tonal'
        * 'corbama-net-tonal'
        * 'corbama-brut'
        * 'corbama-ud'

Example
-------

.. code-block:: python

    corp = lingcorpora.Corpus('bam')
    results = corp.search('kan', n_results=10)
    for result in results:
        for i, target in enumerate(result):
            print(i+1, target.text)

.. parsed-literal::

    "kan": 100%|██████████| 10/10 [00:00<00:00, 14.99docs/s]

    1 dennin in seginna dugu kɔnɔ ka segin dɔnkili in kan a ba ye , a yɛlɛmana ka kɛ warabilen ye ka taa kungo
    2 kɔni tɛ dɔnkili in da dɛ ! jula k' a ka yɛlɛn fali kan ka dɔnkili da , k' a tɛna yɛlɛma . julaw ko , ko fosi
    3 yɛlɛma . musokɔrɔba ye dɔnkili in da k' a to fali kan . a tilala dɔrɔn , a yɛlɛmana ka kɛ warabilen ye . a
    4 a kɛ , don dɔ la , surukuba yaalatɔ bɔra tonkun in kan , kungo kɔnɔ . a kabakoyara : « Ɛ , tonkun yɛrɛ ni
    5 y' o fɔ yɔrɔ min na , fɛn dɔ y' a ta k' a pɛrɛn a kɔ kan . surukuba foori ka wuli , k' a ɲɛkili filaw bɔ u
    6 la . u y' u gɛrɛ tonkun in na . sama ɲɛ datɔ bonbonsi kan , a y' i kanto : « Ɛ , tonkun yɛrɛ ni bonbonsi , a da n
    7 a y' o bɔ a da la yɔrɔ min , fɛn dɔ y' a ta k' a pɛrɛn a kɔ kan . biɲɛ dow turu kojugu a la , a dɔw bɔra a fan dɔ fɛ .
    8 . Ala tora a ka dɔnni na ka kɔngɔ ben dugu nin kan . kɔngɔba . ka dugu nin ɲɛni , ka dugumɔgɔw fasa ,
    9 sara . Ala fana y' o mɔgɔ sugu dan ka bila dugukolo kan . hali n' a ye fɛn sɔrɔ , hali n' a ye nafolo d' a ma , a
    10  nsiirin , nsiirin . n y' a bila den dɔ le kan . den nin ye sira deli a facɛ fɛ , k' a b' a fɛ ka taga

"""



class PageParser(Container):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if self.subcorpus is None:
            self.subcorpus = 'corbama-net-non-tonal'
        if self.kwic:
            self.__viewmode = 'kwic'
        else:
            self.__viewmode = 'sen'
            
        self.__page = None
        self.__pagenum = 1

        
    def get_results(self):
        params = {
            "corpname": self.subcorpus,
            "iquery": self.query,
            "fromp": self.__pagenum,
            "viewmode": self.__viewmode
        }
        """
        create a query url and get results for one page
        """
        r = get('http://maslinsky.spb.ru/bonito/run.cgi/first',params)
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
            self.n_results = min(int(soup.select('strong.add_commas')[0].text.replace(',','')),self.n_results)
        return res

        
    def extract_kws(self,kws):
        final_kws = []
        tags = []
        for kw in kws:
            text_kw = kw.select('span.nott')[0].text.strip()
            tag = kw.select('div.aline')
            tag = [x.text.strip() for x in tag if x.text.strip()]
            if self.get_analysis and self.subcorpus == 'corbama-net-non-tonal':
                tags.append({'lemma': tag[0], 'tag': tag[1], 'gloss': tag[2]})
            final_kws.append(text_kw)
        final_kws = ' '.join(final_kws)
        return final_kws, tags


    def parse_kwic_result(self,result):
        """
        find hit and its left and right contexts
        in the extracted row of table
        """
        lc = ' '.join([x.text.strip() for x in result.select('td.lc span.nott')])
        kws = result.select('td.kw div.token')
        final_kws,tags = self.extract_kws(kws)
        rc = ' '.join([x.text.strip() for x in result.select('td.rc span.nott')])
        
        idx = (len(lc) + 1, len(lc) + 1 + len(final_kws))
        text = lc + ' ' + final_kws + ' ' + rc
        t = Target(text,idx,'',tags)
        return t
 
 
    def parse_sen_result(self,result):
        sentence = result.select('td.par  ')[0]
        text = ''
        if self.subcorpus == 'corbama-net-non-tonal':
            for ch in sentence.children:
                if ch.name is not None:
                    if 'token' in ch['class']:
                        w = ch.select('span.nott')[0].text.strip()
                        text += w + ' '
                    elif ch.name == 'span':
                        kws = ch.select('div.token')
                        final_kws, tags = self.extract_kws(kws)
                        idx = (len(text),len(text)+len(final_kws))
                        text += final_kws + ' '
        else:
            lc = sentence.select('span.nott')[0].string.strip()
            rc = sentence.select('span.nott')[-1].string.strip()
            kws = sentence.select('div.token')
            final_kws, tags = self.extract_kws(kws)
            idx = (len(lc) + 1, len(lc) + 1 + len(final_kws))
            text = lc + ' ' + final_kws + ' ' + rc
        t = Target(text, idx, '', tags)
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
                if self.kwic:
                    yield self.parse_kwic_result(rows[r])
                else:
                    yield self.parse_sen_result(rows[r])
                n += 1
                r += 1
            self.__pagenum += 1
