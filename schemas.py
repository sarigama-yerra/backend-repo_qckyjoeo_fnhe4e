"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Example schemas (you can keep these if useful elsewhere)

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Portfolio-specific schemas

class Contactmessage(BaseModel):
    """
    Contact messages submitted from the portfolio site
    Collection name: "contactmessage"
    """
    name: str = Field(..., description="Sender name")
    email: EmailStr = Field(..., description="Sender email")
    subject: Optional[str] = Field(None, description="Subject line")
    message: str = Field(..., min_length=1, description="Message body")

class Project(BaseModel):
    """
    Portfolio projects metadata
    Collection name: "project"
    """
    title: str
    slug: str
    category: str = Field(..., description="e.g., Industrial, UI, Furniture, CMF")
    thumbnail_url: Optional[str] = None
    hero_url: Optional[str] = None
    summary: Optional[str] = None
    tools: Optional[List[str]] = None
    year: Optional[int] = None
    credits: Optional[str] = None
