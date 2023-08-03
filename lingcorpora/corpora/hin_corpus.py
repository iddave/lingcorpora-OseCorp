from ..params_container import Container
from ..target import Target
from requests import get
from bs4 import BeautifulSoup
import re

# has errors exporting results with words with diacritics on the end

TEST_DATA = {'test_single_query': {'query': 'कुत्ते'},
             'test_multi_query': {'query': ['कुत्ते', 'हाय']}
            }

__author__ = 'zu-ann, ustya-k'
__doc__ = \
"""
Hindi Corpus
============

API for Hindi corpus (http://www.cfilt.iitb.ac.in/~corpus/hindi/find.php).
    
**Search Parameters**

query: str or list([str])
    query or queries
n_results: int, default 100
    number of results wanted
kwic: bool, default True
    kwic format (True) or a sentence (False)
start: int, default 0
    index of the first query appearance to be shown (0 by default)

Example
-------

.. code-block:: python

    corp = lingcorpora.Corpus('hin')
    results = corp.search('कुत्ते', n_results=10)
    for result in results:
        for i, target in enumerate(result):
            print(i+1, target.text)

.. parsed-literal::

    "कुत्ते": 100%|██████████| 10/10 [00:10<00:00,  1.07s/docs]

    1  फिर उससे इस वाइरस का टीका तैयार किया. इस टीके को आपने एक स्वस्थ  कुत्ते  की देह में पहुँचाया.
    2  उस बच्चे को दो दिन पहले एक पागल  कुत्ते  ने काटा था. पागल 
    3   कुत्ते  दिखाई दिये .पालतू भी नहीं . बिल्ली और पक्षी भी नहीं .
    4  किसी दूसरे प्राणों के रहते भूत नहीं आता है . हम लोगों के घर मेए दो महीने का एक  कुत्ते  का बच्चा था .
    5   कुत्ते  का बच्चा गोद में ही सो गया . पढ़ते-पढ़ते यह अन्दाज ही नहीं रहा कि कब सबेरा हो गया .
    6   कुत्ते  का बच्चा मिल नहीं रहा है . समुचे मकान को रत्ती-रत्ती खोज कर सभी परेशान हो गये हैं ." बच्चा इतना बेखबर सो रहा था,
    7 रहीं सूरज अपने घोड़ोंपर चाबुक बरसाता रहा  कुत्ते  भूँकते रहे मशीनें 
    8  चुप क्यों हो गए ?" "सुनाते हैं, सुनाते हैं ." सर्कस ने एक नजर मेरी ओर देखा और जैसे मेरी मंशा ताड़कर बोला, "हमारे लिए  कुत्ते वाला फूल कौन लाएगा ?" "हम लायेंगें !
    9   कुत्ते  पर सवारी गांठने वाले भैरव, को देवता रूप में ग्रहण किया तब मूषक वाहन विघ्नेश गणेश को भी ग्रहण कर उन्हें विघ्नेश बना डाला .
    10  बड़े साहब के घर कितने  कुत्ते  हैं. . . जानकी वकील के घर पूजा में कितनी बलि होती है.

"""


class PageParser(Container):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = None
        if self.start is None:
            self.start = 0

    def __get_page(self):
        """
        create a query url and return a page with results
        """
        params = {'word': self.query,
                  'limit': self.n_results,
                  'start': self.start,
                  'submit': 'Search'}
        s = get('http://www.cfilt.iitb.ac.in/~corpus/hindi/find.php', params=params)
        return s

    def __new_target(self, left, word, right):
        text = '%s %s %s' % (left, word, right)
        idxs = (len(left) + 1, len(left) + len(word) + 1)
        meta = ''
        tags = None
        return Target(text, idxs, meta, tags)

    def __get_results(self):
        """
        parse the page and get results
        """
        num = re.compile(r'\d+')
        sentence_list = []
        center_list = []
        left_list = []
        right_list = []
        soup = BeautifulSoup(self.page.text, 'lxml')
        for sentence in soup.select('tr[bgcolor*="f"] td'):
            if not num.match(sentence.text) and sentence.text.strip():
                sentence_list.append(sentence.text)
                center = sentence.select('font a[target]')
                if center and not num.match(center[0].text):
                    center_list.append(center[0].text)
                else:
                    center_list.append('')
        for i in range(len(sentence_list)):
            if not center_list[i]:
                left_list.append(sentence_list[i])
                right_list.append('')
                continue
            res = sentence_list[i].split(center_list[i])
            left_list.append(res[0])
            right_list.append(res[1])
        s = [self.__new_target(l, w, r) for l, w, r in zip(
            left_list, center_list, right_list)]
        return s

    def __extract_results(self):
        self.page = self.__get_page()
        parsed_results = self.__get_results()
        return parsed_results

    def extract(self):
        parsed_results = self.__extract_results()
        for res in parsed_results:
            yield res
