from typing import Any

from sqlalchemy import create_engine
from sqlalchemy import inspect

class Supabase:
    engine = None
    schema = []

    def connect(self, connection_url: str) -> None:
        if self.engine is None:
            try:
                self.engine = create_engine(connection_url, pool_pre_ping=True)
            except Exception as e:
                raise e

    def fetch_schema(self) -> None:
        if self.engine is None:
            raise NotImplementedError

        with self.engine.connect() as conn:
            inspector = inspect(conn)

            try:
                tables = inspector.get_table_names(schema="public")
                for table in tables:
                    table_info = {"name": table, "columns": []}
                    columns = inspector.get_columns(table)

                    for column in columns:
                        table_info["columns"].append(dict(name=column["name"], type=column["type"], nullable=column["nullable"]))

                    self.schema.append(table_info)
            except Exception as e:
                raise RuntimeError

    def get_schema_as_json(self) -> list[Any]:
        return self.schema

    def get_schema_as_text(self) -> str:
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