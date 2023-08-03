from .arkhangelskiy_corpora import PageParser

language = 'albanian'
results = 'http://web-corpora.net/AlbanianCorpus/search/results.php'

TEST_DATA = {'test_single_query': {'query': 'mace'},
             'test_multi_query': {'query': ['mace', 'dua']}
             }

__author__ = 'ustya-k'
__doc__ = \
"""
Albanian Сorpus
===============
    
API for Albanian corpus (http://web-corpora.net/AlbanianCorpus/search/).

**Search Parameters**

query: str or list([str])
    query or queries
n_results: int, default 100
    number of results wanted
kwic: bool, default True
    kwic format (True) or a sentence (False)
get_analysis: bool, default False
    tags shown (True) or not (False)
    
Example
-------

.. code-block:: python

    corp = lingcorpora.Corpus('alb')
    results = corp.search('shqipe', n_results=10)
    for result in results:
        for i, target in enumerate(result):
            print(i+1, target.text)
    
.. parsed-literal::

    "shqipe": 100%|██████████| 10/10 [00:04<00:00,  2.02docs/s]

    1 Vetë termi huliganizëm e ka prejardhjen nga një mbiemër irlandez «Hooligan » i cili në gjuhën shqipe do të thotë qen, langua ose laro.
    2 Në suaza të realitetit shumetnik që e ka Maqedonia, Bajrami thotë se barazimi i gjuhës shqipe me atë maqedonase si gjuhë zyrtare në vend, paraqet elementin kryesor për plotësimin e këtij mozaiku shumetnik që po ndërtohet në vend.
    3 Në të parën punohet pa kushte minimale, ndërsa në të dytën - sipas të gjitha standardeve, për shkak se MASH nuk është kursyer asnjëherë që të investojë në shkollën e Lubancës, ku mësimi zhvillohet në gjuhën maqedonase, ndërsa në shkollën e Lubotenit - ku mësimi zhvillohet në gjuhën shqipe, nuk është investuar thuajse asgjë në 50 vitet e fundit, prej vitit 1963 kur edhe u ndërtua shkolla.
    4 Edhe për Bogdanin ka pasaktësi kur thotë:«Kryevepra e tij Çeta e profetëve është një traktat i rëndësishëm teologjik e filozofik dhe vepra e parë më e madhe e shkruar në shqip"që mendoj se Bogdani, veprën e quajtur Flanisae prophetarum (Hojet e profetëve), e ka shkruar vetëm në gjuhën shqipe dhe Kongregacioni ka pranuar të botohet me kusht që të përkthehet edhe në italishte, çështja e kalepinit (S. Riza).
    5 Më tej thuhet «autorë tashmë në rrjedhat e letërsisë shqipe të sh.
    6 Së pari, nëntitulli nuk është i saktë, pse ashtu si është formuluar (Letërsia shqipe) nënkupton mbarë letërsinë shqiptare e mendoj se është dashur të thuhet Letërsia shqiptare në Kosovë, ashtu si edhe jo Gjuhët, po Gjuhët në Kosovë, jo Zejet, po Zejet në Kosovë e tjerë.
    7 Autori i nënkapitullit Letërsia shqipe e fillon studimin me Pjetër Budin, Pal Hasit (Palit prej Hasi), Pjetër Bogdanin, Gjon Nikollë Kazazin, për të vazhduar me Tahir Efendi Boshnjakun, Sheh Hilmi Maliqin, Ndue Bytyqin, Shtjefën Gjeçovin e tjerë, ndërsa më poshtë thotë se «fillimet e saj lidhen me shkrimet e para letrare në nismë të viteve’50, që tingëllon si një fillim nga asgjëja », që duket se është në kolizion mendimesh.
    8 «Formula për përkthimin e të gjithë këtyre titujve për këtë periudhë është çështje teknike e shtëpive që merren me përkthim », pohon zëvendësministri Neziri, ndërsa tregon se do të jetë MASH ajo që në të ardhmen do të hapë tenderët për përkthimin e të gjithë titujve të mbetur, si në maqedonisht, ashtu edhe në gjuhën shqipe.
    9 Sipas banorëve të fshatit Podgorcë, ata deri më 1945 kanë mësuar në gjuhën shqipe dhe mësues kanë patur veteranin e arsimit shqiptar, Tomorr Starovën nga Pogradeci, kurse shkolla ka mbajtur emrin e publicistit nga ky fshat, Iljaz Podgorca.
    10 Ky hap për hapjen e paraleleve me mësim në gjuhën shqipe është një zhvillim pozitiv theksojnë banorët që e ndjejnë veten shqiptar në këtë fshat, në drejtim të ruajtjes dhe kultivimin e gjuhës shqipe.
    
"""


class PageParser(PageParser):

    def __init__(self, *args, **kwargs):
        super().__init__(language, results, *args, **kwargs)
