import requests
from bs4 import BeautifulSoup
from ..params_container import Container
from ..target import Target
import re

TEST_DATA = {'test_single_query': {'query': 'kaster'},
             'test_multi_query': {'query': ['kaster', 'kanon']}
            }

__author__ = 'Filaona, kategerasimenko'
__doc__ = \
"""
Danish Corpus
=============

API for Danish corpus (https://ordnet.dk/korpusdk_en/concordance).

**Search Parameters**

query: str or list([str]):
    query or queries
n_results: int, default 100
    number of results wanted (100 by default)

Example
-------

.. code-block:: python

    corp = lingcorpora.Corpus('dan')
    results = corp.search('dansk', n_results=10)
    for result in results:
        for i, target in enumerate(result):
            print(i+1, target.text)

.. parsed-literal::

    "dansk": 100%|██████████| 10/10 [00:01<00:00,  9.08docs/s]

    1 om hvilke juridiske modeller, der overvejes for at få en dansk særordning med EF på plads. Forinden besøger den britiske premierminister,
    2 der også tilknyttes det amibtiøse fremstød for dansk film og højskolekultur. TV 2-medarbejderen, journalist Inger Marie Vennize forlader
    3 skriver Klaus Rifbjerg et sted i " Karakterbogen ". Heri har dansk litteraturs Store Bastian både ret og uret. Hans nye bog
    4 lønstigninger er de laveste i næsten 40 år. Det viser Dansk Arbejdsgiverforenings lønindikator for juli, august og september. På et år
    5 de næste dage, som kan blive uhyre dramatiske dage i dansk politik, skal løsningen forhandles på plads både udadtil og indadtil.
    6 der godkendes på et EF-topmøde og derefter gennemgår en dansk folkeafstemning, vil aldrig blive tilsidesat til fordel for andre traktat-bestemmelser,
    7 og om at uafhængige juridiske eksperter skal vurdere en dansk aftale. Baggrunden er forlydender om en dansk løsning, der ikke
    8 yderst populær vinder af sæsonens sidste klassiske dyst- Dansk Opdrætningsløb på Charlottenlund. Selv om travtalentet løb ud i fejl
    9 have udgivet alle Carl Barks' Disney-serier på dansk . Seneste skud på stammen er " Anders And slår alt ". Det
    10 der døde i 1964, i dobbeltversion, som det hun var: dansk teaters Madame. JEG citerer lige Mette Winge fra det udmærket

"""


class PageParser(Container):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.punc = re.compile("[.-\[\]:\";,!?']")
        self.__pagenum = 1
        self.__page = None
        self.__occurrences = 0
        self.__session = requests.Session()
        
    def get_first_page(self):
        params = {'query': '"' + self.query + '"',
                  'search': 'Search',
                  'tag': 'word'}
        response = self.__session.get('http://ordnet.dk/korpusdk_en/concordance/action', params=params)
        return response


    def get_page(self):
        params = {'page': self.__pagenum}
        page = requests.get('http://ordnet.dk/korpusdk_en/concordance/result/navigate',
                            params=params, cookies=self.__session.cookies)
        return page


    def extract_one_res(self,sen):
        left_part = ''
        right_part = ''
        for word in sen.select('.left-context-cell'):
           left_part = left_part + ' ' + word.select('a')[0].text
        for word in sen.select('.right-context-cell'):
            right_part = right_part + ' ' + word.select('a')[0].text
        center_part = ' '.join([m.a.text.strip() for m in sen.select('.conc_match')])
        left_part, right_part = left_part.strip(), right_part.strip()
        if self.punc.search(center_part[1:]) is not None:
            right_part = center_part[self.punc.search(center_part[1:]).start()+1:].strip() + ' ' + right_part
            center_part = center_part[0:self.punc.search(center_part[1:]).start()+1].strip()
        idx = (len(left_part) + 1, len(left_part) + 1 + len(center_part))
        text = left_part + ' ' + center_part + ' ' + right_part
        t = Target(text, idx, '', None)
        return t        
        
        
    def get_results_page(self):
        soup = BeautifulSoup(self.__page.text, 'lxml')
        if self.__pagenum == 1:
            occur = soup.select('.value')[0].text
            self.__occurrences = int(occur[(occur.find('of') + 2):(occur.find('occur'))].strip())
            if self.__occurrences > 49:
                self.__occurrences -= 1
        p = soup.select('.conc_table')[0]
        return p.select('tr[onmouseover]')


    def extract(self):
        n = 0
        self.__page = self.get_first_page()
        if self.__page.status_code == 200:
            results = self.get_results_page()
            final_total = min(self.n_results,self.__occurrences)
            num_page = final_total // 50 + 1
            while n < final_total and n < len(results):
                yield self.extract_one_res(results[n])
                n += 1
            for i in range(2, num_page + 1):
                r = 0
                self.__pagenum = i
                self.__page = self.get_page()
                results = self.get_results_page()
                while n < final_total and r < len(results):
                    yield self.extract_one_res(results[r])
                    n += 1
                    r += 1
        self.__session.close()
