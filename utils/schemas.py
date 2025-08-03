from pydantic import BaseModel, Field
from typing import List

class UserInput(BaseModel):
    event: str 
    region: str 
    style_preference: str

class ProductDescription(BaseModel):
    category: str
    tags: List[str]