# LanceDB Gemini CLI Extension

This extension provides a simple integration with the LanceDB vector database for the Gemini CLI.

## Installation

1.  **Install the Gemini CLI:**
    ```bash
    npm install -g @google/gemini-cli
    ```

2.  **Install the LanceDB extension:**
    ```bash
    gemini extensions install https://github.com/your-github-username/lancedb-gemini-extension
    ```
    *(Note: Replace with the actual URL of the extension repository)*

3.  **Install Python dependencies:**
    ```bash
    pip install -r lancedb-extension/requirements.txt
    ```

## Configuration

No configuration is required. The extension uses a local LanceDB database.

## Usage

You can interact with the LanceDB extension using either natural language or custom commands.

### Natural Language

You can use natural language to create tables, add documents, search, and delete tables.

*   **Create a table:**
    ```
    create a new lancedb table named my_table
    ```
*   **Add a document:**
    ```
    add the document 'this is a test' to the my_table table
    ```
*   **Search for a document:**
    ```
    search for 'a test' in the my_table table
    ```
*   **Delete a table:**
    ```
    delete the lancedb table named my_table
    ```

### Custom Commands

You can also use custom commands for more direct control.

*   **/lancedb:create-table [table_name]**
    *   Creates a new LanceDB table. If no table name is provided, a default table will be created.
*   **/lancedb:add-doc <document> [table_name]**
    *   Adds a document to a LanceDB table. If no table name is provided, the document will be added to the default table.
*   **/lancedb:search <query> [table_name]**
    *   Searches for similar documents in a LanceDB table. If no table name is provided, the search will be performed on the default table.
*   **/lancedb:delete-table <table_name>**
    *   Deletes a LanceDB table.
