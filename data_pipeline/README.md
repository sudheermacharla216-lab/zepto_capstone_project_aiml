# Data pipeline
Run from the repository root: `python data_pipeline/pipeline.py`.
Install the consolidated root requirements first. The first five listing pages are scraped with requests and BeautifulSoup; detail pages supply category and availability. Unparseable required fields are dropped and logged in rejected_rows.csv because inventing prices/ratings would distort the catalogue. The pipeline asserts at least 60 valid books and three categories.

The artificial assignment conversion is exactly **1 GBP = 105.50 INR**; INR amounts are rounded to two decimal places. It is not a market exchange rate.

books.db has categories and books linked by a primary/foreign key. queries.sql and sql_results.md contain the five queries and actual outputs. The JOIN result is also reproduced with pd.merge and checked for equality.
