from pydantic import BaseModel
from typing import List

class FAQItem(BaseModel):
    """Schema for a single FAQ item with question and answer"""
    question: str
    answer: str

class FAQCategory(BaseModel):
    """Schema for a category of FAQ items"""
    title: str
    items: List[FAQItem]

class FAQResponse(BaseModel):
    """Schema for the complete FAQ response"""
    categories: List[FAQCategory]
