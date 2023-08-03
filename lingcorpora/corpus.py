# python3
# coding=<UTF-8>

import warnings
from collections import Iterable, deque

from tqdm import tqdm

from .result import Result
from .functions import functions


warnings.simplefilter('always', UserWarning)


class Corpus:
    """The object of this class should be instantiated for each corpus. Search is conducted via search method.
    
    Parameters
    ----------
    language: str
        Language ISO 639-3 code for the corpus with combined codes for parallel corpora.
        List of available corpora with corresponding codes:
        
        +--------------+---------------------------------------------------------------+
        | Code         |   Corpus                                                      |
        +==============+===============================================================+
        | ady          |   Adyghe corpus                                               |
        +--------------+---------------------------------------------------------------+
        | alb          |   Albanian corpus                                             |
        +--------------+---------------------------------------------------------------+
        | arm          |   Eastern Armenian corpus                                     |
        +--------------+---------------------------------------------------------------+
        | bam          |   Corpus Bambara de Reference                                 |
        +--------------+---------------------------------------------------------------+
        | bua          |   Buryat corpus                                               |
        +--------------+---------------------------------------------------------------+
        | dan          |   Danish corpus                                               |
        +--------------+---------------------------------------------------------------+
        | deu          |   German corpus                                               |
        +--------------+---------------------------------------------------------------+
        | emk          |   Maninka Automatically Parsed corpus                         |
        +--------------+---------------------------------------------------------------+
        | est          |   Estonian corpus                                             |
        +--------------+---------------------------------------------------------------+
        | grk          |   Modern Greek corpus                                         |
        +--------------+---------------------------------------------------------------+
        | hin          |   Hindi corpus                                                |
        +--------------+---------------------------------------------------------------+
        | kal          |   Kalmyk corpus                                               |
        +--------------+---------------------------------------------------------------+
        | kat          |   Georgian monolingual corpus                                 |
        +--------------+---------------------------------------------------------------+
        | kaz          |   Almaty corpus of the Kazakh language                        |
        +--------------+---------------------------------------------------------------+
        | mon          |   Mongolian corpus                                            |
        +--------------+---------------------------------------------------------------+
        | rus          |   National Corpus of Russian                                  |
        +--------------+---------------------------------------------------------------+
        | rus_parallel |   Parallel subcorpus of National Corpus of Russian Language   |
        +--------------+---------------------------------------------------------------+
        | rus_pol      |   Polish-Russian Parallel Corpus                              |
        +--------------+---------------------------------------------------------------+
        | tat          |   Tatar corpus                                                |
        +--------------+---------------------------------------------------------------+
        | udm          |   Udmurt corpus                                               |
        +--------------+---------------------------------------------------------------+
        | yid          |   Modern Yiddish corpus                                       |
        +--------------+---------------------------------------------------------------+
        | zho          |   Center of Chinese Linguistics corpus                        |
        +--------------+---------------------------------------------------------------+
        | zho_eng      |   Chinese-English subcorpus of JuKuu corpus                   |
        +--------------+---------------------------------------------------------------+
        
    verbose: bool, default True
        whether to enable tqdm progressbar.
    
    Attributes
    ----------
    doc: str
        Documentation for chosen corpus (after instance creation).
    results: list
        List of all Result objects, each returned by search method.
    failed: list
        List of Result objects where nothing was found.
    """

    def __init__(self, language, verbose=True):
        """
        Parameters
        ----------
        language: str
            language alias
        verbose: bool
            enable tqdm progressbar
        """
        
        self.language = language
        self.verbose = verbose
        self.corpus = functions[self.language] 
        self.doc = self.corpus.__doc__
        self.gr_tags_info = self.corpus.__dict__.get('GR_TAGS_INFO')

        self.results = list()
        self.failed = deque(list())
        
        self.warn_str = 'Nothing found for query "%s"'
        self.pbar_desc = '"%s"'
    
    def __getattr__(self, name):
        if name.lower() == 'r':
            return self.results
        
        raise AttributeError("<Corpus> object has no attribute '%s'" % name)

    def __to_multisearch_format(self, arg, arg_name, len_multiplier=1):
        """
        pack <str> or List[str] `arg` to multisearch format
        """
        
        if isinstance(arg, str):
            arg = [arg] * len_multiplier
        
        if not isinstance(arg, Iterable):
            raise TypeError(
                'Argument `%s` must be of type <str> or iterable[str], got <%s>'
                % (arg_name, type(arg))
            )
            
        return arg

    def get_gr_tags_info(self):
        return self.gr_tags_info

    def search(self, query, *args, **kwargs):
        """This is a search function that queries the corpus and returns the results.
        
        Parameters
        ----------
        query: str
            query, for arguments see `params_container.Container`
        
        Example
        -------
        .. code-block:: python

            >>> rus_corp = lingcorpora.Corpus('rus')
            >>> rus_results = rus_corp.search('мешок', n_results=10)
            >>> rus_results
            "мешок": 100%|███████████████████████████████| 10/10 [00:07<00:00,  1.40docs/s]
            [Result(query=мешок, N=10, params={'n_results': 10, 'kwic': True, 'n_left': None, 'n_right': None, 'query_language': None, 'subcorpus': 'main', 'get_analysis': False, 'gr_tags': None, 'start': 0, 'writing_system': None})]
        """

        query = self.__to_multisearch_format(arg=query, arg_name='query')
        gr_tags = kwargs.get('gr_tags')
        if gr_tags is None:
            gr_tags = [None] * len(query)
        gr_tags = self.__to_multisearch_format(
            arg=gr_tags,
            arg_name='gr_tags',
            len_multiplier=len(query)
        )

        if len(query) != len(gr_tags):
            raise ValueError('`query`, `gr_tags` length mismatch')

        results = []
        
        for q, c_gr_tags in zip(query, gr_tags):
            kwargs['gr_tags'] = c_gr_tags            
            parser = self.corpus.PageParser(q, *args, **kwargs)
            result_obj = Result(self.language, parser.__dict__)
                
            for target in tqdm(
                parser.extract(),
                total=parser.n_results,
                unit='docs',
                desc=self.pbar_desc % q,
                disable=not self.verbose
            ):
                result_obj.add(target)
            
            if result_obj:
                results.append(result_obj)
            
            else:
                warnings.warn(self.warn_str % q)
                self.failed.append(result_obj)
        
        self.results.extend(results)
        
        return results

    def retry_failed(self):
        """
        Apply `.search()` to failed queries stored in `.failed`
        """
        
        if self.failed:
            n_rounds = len(self.failed)
            retrieved = []
            
            for _ in range(n_rounds):
                r_failed = self.failed.popleft()
                
                # List[<Result>]
                results_new = self.search(
                    r_failed.query,
                    **r_failed.params
                )
                
                if results_new:
                    retrieved.append(results_new[0])
            
            return retrieved
        
    def reset_failed(self):
        """
        Reset `.failed`
        """
        
        self.failed = deque(list())
