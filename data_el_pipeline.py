import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import inspect, text


def extract_data(location: str):
    df = pd.read_csv(location)
    df = df.set_index(
        "Job ID"
    )  # set index is needed to avoid creating index column in postgresql

    return df


def search_result_cleaning(df: pd.DataFrame, profession: str):
    """return cleaned dataframe with Job Id as index"""
    df.drop_duplicates(subset="Job ID", inplace=True)
    df["Job ID"] = df["Job ID"].astype("int")
    df["Search Term"] = profession
    df["Publish Date"] = pd.to_datetime(df["Publish Date"])

    return df.set_index(
        "Job ID"
    )  # set index is needed to avoid creating index column in postgresql


def change_data_capture(
    df, target_table: str = "job_search_results", primary_key: str = "Job ID"
) -> pd.DataFrame:
    """change data capture to postgresql"""
    df = df.reset_index()
    table_name = target_table
    postgres_url = "postgresql+psycopg2://root:root@localhost:5432/jobs_database"
    engine = create_engine(postgres_url)
    existing_jobs = pd.read_sql(
        text(f'SELECT "{primary_key}" FROM "{table_name}"'), engine.connect()
    )

    delta_index = df.join(existing_jobs, on="Job ID", how="left", rsuffix="_right")[
        f"{primary_key}_right"
    ].isna()
    print(f"Number of new records: {delta_index.sum()}")

    delta_df = df[delta_index]

    return delta_df.set_index("Job ID")


def load_data(user, password, host, port, db, table_name, df):
    """load data into postgresql"""
    postgres_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(postgres_url)

    inspector = inspect(engine)
    if not inspector.has_table(f"{table_name}"):
        print(f"Table does not exist, creating table {table_name}")
        df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")

    df.to_sql(name=table_name, con=engine, if_exists="append")


if __name__ == "__main__":
    df_extracted = extract_data("jobs.csv")
    load_data(
        user="root",
        password="root",
        host="localhost",
        port="5432",
        db="jobs_database",
        table_name="job_search_results",
        df=df_extracted,
    )
