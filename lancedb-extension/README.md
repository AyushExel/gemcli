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
