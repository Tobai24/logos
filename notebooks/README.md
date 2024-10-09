# 📁 **Notebook Folder**

This folder contains the development and experimental implementation of the RAG (Retrieval-Augmented Generation) system for the app. Below are details on the files and their contents:

### 📒 **Notebooks**

1. **`analysis.ipynb`**

   - **Description**: This notebook implements the RAG system using the **MiniSearch** retrieval engine (see `minsearch.py` for the retrieval system).
   - **Purpose**: Demonstrates how MiniSearch works for retrieval-based question answering, using minimalistic tools like `sklearn` and `pandas`.

2. **`final.ipynb`**

   - **Description**: This notebook implements the RAG system using **Elasticsearch**, focusing on **keyword-based search** for retrieval.
   - **Purpose**: Explores how Elasticsearch handles retrieval with only keyword search, highlighting performance and implementation steps.

3. **`semantic.ipynb`**
   - **Description**: This notebook explores **vector-based search** using **Elasticsearch** for the RAG system.
   - **Purpose**: Demonstrates how vector search retrieves documents based on semantic similarity using dense embeddings, improving retrieval accuracy.

### 📜 **Python Script**

- **`minsearch.py`**
  - **Description**: A minimalistic text search engine written using `sklearn` and `pandas`. This lightweight search library supports document indexing with text and keyword fields, filtering, and boosting.
  - **Purpose**: Used for implementing the RAG system in `analysis.ipynb`.
  - **More Information**: To learn more about MiniSearch, check out the [MiniSearch repository](https://github.com/alexeygrigorev/minsearch).

### 📂 **Embeddings**

- **`embedding.json`**
  - **Description**: This file contains pre-generated embeddings to save time during retrieval. Since creating embeddings takes approximately **2 hours**, the embeddings have been saved as a **JSON** file for convenience.
  - **Usage**: You can use this file directly without needing to re-create the embeddings. However, if you want to generate them from scratch, the steps for creating embeddings are documented in the **`semantic.ipynb`** notebook.

For more details on the retrieval systems and how each one contributes to the RAG system, explore each notebook!
