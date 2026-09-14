from pathlib import Path
import re, time, sqlite3, json
from urllib.parse import urljoin
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

DP = Path('data_pipeline')
DP.mkdir(exist_ok=True)
session = requests.Session()
session.mount('https://', HTTPAdapter(max_retries=Retry(
    total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])))
session.headers['User-Agent'] = 'EducationalCatalogPipeline/1.0'
def soup_at(url):
    response = session.get(url, timeout=30)
    response.raise_for_status()
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'html.parser')

rows = []
for page in range(1, 6):
    url = f'https://books.toscrape.com/catalogue/page-{page}.html'
    listing = soup_at(url)
    for card in listing.select('article.product_pod'):
        detail_url = urljoin(url, card.select_one('h3 a')['href'])
        detail = soup_at(detail_url)
        product = detail.select_one('.product_main')
        rating_tag = product.select_one('.star-rating')
        rating_text = next((x for x in rating_tag.get('class', [])
                            if x != 'star-rating'), '') if rating_tag else ''
        def field(selector):
            tag = product.select_one(selector)
            return tag.get_text(' ', strip=True) if tag else ''
        breadcrumb = detail.select('ul.breadcrumb li a')
        rows.append(dict(title=field('h1'), price=field('.price_color'),
                         star_rating=rating_text, availability=field('.availability'),
                         category=breadcrumb[-1].get_text(strip=True) if breadcrumb else '',
                         source_url=detail_url))
        time.sleep(0.12)
    print(f'Page {page}/5 complete: {len(rows)} books')
raw_books = pd.DataFrame(rows)
raw_books.to_csv(DP / 'raw_books.csv', index=False)
print(raw_books.head().to_string(index=False))


books = raw_books.copy()
books['price_gbp'] = pd.to_numeric(
    books['price'].str.extract(r'(\d+(?:\.\d+)?)', expand=False), errors='coerce')
books['rating'] = books['star_rating'].map(
    {'One':1, 'Two':2, 'Three':3, 'Four':4, 'Five':5})
def stock_status(text):
    text = text.lower().strip()
    if 'out of stock' in text: return False
    if 'in stock' in text: return True
    return None
books['in_stock'] = books['availability'].map(stock_status)
valid = (books[['price_gbp','rating','in_stock']].notna().all(axis=1)
         & books['title'].str.strip().ne('') & books['category'].str.strip().ne(''))
books.loc[~valid].to_csv(DP / 'rejected_rows.csv', index=False)
books = books.loc[valid].drop_duplicates('source_url').copy()
books['rating'] = books['rating'].astype(int)
books['in_stock'] = books['in_stock'].astype(bool)
books['price_inr'] = (books['price_gbp'] * 105.50).round(2)
assert len(books) >= 60 and books['category'].nunique() >= 3
assert books['rating'].between(1,5).all()
assert np.allclose(books['price_inr'], (books['price_gbp']*105.50).round(2))
books.to_csv(DP / 'clean_books.csv', index=False)
print(books.dtypes)
print('Rows:', len(books), 'Categories:', books['category'].nunique(),
      'Rejected:', int((~valid).sum()))


categories = pd.DataFrame({'category_name':sorted(books['category'].unique())})
categories.insert(0, 'category_id', range(1, len(categories)+1))
book_table = books.merge(categories, left_on='category', right_on='category_name')
book_table = book_table[['title','price_gbp','price_inr','rating','in_stock','category_id']].copy()
book_table.insert(0, 'book_id', range(1, len(book_table)+1))
book_table['in_stock'] = book_table['in_stock'].astype(int)
conn = sqlite3.connect(DP / 'books.db')
conn.execute('PRAGMA foreign_keys=ON')
conn.executescript("""
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS categories;
CREATE TABLE categories (
 category_id INTEGER PRIMARY KEY, category_name TEXT NOT NULL UNIQUE);
CREATE TABLE books (
 book_id INTEGER PRIMARY KEY, title TEXT NOT NULL,
 price_gbp REAL NOT NULL CHECK(price_gbp>=0), price_inr REAL NOT NULL,
 rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
 in_stock INTEGER NOT NULL CHECK(in_stock IN (0,1)),
 category_id INTEGER NOT NULL REFERENCES categories(category_id));
""")
conn.executemany('INSERT INTO categories VALUES (?,?)',
                 categories.itertuples(index=False, name=None))
conn.executemany('INSERT INTO books VALUES (?,?,?,?,?,?,?,?)',
                 book_table.itertuples(index=False, name=None))
conn.commit()
assert conn.execute('PRAGMA foreign_key_check').fetchall() == []
print('Database saved:', DP / 'books.db')


queries = {
 '01_in_stock': 'SELECT title, rating FROM books WHERE in_stock=1 AND rating>=4;',
 '02_top_prices': 'SELECT title, price_gbp FROM books ORDER BY price_gbp DESC, book_id LIMIT 10;',
 '03_distinct_ratings': 'SELECT DISTINCT rating FROM books ORDER BY rating;',
 '04_price_range': 'SELECT title, price_gbp FROM books WHERE price_gbp BETWEEN 10 AND 20 ORDER BY book_id;',
 '05_join': """SELECT b.book_id, b.title, b.rating, c.category_name
 FROM books b JOIN categories c ON b.category_id=c.category_id
 WHERE b.rating IN (4,5) ORDER BY b.book_id;"""
}
results, report = {}, ['# SQL queries and actual results']
for name, query in queries.items():
    result = pd.read_sql(query, conn)
    results[name] = result
    result.to_csv(DP / f'{name}.csv', index=False)
    report += [f'## {name}', f'```sql\n{query}\n```', result.to_markdown(index=False)]
    print(name, '\n', result.head(10).to_string(index=False))
merged = pd.merge(book_table, categories, on='category_id')
merged = merged.loc[merged.rating.isin([4,5]),
                    ['book_id','title','rating','category_name']].sort_values('book_id').reset_index(drop=True)
pd.testing.assert_frame_equal(results['05_join'], merged, check_dtype=False)
side_by_side = pd.concat({'SQL':results['05_join'], 'pandas':merged}, axis=1)
print(side_by_side.head().to_string(index=False))
report += ['## SQL versus pandas — equal', side_by_side.to_markdown(index=False)]
(DP / 'sql_results.md').write_text('\n\n'.join(report), encoding='utf-8')
(DP / 'queries.sql').write_text('\n\n'.join(queries.values()))
(DP / 'README.md').write_text('# Data pipeline\nRun from the repository root: `python data_pipeline/pipeline.py`.\nInstall the consolidated root requirements first. The first five listing pages are scraped with requests and BeautifulSoup; detail pages supply category and availability. Unparseable required fields are dropped and logged in rejected_rows.csv because inventing prices/ratings would distort the catalogue. The pipeline asserts at least 60 valid books and three categories.\n\nThe artificial assignment conversion is exactly **1 GBP = 105.50 INR**; INR amounts are rounded to two decimal places. It is not a market exchange rate.\n\nbooks.db has categories and books linked by a primary/foreign key. queries.sql and sql_results.md contain the five queries and actual outputs. The JOIN result is also reproduced with pd.merge and checked for equality.\n', encoding='utf-8')
conn.close()
