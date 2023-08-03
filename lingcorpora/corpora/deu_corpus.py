from ..params_container import Container
from ..target import Target
from requests import post
from bs4 import BeautifulSoup

TEST_DATA = {'test_single_query': {'query': 'da'},
             'test_multi_query': {'query': ['da', 'immer']}
            }

__author__ = 'alexeykosh, ustya-k'
__doc__ = \
"""
German Corpus
=============

API for German corpus (https://www.dwds.de).
    
**Search Parameters**

query: str or list([str])
    query or queries. By default, inflection will be included
    (unlike in the case of the other corpora). To perform an
    exact search add '@' symbol before the query (e.g. '@gut').
    By default multi-word queries will not work. To perform
    a multi-word query, put it between double quotation marks
    (e.g. '"guten tag"'). The full list of options is available
    `here (in German) <https://www.dwds.de/d/suche#cheatsheet>`_.
n_results: int, default 100
    number of results wanted
kwic: bool, default True
    kwic format (True) or a sentence (False) (True by default)
subcorpus: str
    subcorpus. The description for the given options are
    `here (in German) <https://www.dwds.de/r#corpusstat>`_.
    Available options:
        * 'kern' (by default)
        * 'tagesspiegel'
        * 'zeit'
        * 'public'
        * 'blogs'
        * 'dingler'
        * 'untertitel'
        * 'spk'
        * 'bz'
        * 'dta'
        * 'korpus21'
        
Example
-------

.. code-block:: python

    corp = lingcorpora.Corpus('deu')
    results = corp.search('gut', n_results=10)
    for result in results:
        for i, target in enumerate(result):
            print(i+1, target.text)

.. parsed-literal::

    "gut": 100%|██████████| 10/10 [00:00<00:00, 17.48docs/s]

    1 Zwar ist er in den letzten Tagen von ungarischer und czechischer Seite hart angegriffen worden, aber neben den Ugron , Gregr und Genossen gibt es in der habsburgischen Monarchie noch vernünftige Leute genug, die recht gut wissen, was sie am Dreibund haben und die sich auch sorgfältig davor hüten, durch Uebertreibung nationaler Forderungen den Bestand der Monarchie zu gefährden.
    2 In den sieben laugen Jahren schwerster Knechtschaft lehrte Gott unser Volk sich auf sich selbst besinnen, und unter dem Druck des Fußes eines übermüthigen Eroberers gebar unser Volk aus sich heraus den hehrsten Gedanken, daß es die höchste Ehre sei, im Waffendienste seinem Vaterlande Gut und Blut zu weihen:
    3 In den sieben langen Jahren schwerster Knechtschaft lehrte Gott unser Volk sich auf sich selbst besinnen und unter dem Drucke eines übermüthigen Eroberers gebar unser Volk aus sich heraus den hehrsten Gedanken, daß es die höchste Ehre sei, im Waffendienste seinem Vaterlande Gut und Blut zu weihen, die allgemeine Dienstpflicht . Mein Urgroßvater gab ihr Form und Leben und neuer Lorbeer krönte die neuerstandene Armee und ihre jungen Fahnen.
    4 In den sieben langen Jahren schwerster Knechtschaft lehrte Gott unser Volk sich auf sich selbst besinnen, und unter dem Druck des Fußes eines übermütigen Eroberers gebar unser Volk aus sich heraus den hehrsten Gedanken, daß es die höchste Ehre sei, im Waffendienste seinem Vaterlande Gut und Blut zu weihen: die allgemeine Dienstpflicht . Mein Urgroßvater gab ihr Form und Leben, und neuer Lorber krönte die neu erstandene Armee und ihre jungen Fahnen.
    5 Wie die "Köln. Ztg." aus London erfährt, beunruhigt man sich dort, obschon neuere Nachrichten aus Ladysmith von hinreichendem Proviant für mindestens sechs Wochen melden, neuerdings in gewöhnlich gut unterrichteten Kreisen wieder lebhafter um das Schicksal der eingeschlossenen Garnison.
    6 Man wird gut thun, hinter diese privaten englischen Berichte ein Fragezeichen zu setzen.
    7 Der Rittmeister Montmorency von den 21. Lancers stieß mit einer überlegenen feindlichen Streitmacht, die Artillerie mit sich führte, zusammen und wurde im Laufe des Sonnabends gezwungen, sich nach Dordrecht zurückzuziehen, was in guter Ordnung geschah.
    8 Insbesondere sollen die Parlamente, die im Begriff stehen, neue Marinerüstungen zu beraten, sich von dem Gedanken erleuchten lassen, daß es einen besseren Weg giebt, das Vaterland zu schützen und zugleich der Menschheit ewige Dienste zu leisten. -
    9 Diejenigen, die ihn tadelten, seine keine guten Katholiken und seien vom Protestantismus angesteckt.
    10 Die gute einheimische Ernte in Verbindung mit den reichlichen Vorräthen Amerikas und der Aussicht auf große Erträge in Argentinien und Australien lähmten jeden Anlauf zu einer Besserung.

"""


class PageParser(Container):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__page = None
        if self.subcorpus is None:
            self.subcorpus = 'kern'

    def __get_page(self):
        params = {'corpus': self.subcorpus,
                  'date-end': '1999',
                  'date-start': '1900',
                  'format': 'kwic',
                  'genre': 'Belletristik',
                  'genre': 'Wissenschaft',
                  'genre': 'Gebrauchsliteratur',
                  'genre': 'Zeitung',
                  'limit': self.n_results,
                  'q': self.query,
                  'sort': 'date_asc'}
        s = post('https://www.dwds.de/r', params=params)
        return s

    def __new_target(self, left, word, right):
        text = '%s %s %s' % (left, word, right)
        idxs = (len(left) + 1, len(left) + len(word) + 1)
        meta = ''
        tags = None
        return Target(text, idxs, meta, tags)

    def __get_results(self):
        left_list = []
        right_list = []
        center_list = []
        soup = BeautifulSoup(self.__page.text, 'lxml')
        for left in soup.select('.ddc-kwic-ls'):
            left_list.append(left.text.strip())
        for center in soup.select('.ddc-kwic-kw.ddc-hl'):
            center_list.append(center.text.strip())
        for right in soup.select('.ddc-kwic-rs'):
            right_list.append(right.text.strip())

        s = [self.__new_target(l, w, r) for l, w, r in zip(
            left_list, center_list, right_list)]
        return s

    def __extract_results(self):
        self.__page = self.__get_page()
        parsed_results = self.__get_results()
        return parsed_results

    def extract(self):
        parsed_results = self.__extract_results()
        for res in parsed_results:
            yield res
