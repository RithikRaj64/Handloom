import os
import json
import base64

from fastapi import UploadFile

def encode_image(file: UploadFile) -> str:
    return base64.b64encode(file.file.read()).decode("utf-8")

def load_json(filepath):
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r") as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)