import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

df = pd.read_csv('feltrinelli_data.csv')

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

df_books = df[['isbn_code', 'title', 'author']].drop_duplicates(subset=['isbn_code'])

existing_isbns = pd.read_sql("SELECT isbn_code FROM books", engine)['isbn_code'].tolist()
new_books = df_books[~df_books['isbn_code'].isin(existing_isbns)]

if not new_books.empty:
    new_books.to_sql('books', engine, index=False, if_exists='append')

df['snapshot_date'] = pd.to_datetime('today').strftime('%Y-%m-%d')
df_rankings = df[['snapshot_date', 'isbn_code', 'rank', 'stars', 'reviews', 'price', 'discount', 'old_price']]
df_rankings.to_sql('daily_rankings', engine, index=False, if_exists='append')

print("Uploading done.")