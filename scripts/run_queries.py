"""
Run M3 business questions using DuckDB.
"""

import os

import duckdb

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SQL_FILE = os.path.join(BASE_DIR, "sql", "business_questions.sql")


def run_queries():
    """Execute the business questions."""

    with open(SQL_FILE, "r", encoding="utf-8") as file:
        sql = file.read()

    # Split the SQL file into individual queries.
    queries = [query.strip() for query in sql.split(";") if query.strip()]

    connection = duckdb.connect()

    for index, query in enumerate(queries, start=1):

        print("\n" + "=" * 60)
        print(f"Business Question {index}")
        print("=" * 60)

        result = connection.execute(query).df()

        print(result.to_string(index=False))

    connection.close()


if __name__ == "__main__":
    run_queries()
