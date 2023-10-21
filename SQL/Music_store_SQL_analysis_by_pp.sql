
-- 1. Who is the senior most employee based on job title?

SELECT title FROM employee ORDER BY levels DESC LIMIT 1

-- 1. 2. Which countries have the most Invoices?

SELECT billing_country, count(billing_country) FROM invoice GROUP BY billing_country ORDER BY count(billing_country) DESC LIMIT 1

-- 3. What are top 3 values of total invoice?

SELECT total FROM invoice ORDER BY total DESC LIMIT 3

-- 4. Which city has the best customers? We would like to throw a promotional Music
-- Festival in the city we made the most money. Write a query that returns one city that
-- has the highest sum of invoice totals. Return both the city name & sum of all invoice
-- totals

SELECT billing_city, sum(total) AS total_invoice FROM invoice GROUP BY billing_city ORDER BY sum(total) DESC LIMIT 1

-- 5. Who is the best customer? The customer who has spent the most money will be
-- declared the best customer. Write a query that returns the person who has spent the
-- most money

SELECT c.first_name as first_name, c.last_name as last_name, sum(total) FROM customer as c JOIN invoice ON c.customer_id=invoice.customer_id GROUP BY c.customer_id ORDER BY sum(total) DESC limit 1

-- 1. Write query to return the email, first name, last name, & Genre of all Rock Music
-- listeners. Return your list ordered alphabetically by email starting with A

SELECT c.email, c.first_name, c.last_name, g.name FROM Customer AS c 
JOIN invoice ON c.customer_id=invoice.customer_id
JOIN invoice_line ON invoice.invoice_id=invoice_line.invoice_id
JOIN track ON invoice_line.track_id=track.track_id
Join genre AS g ON track.genre_id=g.genre_id
WHERE g.name='Rock'

-- 2. Let's invite the artists who have written the most rock music in our dataset. Write a 
-- query that returns the Artist name and total track count of the top 10 rock bands

SELECT artist.name, count(track_id) FROM artist 
JOIN album ON artist.artist_id=album.artist_id
JOIN track ON album.album_id=track.album_id
JOIN genre ON track.genre_id=genre.genre_id
WHERE genre.name='Rock' 
GROUP BY artist.name
ORDER BY count(track_id) DESC
LIMIT 10

-- 3. Return all the track names that have a song length longer than the average song length. 
-- Return the Name and Milliseconds for each track. Order by the song length with the 
-- longest songs listed first

SELECT name,milliseconds FROM track
WHERE milliseconds>(SELECT AVG(milliseconds) FROM track)
ORDER BY milliseconds DESC


-- 1. Find how much amount spent by each customer on artists? Write a query to return
-- customer name, artist name and total spent

WITH best_selling_artist AS (
	SELECT artist.artist_id AS artist_id, artist.name AS artist_name, SUM(invoice_line.unit_price*invoice_line.quantity) AS total_sales
	FROM invoice_line
	JOIN track ON track.track_id = invoice_line.track_id
	JOIN album ON album.album_id = track.album_id
	JOIN artist ON artist.artist_id = album.artist_id
	GROUP BY 1
	ORDER BY 3 DESC
)
SELECT c.customer_id, c.first_name, c.last_name, bsa.artist_name, SUM(il.unit_price*il.quantity) AS amount_spent
FROM invoice i
JOIN customer c ON c.customer_id = i.customer_id
JOIN invoice_line il ON il.invoice_id = i.invoice_id
JOIN track t ON t.track_id = il.track_id
JOIN album alb ON alb.album_id = t.album_id
JOIN best_selling_artist bsa ON bsa.artist_id = alb.artist_id
GROUP BY 1,2,3,4
ORDER BY 1,5 DESC,4;

-- 2. We want to find out the most popular music Genre for each country. We determine the 
-- most popular genre as the genre with the highest amount of purchases. Write a query 
-- that returns each country along with the top Genre. For countries where the maximum 
-- number of purchases is shared return all Genres

WITH tt AS (
	SELECT c.country,g.name AS genre,count(invoice_line.track_id) as track,
	ROW_NUMBER() OVER (PARTITION BY c.country ORDER BY count(invoice_line.track_id) DESC) as rowno
	FROM customer AS c 
    JOIN invoice ON c.customer_id=invoice.customer_id
    JOIN invoice_line ON invoice.invoice_id=invoice_line.invoice_id
    JOIN track ON invoice_line.track_id=track.track_id
    Join genre AS g ON track.genre_id=g.genre_id
    GROUP BY 1,2
    ORDER BY 1,3 DESC
)

SELECT * FROM tt WHERE rowno<=1

-- 3. Write a query that determines the customer that has spent the most on music for each 
-- country. Write a query that returns the country along with the top customer and how
-- much they spent. For countries where the top amount spent is shared, provide all 
-- customers who spent this amount

WITH kt AS (
	SELECT c.country,c.first_name, c.last_name,SUM(invoice_line.quantity*track.milliseconds) as time,
	ROW_NUMBER() OVER (PARTITION BY c.country ORDER BY SUM(invoice_line.quantity*track.milliseconds) DESC) as rowno
	FROM customer AS c 
    JOIN invoice ON c.customer_id=invoice.customer_id
    JOIN invoice_line ON invoice.invoice_id=invoice_line.invoice_id
    JOIN track ON invoice_line.track_id=track.track_id
    GROUP BY 1,2,3
    ORDER BY 1,4 DESC
)

SELECT * FROM kt WHERE rowno<=1




