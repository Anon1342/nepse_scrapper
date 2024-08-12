from pydantic import BaseModel

from datetime import date

#schema for reading
class Item(BaseModel):
    id:int
    Sn: int 
    Symbol: str
    Open_Price_Rs: float 
    High_Price_Rs: float 
    Low_Price_Rs: float 
    Total_Traded_Quantity: float 
    Total_Traded_Value: float 
    Total_Trades: float 
    LTP: float 
    Previous_Day_Close_Price_Rs: float
    Average_Traded_Price_Rs: float 
    Week_High_52_Rs: float 
    Week_Low_52_Rs: float 
    Date: date

#schema for creating and updating
class ItemCreateUpdate(BaseModel):
    Sn: int 
    Symbol: str
    Open_Price_Rs: float 
    High_Price_Rs: float 
    Low_Price_Rs: float 
    Total_Traded_Quantity: float 
    Total_Traded_Value: float 
    Total_Trades: float 
    LTP: float 
    Previous_Day_Close_Price_Rs: float
    Average_Traded_Price_Rs: float 
    Week_High_52_Rs: float 
    Week_Low_52_Rs: float 
    Date: date

class Config:
        orm_mode = True