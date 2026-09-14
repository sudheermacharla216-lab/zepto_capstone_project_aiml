SELECT title, rating FROM books WHERE in_stock=1 AND rating>=4;

SELECT title, price_gbp FROM books ORDER BY price_gbp DESC, book_id LIMIT 10;

SELECT DISTINCT rating FROM books ORDER BY rating;

SELECT title, price_gbp FROM books WHERE price_gbp BETWEEN 10 AND 20 ORDER BY book_id;

SELECT b.book_id, b.title, b.rating, c.category_name
 FROM books b JOIN categories c ON b.category_id=c.category_id
 WHERE b.rating IN (4,5) ORDER BY b.book_id;