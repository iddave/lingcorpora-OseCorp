# python3
# coding=<UTF-8>

import re
import csv


class Result:
    """The object of this class contains all results found. Result object is iterable and supports indexing.
    
    Parameters
    ----------
    language: str
        corpus language.
    query_params: dict
        all other parameters of the search.

    Attributes
    ----------
    results: list[Target]
        List of results.
    n: int
        Number of results.
    query: str
        Search query.
    
    Example
    -------
    .. code-block:: python
    
        >>> corp = lingcorpora.Corpus('emk')
        >>> results = corp.search('tuma', n_results=10, kwic=False)[0]
        >>> results
        "tuma": 100%|██████████| 10/10 [00:00<00:00, 11.09docs/s]
        Result(query=tuma, N=10, params={'n_results': 10, 'kwic': False, 'n_left': None, 'n_right': None, 'query_language': None, 'subcorpus': 'cormani-brut-lat', 'get_analysis': False, 'gr_tags': None, 'start': 0, 'writing_system': ''})
    """

    def __init__(self, language, query_params):
        """
        language: str
            language
        query_params: dict
            __dict__ of used parser
        """
        
        self.lang = language
        self.query = query_params['query']
        
        self.params = {
            k: query_params[k]
            for k in query_params
            if not k.startswith('_') and k not in {'page', 'query'}
        }
        self.results = list()
        self.n = 0
        self.header = ('index', 'text')
        self.kwic_header = ('index', 'left', 'center', 'right')
        self.not_allowed_sub_regexp = re.compile('/\\?%*:|"<>')

    def __str__(self):
        return 'Result(query=%s, N=%s, params=%s)' % \
                (self.query, self.n, self.params)
    
    __repr__ = __str__
    
    def __bool__(self):
        return self.n > 0
    
    def __iter__(self):
        return iter(self.results)
    
    def __getattr__(self, name):
        if name.lower() == 'r':
            return self.results
        
        raise AttributeError("'Result' object has no attribute '%s'" % name)
        
    def __getitem__(self,key):
        return self.results[key]
        
    def __setitem__(self,key,val):
        self.results[key] = val

    def __delitem__(self, key):
        del self.results[key]
        
    def add(self, x):
        self.results.append(x)
        self.n += 1
    
    def export_csv(self, filename=None, header=True, sep=';'):
        """Save search result as CSV.
        
        Parameters
        ----------
        filename: str, default None
            name of the file. If None, filename is lang_query_results.csv
            with omission of disallowed filename symbols.
        header: bool, default True
            whether to include a header in the table.
            Header is stored in .__header: ``('index', 'text')``
        sep: str, default ';'
            cell separator in the csv.
        """

        if filename is None:
            filename = '%s_%s_results.csv' % \
                        (self.lang, self.not_allowed_sub_regexp.sub('', self.query))
        
        with open(filename, 'w', encoding='utf-8-sig') as f:
            writer = csv.writer(
                f,
                delimiter=sep,
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
                lineterminator='\n'
            )
            
            if self.params['kwic']:
                if header:
                    writer.writerow(self.kwic_header)
                
                n_left = self.params['n_left'] if self.params['n_left'] is not None else 10 
                n_right = self.params['n_right'] if self.params['n_right'] is not None else 10
                    
                for i, t in enumerate(self.results):
                    writer.writerow((i + 1, *t.kwic(n_left, n_right)))
            
            else:
                if header:
                    writer.writerow(self.header)
                
                for i, t in enumerate(self.results):
                    writer.writerow((i + 1, t.text))
                    
    def clear(self):
        """Overwrites the results attribute to empty list.
        
        Example
        -------
        .. code-block:: python
        
            >>> print(results.results)
            >>> results.clear()
            >>> print(results.results)
            [Target(tuma, ), Target(tuma, ), Target(tuma, ), Target(tuma, ), Target(tuma, ), Target(tuma, ), Target(tuma, ), Target(tuma, ), Target(tuma, ), Target(tuma, )]
            []
        """
        del self.results
        self.results = list()
