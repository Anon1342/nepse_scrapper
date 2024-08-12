from sqlalchemy import Column, Integer, Float, String,Date
from .database import Base

from datetime import date


class Item(Base): #This allows SQLAlchemy to track the class and map it to a table in the database.
    __tablename__ = 'nepse_stocks6'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Sn = Column(Integer)
    Symbol = Column(String)
    Open_Price_Rs = Column(Float)
    High_Price_Rs = Column(Float)
    Low_Price_Rs = Column(Float)
    Total_Traded_Quantity = Column(Float)
    Total_Traded_Value = Column(Float)
    Total_Trades = Column(Float)
    LTP = Column(Float)
    Previous_Day_Close_Price_Rs = Column(Float)
    Average_Traded_Price_Rs = Column(Float)
    Week_High_52_Rs = Column(Float)
    Week_Low_52_Rs = Column(Float)
    Date = Column(Date)