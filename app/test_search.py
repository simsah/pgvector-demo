import os
import numpy as np  # Make sure to import NumPy if you haven't already
from app.db.connect import create_db_connection
from dotenv import load_dotenv
from openai import OpenAI

if __name__ == '__main__':
    # This script is used to test the embedding model and the
    # cosine similarity function within the database.

    text = "Did anyone adopt a cat this weekend?"

    # Load environment variables from .env file
    load_dotenv()

    # Get the API key from the environment
    api_key = os.getenv('OPENAI_API_KEY')
    # Ensure you set your OpenAI API key
    model = os.getenv('EMBEDDING_MODEL') or "text-embedding-ada-002"  # Default model if not set

    # Define the OpenAI client
    client = OpenAI(api_key=api_key)

    # Get embeddings for the input text
    response = client.embeddings.create(input=text, model=model)
    embedding = response.data[0].embedding

    # Convert the embedding to a PostgreSQL-compatible array
    embedding_array = np.array(embedding).tolist()  # Convert to list

    connection = create_db_connection()
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute(f"""
                SELECT text, 1 - (embedding <=> %s::vector) AS cosine_similarity
                FROM embeddings
                ORDER BY cosine_similarity DESC
                LIMIT 3
            """, (embedding_array,))  # Use parameterized query to prevent SQL injection

            for r in cursor.fetchall():
                print(f"Text: {r[0]}; Similarity: {r[1]}")
        except Exception as error:
            print("Error while querying the database:", error)
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to create a database connection.")
