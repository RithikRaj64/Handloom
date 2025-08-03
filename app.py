from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from utils.schemas import UserInput, ProductDescription
from utils.prompt import *
from utils.methods import *

from groq import Groq

import os
import json
from dotenv import load_dotenv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

context_store = {}

CATALOG_PATH = "./utils/product_catalog.json"
product_catalog = load_json(CATALOG_PATH)

@app.post("/suggest-tags")
async def suggest_tags_for_new_product(
    image: UploadFile = File(...) 
):
    base64_image = encode_image(image)

    user_prompt = tags_suggestion_prompt["user_prompt"].format(catalog_metadata=product_catalog)

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": tags_suggestion_prompt["sys_prompt"]},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            },
        ],
        model="meta-llama/llama-4-scout-17b-16e-instruct",
    )

    try:
        response = chat_completion.choices[0].message.content.strip()
        return json.loads(response)
    except Exception as e:
        return {"error": "Invalid model response", "raw_response": response, "exception": str(e)}

@app.post("/update-catalog")
def update_catalog(product: ProductDescription):
    catalog = load_json(CATALOG_PATH)
    category = product.category
    new_tags = product.tags

    if category in catalog:
        existing_tags = set(catalog[category])
        updated_tags = list(existing_tags.union(new_tags))
        catalog[category] = updated_tags
    else:
        catalog[category] = new_tags

    save_json(CATALOG_PATH, catalog)
    return {"message": "Catalog updated successfully", "category": category, "tags": catalog[category]}

@app.post("/set_context")
async def set_context(input: UserInput):
    context_store["user_input"] = input
    return {"message": "Context saved"}

@app.post("/recommend")
async def recommend_fashion(
    image: UploadFile = File(...)
):
    input = context_store.get("user_input")
    if not input:
        raise HTTPException(status_code=400, detail="User input context not found. Call /set_context first.")
    
    base64_image = encode_image(image)

    user_prompt = recommendation_prompt["user_prompt"].format(
        event=input.event,
        region=input.region,
        style_preference=input.style_preference,
        catalog_metadata=product_catalog
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": recommendation_prompt["sys_prompt"]},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            },
        ],
        model="meta-llama/llama-4-scout-17b-16e-instruct",
    )

    try:
        response = chat_completion.choices[0].message.content.strip()
        return json.loads(response)
    except Exception as e:
        return {"error": "Invalid model response", "raw_response": response, "exception": str(e)}
