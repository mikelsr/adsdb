import pandas as pd
from sqlalchemy import create_engine


from zones.config import config
from zones.formatted.formatter import Formatter
from zones.trusted.processes import data_quality_processes


class Cleaner:
    @staticmethod
    def load_data(db_name, use_config=config):
        tables_query = "SELECT table_name FROM information_schema.tables WHERE table_name LIKE 'formatted%%';"

        postgres_access = "postgresql://{}:{}/{}".format(
            use_config["POSTGRES"]["Host"], use_config["POSTGRES"]["Port"], db_name
        )
        engine = create_engine(postgres_access)
        tables = engine.execute(tables_query).fetchall()
        dfs = []
        for table_name in tables:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, con=engine)
            df.drop("index", axis=1, inplace=True)
            dfs.append(df)
        return dfs

    @staticmethod
    def clean_data(df):
        for process in data_quality_processes:
            process(df)

    @staticmethod
    def store(df, db_name, table_name):
        Formatter.store(df, db=db_name, table=table_name)
