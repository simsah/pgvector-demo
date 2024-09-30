import os
import psycopg2
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
api_key = os.getenv('OPENAI_API_KEY')

# Define the OpenAI client
client = OpenAI(api_key=api_key)


from app.db.connect import create_db_connection

if __name__ == '__main__':
    # Write five example sentences that will be converted to embeddings
    texts = [
        "I like to eat broccoli and bananas.",
        "I ate a banana and spinach smoothie for breakfast.",
        "Chinchillas and kittens are cute.",
        "My sister adopted a kitten yesterday.",
        "Look at this cute hamster munching on a piece of broccoli.",
    ]

    # Get embeddings using the OpenAI API
      # Ensure you set your OpenAI API key
    model = os.getenv('EMBEDDING_MODEL') or "text-embedding-ada-002"  # Default model if not set

    embeddings = []
    for text in texts:
        response = client.embeddings.create(input=text, model=model)
        embeddings.append(response.data[0].embedding)

    # Write text and embeddings to the database
    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        for text, embedding in zip(texts, embeddings):
            cursor.execute(
                "INSERT INTO embeddings (embedding, text) VALUES (%s, %s)",
                (embedding, text)
            )
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while writing to DB", error)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
