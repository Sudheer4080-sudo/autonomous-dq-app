
import sqlalchemy
import sqlite3
import pandas as pd
from sqlalchemy import create_engine

import psycopg2
import pymysql
import mysql.connector
import snowflake.connector
import pyodbc
import cx_Oracle
import redshift_connector
from pyathena import connect as athena_connect
from google.cloud import bigquery

def get_sqlalchemy_engine(db_type, **kwargs):
    if db_type == "postgresql":
        return create_engine(f"postgresql+psycopg2://{kwargs['user']}:{kwargs['password']}@{kwargs['host']}:{kwargs['port']}/{kwargs['database']}")
    elif db_type == "mysql":
        return create_engine(f"mysql+pymysql://{kwargs['user']}:{kwargs['password']}@{kwargs['host']}:{kwargs['port']}/{kwargs['database']}")
    elif db_type == "sqlite":
        return create_engine(f"sqlite:///{kwargs['filepath']}")
    elif db_type == "snowflake":
        return snowflake.connector.connect(
            user=kwargs['user'],
            password=kwargs['password'],
            account=kwargs['account'],
            warehouse=kwargs['warehouse'],
            database=kwargs['database'],
            schema=kwargs['schema']
        )
    elif db_type == "sqlserver":
        conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={kwargs['host']},{kwargs['port']};DATABASE={kwargs['database']};UID={kwargs['user']};PWD={kwargs['password']}"
        return pyodbc.connect(conn_str)
    elif db_type == "oracle":
        dsn = cx_Oracle.makedsn(kwargs['host'], kwargs['port'], sid=kwargs['sid'])
        return cx_Oracle.connect(user=kwargs['user'], password=kwargs['password'], dsn=dsn)
    elif db_type == "redshift":
        return redshift_connector.connect(
            user=kwargs['user'],
            password=kwargs['password'],
            host=kwargs['host'],
            port=int(kwargs['port']),
            database=kwargs['database']
        )
    elif db_type == "athena":
        return athena_connect(s3_staging_dir=kwargs['s3_staging_dir'], region_name=kwargs['region'])
    elif db_type == "bigquery":
        client = bigquery.Client()
        return client
    else:
        raise ValueError("Unsupported database type")

def preview_table(engine_or_conn, table_name, limit=5):
    if isinstance(engine_or_conn, sqlalchemy.engine.base.Engine):
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        return pd.read_sql(query, engine_or_conn)
    elif isinstance(engine_or_conn, bigquery.Client):
        query = f"SELECT * FROM `{table_name}` LIMIT {limit}"
        return engine_or_conn.query(query).to_dataframe()
    elif hasattr(engine_or_conn, 'cursor'):
        cursor = engine_or_conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        return pd.DataFrame(data, columns=columns)
    else:
        raise ValueError("Unsupported connection object")
