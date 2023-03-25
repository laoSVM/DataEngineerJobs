import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import inspect

def extract_data(location: str):

    df = pd.read_csv(location)
    df = df.set_index("Job ID") # set index is needed to avoid creating index column in postgresql

    return df

def transform_data(df: pd.DataFrame, profession: str):
    df['Search Term'] = profession
    df['Publish Date'] = pd.to_datetime(df['Publish Date'])

    return df

def load_data(user, password, host, port, db, table_name, df):

    postgres_url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'
    engine = create_engine(postgres_url)

    inspector = inspect(engine)
    if not inspector.has_table(f'{table_name}'):
        print(f'Table does not exist, creating table {table_name}')
        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')


if __name__ == '__main__':

    df = extract_data("jobs.csv")
    load_data(
        user = "root",
        password = "root",
        host = "localhost",
        port = "5432",
        db = "jobs_database",
        table_name = "job_search_results",
        df = df
        )
