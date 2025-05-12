import openai
import json
import product_management as pm
import os 
from dotenv import load_dotenv

load_dotenv()

gpt_api_key = os.getenv("GPT_API_KEY")


client = openai.OpenAI(api_key= gpt_api_key)


image_url1 = "https://www.southernliving.com/thmb/7Pg9J4Q0dyVevZtiq-3p2GnohQA=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Eggs_002_preview-8d532a48790b4a5190e513de08678e7f.jpg"
image_url2 = "https://themodernmilkman.co.uk/_next/image?url=https%3A%2F%2Fimages.ctfassets.net%2Fszr69flitpp6%2F6PXWtJEYg0QPpJZk0TSYKv%2F1a077f282154421fe7060e6b5eb314f4%2FOrganic_Eggs.png&w=640&q=75"

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "List all visible vegetables, fruits, and other basic food items (e.g.  eggs, juice) in this fridge image and return their quantities in valid JSON format only."

                },
                {
                    "type": "image_url",
                    "image_url": { "url": image_url1 }
                }
            ]
        }
    ],
    max_tokens=500
)

raw_output = response.choices[0].message.content.strip()


#Cleaning the raw output from GPT model
if raw_output.startswith("```"):
    raw_output = raw_output.strip("```").strip()
    if raw_output.lower().startswith("json"):
        raw_output = raw_output[4:].strip()



try:
    products = json.loads(raw_output)
except json.JSONDecodeError as e:
    print("Failed to parse GPT response as JSON:", e)
    
    products = {}

for product_name, amount in products.items():
    product_name = product_name.capitalize()
    if pm.is_product_exists(product_name) == -1:
        create_status = pm.creating_product(product_name, location_id=2, quantity_id=2)  # 2 = Fridge, Piece
        if create_status != -1:
            pm.adding_product_to_stock(product_name, amount)
            print(f"Created and added '{product_name}' ({amount}) to stock.")
        else:
            print(f"Failed to create product: {product_name}")
    else:
        previous_amount = pm.previous_stock_amount(product_name)
        if amount > previous_amount:
            add = amount - previous_amount
            pm.adding_product_to_stock(product_name, add)
            print(f"Added '{product_name}' ({add}) to stock.")
        elif amount < previous_amount:
            consumed = previous_amount - amount 
            pm.consuming_product(product_name,consumed)
            print(f"Consumed {product_name} ({consumed}) from stock.")
        else:
            print(f"State is the same")
if not products:
    print("No valid products were processed. Try a clearer fridge image or adjust your prompt.")




