import nltk
nltk.download('book_grammars')
# nltk.data.show_cfg('grammars/book_grammars/sql0.fcfg')

from nltk.parse import load_parser
cp = load_parser('grammars/book_grammars/sql0.fcfg')
query = 'What are the buildings?'
trees = list(cp.parse(query.split()))
answer = trees[0].label()['SEM']
answer = [s for s in answer if s]
q = ' '.join(answer)
# print(q)
# SELECT City FROM city_table WHERE Country="china"