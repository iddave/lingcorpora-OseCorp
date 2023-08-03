from ..params_container import Container
from requests import get
from bs4 import BeautifulSoup
from html import unescape
from ..target import Target


TEST_DATA = {'test_single_query': {'query': '代汉语'},
             'test_multi_query': {'query': ['古', '问题']}
            }

__author__ = 'kategerasimenko'
__doc__ = \
"""
Chinese Corpus
==============

API for Chinese corpus (http://ccl.pku.edu.cn:8080/ccl_corpus/).
    
**Search Parameters**

query: str or list([str])
    query or queries (currently only exact search by word or phrase is available)
n_results: int, default 100
    number of results wanted
subcorpus: str, default 'xiandai'
    subcorpus.
    Available options:
        * 'xiandai' (modern Chinese)
        * 'dugai' (ancient Chinese)
n_left: int, default 30
    context lenght (in symbols)
n_right: int, default 30
    context lenght (in symbols)
    
Example
-------

.. code-block:: python

    corp = lingcorpora.Corpus('zho')
    results = corp.search('语', n_results=10)
    for result in results:
        for i, target in enumerate(result):
            print(i+1, target.text)

.. parsed-literal::

    "语": 100%|██████████| 10/10 [00:01<00:00,  6.77docs/s]

    1 ...是学校教学的基本组织形式；某些教学内容，特别是自然科学知识、语言文字知识等，成为各历史时期的共同内容；一些反映教育规律的教育...
    2 ...的，必须先教他们识字，不识字就不能有政治，不识字只能有流言蜚语、传闻偏见，而没有政治。"因为政治民主化的最主要表现之一，是人...
    3 ...常有三种：（1）物质载体，如工具、建筑等；（2）精神载体，如语言、文字、意识形态等；（3）人的戴体，如个人所拥有的知识、道德...
    4 ...程。就教育而言，首先是教育者将寓于自己主体内的文化外化为教育语言、文字形式的材料等，教育过程才能进行。没有这种外化，教育过程...
    5 ...一个首要条件，即首先要求人们对文化的认同和理解，无论是见之于语言文字的或是其它象征符号的文化，只有当它们成为共享文化时，才能...
    6 ...如见之于文字的文化，无法向一个文盲传播；将外国文化向不懂该国语言或不了解该文化背景的人传播，就会发生困难。所以，教育者首先需...
    7 ...就是指某种心理机能发展最重要的刻印时期。如2到3岁是儿童口头语言发展的关键期。实验证明，小学四年级是童年思维发展的质变期，初...
    8 ...的生理和心理也存在着差异。心理学研究表明，在婴儿期，孪生子的语言和认识能力就有了差异。
    9 ...直立行走，而是像狼一样四肢落地并养成了狼的生活习性，没有人的语言和思维，没有人的情感和兴趣。由此可知，人的身心的最终发展方向...
    10 ...际交往关系和利益交往关系，使人在交往中逐步掌握作为交往工具的语言，把握思想和行为规范；正是社会意识形态，为个体的心理发展提供...

"""


class PageParser(Container):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.__per_page = 50
        self.__pagenum = 0
        if self.subcorpus is None:
            self.subcorpus = 'xiandai'
        if self.n_left is None:
            self.n_left = 30
        if self.n_right is None:
            self.n_right = 30

            
    def get_results(self):
        """
        create a query url and get results for one page
        """
        params = {'q': self.query,
                  'start': self.__pagenum,
                  'num': self.n_results,
                  'index':'FullIndex',
                  'outputFormat':'HTML',
                  'encoding':'UTF-8',
                  'maxLeftLength':self.n_left,
                  'maxRightLength':self.n_right,
                  'orderStyle':'score',
                  'dir':self.subcorpus,
                  'scopestr':'' # text selection: TO DO?
                  }
        r = get('http://ccl.pku.edu.cn:8080/ccl_corpus/search',params)
        return unescape(r.text)


    def parse_page(self):
        """
        find results (and total number of results) in the page code
        """
        soup = BeautifulSoup(self.__page, 'lxml')
        res = soup.find('table',align='center')
        if res:
            res = res.find_all('tr')
        else:
            return []
        if self.__pagenum == 0:
            self.n_results = min(self.n_results,int(soup.find('td',class_='totalright').find('b').text))
        return res

        
    def parse_result(self,result):
        """
        find hit and its left and right contexts
        in the extracted row of table
        """
        result = result.select('td[align]')
        result = [x.text.strip() for x in result]
        text = ''.join(result)
        idxs = (len(result[0]),len(result[0])+len(result[1]))
        return Target(text, idxs, '', None)

        
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
            self.__pagenum += self.__per_page

