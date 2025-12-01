from typing import Any

from sqlalchemy import create_engine
from sqlalchemy import inspect

class Supabase:
    engine = None
    schema = []

    def connect(self, connection_url: str) -> None:
        """
        Initialize a connection to the Supabase database

        :param connection_url: Supabase database connection URL
        :return: None
        """

        if self.engine is None:
            try:
                # Create PG engine
                self.engine = create_engine(connection_url, pool_pre_ping=True)
            except Exception as e:
                raise e

    def fetch_schema(self) -> None:
        """
        Fetch schema from Supabase database

        :return: None
        """
        if self.engine is None:
            # Throw an error if function is called before engine in initialized
            raise NotImplementedError

        with self.engine.connect() as conn:
            inspector = inspect(conn)

            try:
                # Fetch all tables in database
                tables = inspector.get_table_names(schema="public")

                # Construct the simplified list of database tables and columns
                for table in tables:
                    table_info = {"name": table, "columns": []}
                    columns = inspector.get_columns(table)

                    for column in columns:
                        table_info["columns"].append(dict(name=column["name"], type=column["type"], nullable=column["nullable"]))

                    self.schema.append(table_info)
            except Exception as e:
                raise RuntimeError

    def get_schema_as_json(self) -> list[Any]:
        """
        Get schema as JSON

        :return: List of tables
        """
        return self.schema

    def get_schema_as_text(self) -> str:
        """
        Get schema as text
        :return: Database schema as text
        """

        schema_raw = ""

        for item in self.schema:
            schema_raw += f"Table: {item['name']} \n\n"
            schema_raw += f"Columns: \n"

            for column in item["columns"]:
                schema_raw += f"- {column['name']}: {column['type']}"
                if column['nullable']:
                    schema_raw += ", Nullable "
                schema_raw += f"\n"

            schema_raw += "\n\n"
            schema_raw += "-----------------"
            schema_raw += "\n\n"

        return schema_raw