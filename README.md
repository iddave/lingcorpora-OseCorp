# Морфологический анализатор

  По осетинскому\дигорскому слову выводит его морфологический разбор.
Данные берутся из [осетинского](http://corpus.ossetic-studies.org/) и [дигорского](http://corpus-digor.ossetic-studies.org/) корпусов. Для работы приложения нужен выход в интернет и доступ к сайтам.
  В основе проекта лежит использование [lingcorpora](https://lingcorpora.github.io/lingcorpora.py/html/index.html).
____

- **arkhangelskiy_corpora** – Тут реализован класс PageParser, который описывает парсер страницы сайта корпуса определенного шаблона, например сайта [старого албанского корпуса](http://web-corpora.net/AlbanianCorpus/).
-	**lang_corpus.py** – файлы которые хранят данные конкретного корпуса и переопределяют PageParser если это необходимо. Там хранится строка описывющая язык и ссылка на страницу результатов, например для адыгского (ady_corpus.py) эти данные выглядят так:
```python
language = ‘adyghe’
results = 'http://web-corpora.net/AdygheCorpus/search/results.php'
```
-	**corpus.py** – основной код хранится здесь. Тут реализуются методы поиска текста в определенном корпусе. Для каждого языкового коруса требуется создавать отдельный экземпляр этого класса.
-	**functions.py** – ставятся сопостовления кодам языка в формате Language ISO 639-3 code соответствующие языки. Например, 
‘rus’: rus_corpus
-	**params_container.py** – описание параметров использующихся при поиске и обработки текста
-	**result.py** – объект этого класса содержит найденную информацию. Объекты этого класса итерируемы и поддерживают индексацию
-	**target.py** – объект этого класса описывает один элемент из списка result
- **attributes.json** - файл с расшифровкой граммем

Пример кода с использованием вышеперечисленных классов:
```python
rus_corp = lingcorpora.Corpus('rus')
rus_results = rus_corp.search('одеяло', n_results = 10,get_analysis=True)[0]
first_hit = rus_results[0]
first_hit
```
Вывод 
```txt
Target(одеяло, Народный костюм: архаика или современность? // «Народное творчество», 2004)
```

Поиск грамем осуществляется в файле analyse.py:
```python
def get_tags(word, lang):
    corp = lingcorpora.Corpus(lang)
    results = corp.search(word, n_results=1, get_analysis = True)
    for result in results:
        for i, target in enumerate(result):
            if target != False:
                for tok in target.analysis:
                        translation=""
                        if tok['transl'] != '': translation = '\nПеревод: '+ tok['transl']
                        yield Convert(tok['lemma']+','+tok['PoS'] +','+ tok['tag']) + translation
```
