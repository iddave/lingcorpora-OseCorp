from ..params_container import Container
from requests import get
from bs4 import BeautifulSoup
import re
from html import unescape
from ..target import Target


__author__ = 'ustya-k'
__doc__ = \
"""
arkhangelskiy_corpora
=====================

API for Тimofey Arkhangelskiy's corpora (http://web-corpora.net/).

**Search Parameters**

query: str or List([str])
    query or queries
n_results: int
    number of results wanted (100 by default)
kwic: bool
    kwic format (True) or a sentence (False) (True by default)
get_analysis: bool
    tags shown (True) or not (False) (False by default)
"""


class PageParser(Container):

    def __init__(self, search_language, results_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__search_language = search_language
        self.__results_url = results_url
        self.__per_page = 100

        if self.subcorpus is None:
            self.subcorpus = ''

        self.sid = 0
        self.__get_sid()

        self.__page = None
        self.__pagenum = 1
        self.__occurences = None

    def __get_sid(self):
        params = {
            "fullsearch": self.query,

            "occurences_per_page": self.__per_page,
            "search_language": self.__search_language,
            "subcorpus": self.subcorpus,
            "sort_by": "wordform",
            "interface_language": "ru",
            "sentences_per_enlarged_occurrence": "1",
            "contexts_layout": "basic",
            "show_gram_info": int(self.get_analysis),
            "subcorpus_query": ""
        }
        res = get(self.__results_url, params)
        sid_res = re.search('sid=([0-9]+)', res.text)
        if sid_res is not None:
            self.sid = sid_res.group(1)

    def get_results(self):
        params = {"sid": self.sid,
                  "page": self.__pagenum,
                  "search_language": self.__search_language}
        res = get(self.__results_url, params)
        return unescape(res.text)

    def parse_page(self):
        soup = BeautifulSoup(self.__page, 'lxml')
        occs = re.search('FOUND(.*?)MATCHES', soup.text)
        self.__occurences = int(occs.group(1).replace(' ', ''))
        contexts = soup.find(id="contexts_div")
        res = list(contexts.find_all('table', recursive=False))
        return res

    def parse_results(self, results):
        parsed_results = []
        for i in range(len(results)):
            context = self.__parse_context(results[i])
            if context is not None:
                parsed_results.append(context)
        return parsed_results

    def __parse_context(self, context):
        res_context = list(context.find_all('tr', recursive=False))[1]
        meta = self.__get_meta(context)
        res_text, word, idxs = self.__get_text(res_context)
        tags = []
        if idxs is None:
            return None
        if self.get_analysis:
            tags = word['tag']
        return Target(res_text, idxs, meta, tags)

    def __move_tags_from_pos(self, pos, tags):
        '''
        In some cases grammatical gender and animacy are in PoS tag.
        '''
        new_pos = []
        new_tags = []
        for p, t in zip(pos, tags):
            res = re.search('^(.*?)(?:,|$)(.*?)$', p)
            new_pos.append(res.group(1))
            new_tags.append(','.join([res.group(2), t]).strip(','))
        return new_pos, new_tags

    def __get_tag(self, tag_text):
        '''
        tag_text: str, tag line
        tags: list of dicts
        '''
        brkts = '?:(\'(.*?)\',?)+'
        # [lemmas], [PoS], [tags]
        regex = re.search(
            'popup\(this,\[(.*?)\],\[(.*?)\],\[(.*?)\],\[(.*?)\],\[(.*?)\]', tag_text) #дописал две группы
        try:
            lemmas = re.findall("'(.*?)'", regex.group(1))
            pos = re.findall("'(.*?)'", regex.group(2))
            tags_values = re.findall("'(.*?)'", regex.group(3))

            #ДОПИСЫВАЮ
            group4 = re.findall("'(.*?)'", regex.group(4))
            translations = re.findall("'(.*?)'", regex.group(5))

            pos, tags_values = self.__move_tags_from_pos(pos, tags_values)
        except AttributeError:
            lemmas = []
            pos = []
            tags_values = []

            #ДОПИСЫВАЮ
        tags = [{'lemma': l, 'PoS': p, 'tag': t, 'transl': tr}
                for l, p, t, tr in zip(lemmas, pos, tags_values, translations)]
        return tags

    def __get_word_info(self, res_context):
        l_context_len = 0
        word = {}
        for child in list(res_context.find_all('span')):
            if 'class' in child.attrs and 'result1' in child.attrs['class']:
                word['word'] = child.text
                word['tag'] = self.__get_tag(child.attrs['onmouseover'])
                break
        return word

    def __get_idxs(self, text, word):
        beg = re.search('\\b' + word + '\\b', text)
        if beg is None:
            return None
        return (beg.start(), beg.end())

    def __get_text(self, res_context):
        res_text = res_context.text.strip()
        word = self.__get_word_info(res_context)
        idxs = None
        if word != {}:
            idxs = self.__get_idxs(res_text, word['word'])
        return res_text, word, idxs

    def __get_meta(self, context):
        header = context.find(class_='results_header')
        text = header.find_all('td')[1].text
        text = re.sub('\s{2,}', '\t', text)
        text = re.sub('(^\s+|\s+$)', '', text)
        text_as_list = text.split('\t')
        return ', '.join(text_as_list)

    def extract_from_page(self):
        self.__page = self.get_results()
        rows = self.parse_page()
        return self.parse_results(rows)

    def extract(self):
        result_found = False
        # while (self.__occurences is None) or (output_counter < self.n_results and self.__occurences > output_counter):
        # self.__pagenum = output_counter / self.__per_page + 1
        while result_found == False :
            parsed_results = self.extract_from_page()
            self.__pagenum += 1
            if self.__occurences == 0:
                result_found = True
                yield False
            elif (parsed_results != []):
                result_found = True
                yield parsed_results[0]