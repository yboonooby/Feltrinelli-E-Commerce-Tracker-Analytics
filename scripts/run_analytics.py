import os
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

current_date = datetime.now().strftime('%Y-%m-%d')

output_dir = os.path.join('outputs', current_date)

os.makedirs(output_dir, exist_ok=True)

queries = {
    'view_creation': os.path.join('sql', '01_view_creation.sql'),
    'rank_difference': os.path.join('sql', '02_rank_difference.sql'),
    'price_difference': os.path.join('sql', '03_price_difference.sql'),
    'discount_rank_relation': os.path.join('sql', '04_discount_rank_relation.sql')}

def load_sql_query(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def run_pipeline():
    for report_name, sql_file in queries.items():
        if os.path.exists(sql_file):
            query_text = load_sql_query(sql_file)
            
            if 'view_creation' in report_name:
                with engine.begin() as conn:
                    conn.execute(text(query_text))
                print(f"Vista database aggiornata: {report_name}")

            else:
                df = pd.read_sql(query_text, engine)
                file_path = os.path.join(output_dir, f'{report_name}.csv')
                df.to_csv(file_path, index=False)
                print(f"Report generato: {file_path}")
        else:
            print(f"File non trovato: {sql_file}")

if __name__ == '__main__':
    run_pipeline()