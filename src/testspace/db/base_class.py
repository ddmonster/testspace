from sqlalchemy.ext.declarative import declarative_base
from src.testspace.components.cache import __all__
# from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Table
__all__ = ["Base"]
Base = declarative_base()

