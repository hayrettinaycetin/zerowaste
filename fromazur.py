from azure.storage.blob import BlobServiceClient
import openai
from dotenv import load_dotenv
import os


load_dotenv()

connect_str = os.getenv("AZURE_CONNECTION_STRING")
openai_api_key = os.getenv("OPENAI_API_KEY")
container_name = os.getenv("AZURE_CONTAINER_NAME")

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(container_name)
account_name = blob_service_client.account_name


blob_urls = []
for blob in container_client.list_blobs():
    blob_name = blob.name
    url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}"
    blob_urls.append(url)


client = openai.OpenAI(
    client=openai.OpenAI(api_key=openai_api_key)
)


for url in blob_urls:
    print(f"\n Analyzing: {url}")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "List all visible vegetables and fruits in this fridge image and return the count of each in JSON format only. Do not explain anything else."},
                        {"type": "image_url", "image_url": {"url": url}}
                    ]
                }
            ],
            max_tokens=500
        )
        print(" JSON Result:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f" Error analyzing {url}: {e}")
