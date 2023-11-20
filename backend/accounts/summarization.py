import os
import openai
import time
from authentication.settings import API_KEY
from accounts.models import Summary

def split_text_into_chunks(file_text, chunk_size):
    words = file_text.split()  # Split the text into words
    chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
    return [' '.join(chunk) for chunk in chunks]


def summarize(file_text):

    chunk_size = 200

    

    # Split the content into chunks of 200 words
    chunks = split_text_into_chunks(file_text, chunk_size)

    # Print each chunk
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}:\n{chunk}\n")




    openai.api_key =API_KEY

    # Initialize the messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes content provided."}
    ]

    # Process each chunk and generate response
    chunk_messages = []
    for i, chunk in enumerate(chunks):
        chunk_messages.append({"role": "user", "content": chunk + " Remember this text. I will provide you further text"})
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages + chunk_messages,
            temperature=0.7,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        print(f"Chunk {i+1} processed ...\n")
        time.sleep(20)  # Introduce a 20-second delay before sending the next request
        print("Processing next chunk ...")

    # Ask GPT-3 to generate headings and subheadings for the entire content
    print("\nSending prompt to chatgpt\n")
    prompt = "Now that you have all the text, generate a detailed summary that covers all the important and technical details"
    final_message = chunk_messages + [{"role": "user", "content": prompt}]

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages + final_message,
        temperature=0.7,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the final response containing headings
    output = response.choices[0].message.content
    print("Generated Summary:", output)

    return output


# # Open the file in read mode
# with open('backend/authentication/speech.txt', 'r') as file:
#     # Read the entire contents of the file
#     file_text = file.read()
#     summarize(file_text)


