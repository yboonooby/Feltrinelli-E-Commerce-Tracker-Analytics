# Feltrinelli E-Commerce Tracker & Analytics

An E2E pipeline project that takes regularly the top 100 books of the day from the Feltrinelli website, uploads it to PostgreSQL and runs queries to analyze the rank and price changes, and also analyzes the relation between price change and rank change.

## Tech Stack

* **ETL / Scripting:** Python (Pandas, BeautifulSoup, Requests)
* **Database:** PostgreSQL
* **Database Driver / ORM:** SQLAlchemy, psycopg2
* **Database GUI:** DBeaver
* **Version Control:** Git

## Pipeline Architecture

**Extraction & Cleaning (convert.py)**
Requests the HTML from the Feltrinelli website in the daily book ranking ("https://www.lafeltrinelli.it/classifica/libri/1day/sold?page=1-3"), isolates each book link and then requests the HTML of the page of each book, extracting the info for each book. Finally, it uploads the info into a .csv file ('feltrinelli_data.csv') in the same folder.

**Database & Upload (upload_to_db.py):**
Takes the .csv  and uploads it to PostgreSQL into the 'books' (title, author, isbn_code) and 'daily_rankings' (snapshot_date, isbn_code, rank, stars, reviews, price, discount, old_price) tables.

**SQL Analytics & Output Saving (sql/, run_analytics.py):**
Runs four queries (sql/) to analyze and track the book's changes in the leaderboard and price. Then saves the outputs in a folder (outputs/) with the current date.

## Output Folder & Queries

### Query 01 ('02_rank_difference.sql')
Outputs data relative to the books' leaderboard, including:

* **Date of the ranking**
* **ISBN Code**
* **Ranking**
* **Leaderboard jump**

### Query 02 ('03_price_difference.sql')
Outputs data relative to the books' price analytics, including:

* **Date of the ranking**
* **ISBN Code**
* **Full Price**
* **Current Price**
* **Price of the Day Prior**
* **Price Difference** (between current price and prior price)
* **Lowest Price** (of all time recorded)
* **Highest Discount** (of all time recorded)

### Query 03 ('04_discount_rank_relation.sql')
Outputs data relative to both the books' price analytics and leaderboard:

* **Date of the ranking**
* **ISBN Code**
* **Discount Difference 1** (between current discount and the one of the day prior)
* **Discount Difference 2** (between discount of the day prior and the one even before)
* **Current Discount**
* **Rank**
* **Rank Difference** (between current and the one of the day prior)