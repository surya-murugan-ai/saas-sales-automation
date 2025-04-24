# from sqlalchemy import Column, Integer, String, Text
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class Lead(Base):
#     __tablename__ = "leads"
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     position = Column(String)
#     company = Column(String)
#     linkedin_url = Column(String)
#     email = Column(String)
#     phone = Column(String)
#     enriched_data = Column(Text)
#     status = Column(String, default="new")

from pydantic import BaseModel
from typing import Optional


class Lead(BaseModel):
    name: str
    company: str
    linkedin_url: str
    company_url: Optional[str]


class EnrichedLead(Lead):
    email: Optional[str]
    phone: Optional[str]
    personalized_profile: str
    outreach_message: str
