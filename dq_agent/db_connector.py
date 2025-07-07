import pandas as pd
from sqlalchemy import create_engine

def load_from_postgres(host, db, user, password, table):
    engine = create_engine(f"postgresql://{user}:{password}@{host}/{db}")
    return pd.read_sql_table(table, con=engine)

def load_from_mysql(host, db, user, password, table):
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db}")
    return pd.read_sql_table(table, con=engine)
