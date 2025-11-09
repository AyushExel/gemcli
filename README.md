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

3.  **Find the extension path:**
    Run `gemini extensions list` to find the installation path for `lancedb-gemini-extension`.

4.  **Navigate to the extension directory:**
    ```bash
    cd <path-to-lancedb-gemini-extension>
    ```
    *(Note: Replace `<path-to-lancedb-gemini-extension>` with the actual path from the previous step)*

5.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

6.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

No configuration is required. The extension uses a local LanceDB database.

## Usage

You can interact with the LanceDB extension using either natural language or custom commands.

### Natural Language

You can use natural language to create tables, add documents, search, and delete tables.

*   **Create a table:**
    ```
    gemini -p "create a new lancedb table named my_table"
    ```
*   **Add a document:**
    ```
    gemini -p "add the document 'this is a test' to the my_table table"
    ```
*   **Search for a document:**
    ```
    gemini -p "search for 'a test' in the my_table table"
    ```
*   **Delete a table:**
    ```
    gemini -p "delete the lancedb table named my_table"
    ```

### Custom Commands

You can also use custom commands for more direct control.

*   **Create a table:**
    ```bash
    gemini -p "/lancedb:create-table my_table"
    ```
*   **Add a document:**
    ```bash
    gemini -p "/lancedb:add-doc 'this is a test document' my_table"
    ```
*   **Search for a document:**
    ```bash
    gemini -p "/lancedb:search 'a test' my_table"
    ```
*   **Delete a table:**
    ```bash
    gemini -p "/lancedb:delete-table my_table"
    ```
