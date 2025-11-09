import lancedb
import argparse
import json
import sys
import pyarrow as pa
import numpy as np
import google.generativeai as genai
import os

# Define constants for the LanceDB client
DEFAULT_TABLE = "default_global_table"
DB_URI = "./lancedb"
VECTOR_DIM = 768 # Dimension for Gemini embedding model
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class NumpyEncoder(json.JSONEncoder):
    """ Custom JSON encoder for numpy arrays """
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def get_db():
    """ Connect to the LanceDB database """
    return lancedb.connect(DB_URI)

def create_table(args):
    """ Create a new LanceDB table with a fixed schema """
    db = get_db()
    table_name = args.table_name
    try:
        schema = pa.schema(
            [
                pa.field("vector", pa.list_(pa.float32(), VECTOR_DIM)),
                pa.field("text", pa.string()),
            ]
        )
        db.create_table(table_name, schema=schema)
        print(json.dumps({"status": "success", "message": f"Table '{table_name}' created."}))
    except ValueError:
        print(json.dumps({"status": "error", "message": f"Table '{table_name}' already exists."}))

def add_doc(args):
    """ Add a document to a LanceDB table """
    db = get_db()
    table_name = args.table_name
    if not table_name:
        table_name = DEFAULT_TABLE

    try:
        table = db.open_table(table_name)
    except FileNotFoundError:
        # If the table doesn't exist, create it with the fixed schema
        schema = pa.schema(
            [
                pa.field("vector", pa.list_(pa.float32(), VECTOR_DIM)),
                pa.field("text", pa.string()),
            ]
        )
        table = db.create_table(table_name, schema=schema)

    # Create a vector from the document string
    result = genai.embed_content(model="models/embedding-001",
                                 content=args.document,
                                 task_type="retrieval_document",
                                 output_dimensionality=VECTOR_DIM)
    vector = result["embedding"]

    table.add([{"vector": vector, "text": args.document}])
    print(json.dumps({"status": "success", "message": "Document added."}))

def search(args):
    """ Search for similar documents in a LanceDB table """
    db = get_db()
    table_name = args.table_name
    if not table_name:
        table_name = DEFAULT_TABLE
    try:
        table = db.open_table(table_name)
    except FileNotFoundError:
        print(json.dumps({"status": "error", "message": f"Table '{table_name}' not found."}))
        return

    # Create a vector from the query string
    result = genai.embed_content(model="models/embedding-001",
                                 content=args.query,
                                 task_type="retrieval_query",
                                 output_dimensionality=VECTOR_DIM)
    vector = result["embedding"]

    # Perform the search and return the results as JSON
    results = table.search(vector).limit(5).to_pandas().to_dict(orient="records")
    print(json.dumps(results, cls=NumpyEncoder))


def delete_table(args):
    """ Delete a LanceDB table """
    db = get_db()
    table_name = args.table_name
    if not table_name:
        print(json.dumps({"status": "error", "message": "Table name is required."}))
        return
    try:
        db.drop_table(table_name)
        print(json.dumps({"status": "success", "message": f"Table '{table_name}' deleted."}))
    except ValueError:
        # Handle the case where the table doesn't exist
        print(json.dumps({"status": "info", "message": f"Table '{table_name}' not found, skipping."}))

def main():
    """ Main function to parse arguments and call the appropriate function """
    parser = argparse.ArgumentParser(description="LanceDB CLI client.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create subparsers for each command
    create_parser = subparsers.add_parser("create_table")
    create_parser.add_argument("table_name", nargs='?', default=DEFAULT_TABLE)
    create_parser.set_defaults(func=create_table)

    add_parser = subparsers.add_parser("add_doc")
    add_parser.add_argument("document")
    add_parser.add_argument("--table_name", default=DEFAULT_TABLE)
    add_parser.set_defaults(func=add_doc)

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("query")
    search_parser.add_argument("--table_name", default=DEFAULT_TABLE)
    search_parser.set_defaults(func=search)

    delete_parser = subparsers.add_parser("delete_table")
    delete_parser.add_argument("table_name")
    delete_parser.set_defaults(func=delete_table)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
