from .arkhangelskiy_corpora import PageParser

language = 'greek'
results = 'http://web-corpora.net/GreekCorpus/search/results.php'

TEST_DATA = {'test_single_query': {'query': 'γάτα'},
             'test_multi_query': {'query': ['γάτα', 'αγάπη']}
             }

__author__ = 'ustya-k'
__doc__ = \
"""
Modern Greek Corpus
===================

API for Modern Greek corpus (http://web-corpora.net/GreekCorpus/search/).

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

    corp = lingcorpora.Corpus('grk')
    results = corp.search('γλώσσα', n_results=10)
    for result in results:
        for i, target in enumerate(result):
            print(i+1, target.text)

.. parsed-literal::
    
    "γλώσσα": 100%|██████████| 10/10 [00:03<00:00,  2.95docs/s]

    1 Τέτοια βρισίδια του Αγαμέμνονα του πρωτοστρατολάτηξεφώνιζε ο Θερσίτης, μα ο θεϊκός πετάχτηκε Οδυσσέαςμπροστά του και στραβοκοιτώντας τον αψιά τον αποπηρε:« Θερσίτη εσύ γλωσσά, ατσαλόστομε!
    2 «Θέλουμε και εξειδικευμένους και καταρτισμένους επαγγελματίες-τεχνίτες που να μιλούν τη γλωσσά μας, να έχουν μαθηματική αντίληψη, ψηφιακή ικανότητα, πρωτοβουλία, πολιτισμική συνείδηση και να αναπτύσσουν την ιδιότητα του πολίτη.
    3 «Τηλέμαχε, γλωσσά κι απόκοτε, τι λόγια αυτά που κρένεις;
    4 «Τηλέμαχε γλωσσά κι απόκοτε, τι λόγια αυτά που κρένεις;να μας ντροπιάσεις θες κι απάνω μας να ρίξεις κατηγόρια;
    5 «Τηλέμαχε γλωσσά κι απόκοτε, μη συλλογάσαι τώραπια άλλο κακό βαθιά στα φρένα σου, μήτε έργο μήτε λόγο’τη χάρη κάνε μου κι ως άλλοτε μονάχα τρώγε, πίνε ᾿κι οι Αργίτες όλα αυτά που γύρεψες — καράβι, λαμνοκόπουςξεδιαλεχτούς — θα σ'τα τελέψουνε, κι έτσι γοργά θα φτάσειςστην άγια Πύλο, για τον κύρη σου τον ξακουστό να μάθεις.»
    6 ΔΕΥΤΕΡΑ 19/5-ΝΕΟΕΛΛΗΝΙΚΗ ΓΛΩΣΣΑ ΓΕΝΙΚΗΣ ΠΑΙΔΕΙΑΣ
    7 ΣΚΛΗΡΗ ΓΛΩΣΣΑ ΣΕ ΓΕΩΡΓΙΑ, ΟΥΚΡΑΝΙΑ
    8 ΣΤΗ ΓΛΩΣΣΑ ΤΗΣ ΕΠΟΧΗΣ
    9 ΤΡΙΤΗ 20/5-ΝΕΟΕΛΛΗΝΙΚΗ ΓΛΩΣΣΑ ΓΕΝΙΚΗΣ ΠΑΙΔΕΙΑΣ
    10 Η ΠΑΓΚΟΣΜΙΑ «ΓΛΩΣΣΑ » ΤΟΥ ΧΡΗΜΑΤΟΣ
    
"""


class PageParser(PageParser):

    def __init__(self, *args, **kwargs):
        super().__init__(language, results, *args, **kwargs)
