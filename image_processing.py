import openai
import json
import product_management as pm
from best_before_days import guess_best_before

APIKEY=""
client = openai.OpenAI(api_key=APIKEY)


image_url = "https://i.imgur.com/fBWbqVI.jpeg"

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "List all visible vegetables, fruits, and other basic food items (e.g. eggs, juice) in this fridge image and return their quantities in valid JSON format only."

                },
                {
                    "type": "image_url",
                    "image_url": { "url": image_url }
                }
            ]
        }
    ],
    max_tokens=500
)

raw_output = response.choices[0].message.content.strip()
print("\n🧠 GPT-4o raw response:\n", raw_output)

if raw_output.startswith("```"):
    raw_output = raw_output.strip("```").strip()
    if raw_output.lower().startswith("json"):
        raw_output = raw_output[4:].strip()

try:
    products = json.loads(raw_output)
except json.JSONDecodeError as e:
    print("❌ Failed to parse GPT response as JSON:", e)
    print("🔍 Raw response was:", raw_output)
    products = {}

for product_name, amount in products.items():
    best_before_date = guess_best_before(product_name)

    if pm.is_product_exists(product_name) == -1:
        create_status = pm.creating_product(product_name, location_id=2, quantity_id=2)  # 2 = Fridge, Piece
        if create_status != -1:
            pm.adding_product_to_stock(product_name, amount, best_before_date)
            print(f"✅ Created and added '{product_name}' ({amount}) to stock. Best before: {best_before_date}")
        else:
            print(f"❌ Failed to create product: {product_name}")
    else:
        pm.adding_product_to_stock(product_name, amount, best_before_date)
        print(f"✅ Added '{product_name}' ({amount}) to stock. Best before: {best_before_date}")

if not products:
    print("⚠️ No valid products were processed. Try a clearer fridge image or adjust your prompt.")
