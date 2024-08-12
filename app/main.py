from fastapi import FastAPI, Depends, status, Response, HTTPException
from fastapi.responses import JSONResponse
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm  import Session
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.firefox.service import Service as FirefoxService

import time
import pandas as pd
import re


from lxml import html

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    
    finally:
        db.close()




@app.get('/stock')
def get_stock(skip:int=0, limit:int=10,db:Session = Depends(get_db)):
    stocks = db.query(models.Item).all()
    return stocks[skip:skip+limit]

@app.get('/stock/{id}')
def get_stock_id(id:int,db:Session= Depends(get_db)):
    stocks = db.query(models.Item).filter(models.Item.id == id).first()
    if not stocks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'Stock with {id} not found')
    return stocks


#perfoming update operations
@app.put('/stock/{id}')
def update_item(id:int,request: schemas.ItemCreateUpdate, db:Session =Depends(get_db)):
    update_data = request.dict()
    # if 'id' in update_data:
    #     del update_data['id']
    db.query(models.Item).filter(models.Item.id == id).update(update_data)
    db.commit()
    return{'updated'}


@app.get('/stocks/{date}')
def get_date(date:str,db:Session= Depends(get_db)):
    try:
        date_obj = datetime.strptime(date, "%d-%m-%Y").date()
    except ValueError:
        return{'error':'Return the date in valid date format. Use YYYY-MM-DD'}
    
    stock_date = db.query(models.Item).filter(models.Item.Date == date_obj).all()
    if stock_date:
        return stock_date
    
    if not stock_date:
    
        # options.add_argument('--disable-gpu')  
        # options.add_argument('--no-sandbox') 
        # options.add_argument('--disable-dev-shm-usage')  
        # service = webdriver.ChromeService(executable_path="C:\Program Files (x86)\chromedriver.exe")
        # driver = webdriver.Chrome(service=service) 
        service = webdriver.FirefoxService(executable_path="C:\Program Files (x86)\geckodriver.exe")
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(service=service,options=options) 
        url = 'https://www.nepalstock.com/today-price'
        driver.get(url)
        # time.sleep(10)

        
        search_box = WebDriverWait(driver,10).until( #this code makes the program to wait for 10 seconds so that our element can be fully loaded 
        EC.element_to_be_clickable((By.XPATH,'/html/body/app-root/div/main/div/app-today-price/div/div[2]/div[1]/div[1]/div/input'))
        )
        # search_box = driver.find_element(By.XPATH, '/html/body/app-root/div/main/div/app-today-price/div/div[2]/div[1]/div[1]/div/input')
        # driver.implicitly_wait(10)
        search_box.clear()
        # driver.implicitly_wait(10)
        search_box.send_keys(date_obj.strftime("%m-%d-%Y"))
        
        

        
        # search_box.send_keys(Keys.RETURN)
        # # driver.implicitly_wait(10)
        # time.sleep(5)
        # link2 = WebDriverWait(driver,10).until( #this code makes the program to wait for 10 seconds so that our element can be fully loaded 
        # EC.presence_of_element_located((By.XPATH,'/html/body/app-root/div/main/div/app-today-price/div/div[2]/div[1]/div[3]/select'))
        # )
        link2 = driver.find_element(By.XPATH, '/html/body/app-root/div/main/div/app-today-price/div/div[2]/div[1]/div[3]/select')
        link2.click()

        # link3 = WebDriverWait(driver,10).until( #this code makes the program to wait for 10 seconds so that our element can be fully loaded 
        # EC.presence_of_element_located((By.XPATH,'/html/body/app-root/div/main/div/app-today-price/div/div[2]/div[1]/div[3]/select/option[6]'))
        # )
        link3 = driver.find_element(By.XPATH, '/html/body/app-root/div/main/div/app-today-price/div/div[2]/div[1]/div[3]/select/option[6]')
        link3.click()


        filter_button = WebDriverWait(driver,10).until( #this code makes the program to wait for 10 seconds so that our element can be fully loaded 
        EC.element_to_be_clickable((By.XPATH,'/html/body/app-root/div/main/div/app-today-price/div/div[2]/div[1]/div[4]/button[1]'))
        )
    
        filter_button.click()
        time.sleep(10)
        


        # time.sleep(10)
        # filter_button = driver.find_element(By.XPATH, '/html/body/app-root/div/main/div/app-today-price/div/div[2]/div[1]/div[4]/button[1]')
        # filter_button.click()
        # driver.implicitly_wait(10)
        body_element = WebDriverWait(driver,10).until( #this code makes the program to wait for 10 seconds so that our element can be fully loaded 
        EC.presence_of_element_located((By.XPATH,'/html/body/app-root/div/main/div/app-today-price/div/div[3]/table/tbody'))
        )
        # body_element = driver.find_element(By.XPATH, '/html/body/app-root/div/main/div/app-today-price/div/div[3]/table/tbody')
        inner_html = body_element.get_attribute('innerHTML')

        driver.quit()

        
        tree = html.fromstring(inner_html)
        rows = tree.xpath('//tr')

        SN = []
        Symbol = []
        Close_Price_Rs = []
        Open_Price_Rs = []
        High_Price_Rs = []
        Low_Price_Rs = []
        Total_Traded_Quantity = []
        Total_Traded_Value = []
        Total_Trades = []
        LTP = []
        Previous_Day_Close_Price_Rs = []
        Average_Traded_Price_Rs = []
        Week_High_52_Rs = []
        Week_Low_52_Rs = []
        # Market_Capitalization_Rs_Amt_in_millions = []

        for row in rows:
            # Find all <td> tags within this row
            cells = row.xpath('.//td')
            if len(cells) == 15:  # Ensure there are exactly 15 columns, as expected
                SN.append(cells[0].text_content().strip())
                Symbol.append(cells[1].text_content().strip())
                Close_Price_Rs.append(cells[2].text_content().strip())
                Open_Price_Rs.append(cells[3].text_content().strip())
                High_Price_Rs.append(cells[4].text_content().strip())
                Low_Price_Rs.append(cells[5].text_content().strip())
                Total_Traded_Quantity.append(cells[6].text_content().strip())
                Total_Traded_Value.append(cells[7].text_content().strip())
                Total_Trades.append(cells[8].text_content().strip())
                LTP.append(cells[9].text_content().strip())
                Previous_Day_Close_Price_Rs.append(cells[10].text_content().strip())
                Average_Traded_Price_Rs.append(cells[11].text_content().strip())
                Week_High_52_Rs.append(cells[12].text_content().strip())
                Week_Low_52_Rs.append(cells[13].text_content().strip())
                # Market_Capitalization_Rs_Amt_in_millions.append(cells[14].text_content().strip())

        # Now you can create your DataFrame
        df = pd.DataFrame({
            'Sn': SN,
            'Symbol': Symbol,
            'Close_Price_Rs': Close_Price_Rs,
            'Open_Price_Rs': Open_Price_Rs,
            'High_Price_Rs': High_Price_Rs,
            'Low_Price_Rs': Low_Price_Rs,
            'Total_Traded_Quantity': Total_Traded_Quantity,
            'Total_Traded_Value': Total_Traded_Value,
            'Total_Trades': Total_Trades,
            'LTP': LTP,
            'Previous_Day_Close_Price_Rs': Previous_Day_Close_Price_Rs,
            'Average_Traded_Price_Rs': Average_Traded_Price_Rs,
            'Week_High_52_Rs': Week_High_52_Rs,
            'Week_Low_52_Rs': Week_Low_52_Rs
            # 'Market Capitalization (Rs) (Amt in millions)': Market_Capitalization_Rs_Amt_in_millions
        })
        



        columns_to_convert = [
            'Close_Price_Rs',
            'Open_Price_Rs',
            'High_Price_Rs',
            'Low_Price_Rs',
            'Total_Traded_Quantity',
            'Total_Traded_Value',
            'Total_Trades',
            'LTP',
            'Previous_Day_Close_Price_Rs',
            'Average_Traded_Price_Rs',
            'Week_High_52_Rs',
            'Week_Low_52_Rs'
            ]

        def clean_data(value):
                # Remove commas
                value = value.replace(',', '')
                # Remove text within parentheses and the parentheses themselves
                value = re.sub(r'\(.*?\)', '', value)
                # Replace hyphens with '0'
                value = value.replace('-', '0')
                return value

        for column in columns_to_convert:
                df[column] = df[column].astype(str)
                df[column] = df[column].apply(clean_data)
                df[column] = df[column].astype(float)

        return JSONResponse(content=df.to_dict(orient='records'))






                


@app.get('/stocke')#use of query parameter
def my_func(limit):
            return{'message':f'{limit} messages'}


@app.post('/stock',status_code=status.HTTP_201_CREATED) #creating a new item and inserting it into our database
def create_stock(request:schemas.ItemCreateUpdate,db:Session= Depends(get_db)):
            new_item = models.Item( 
            Sn = request.Sn, 
            Symbol = request.Symbol,
            Open_Price_Rs= request.Open_Price_Rs,  
            High_Price_Rs= request.High_Price_Rs , 
            Low_Price_Rs= request.Low_Price_Rs  ,
            Total_Traded_Quantity= request.Total_Traded_Quantity  ,
            Total_Traded_Value= request.Total_Traded_Value,
            Total_Trades= request.Total_Trades  ,
            LTP= request.LTP  ,
            Previous_Day_Close_Price_Rs= request.Previous_Day_Close_Price_Rs ,
            Average_Traded_Price_Rs= request.Average_Traded_Price_Rs  ,
            Week_High_52_Rs= request.Week_High_52_Rs  ,
            Week_Low_52_Rs= request.Week_Low_52_Rs ,
            Date= request.Date)
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            return(new_item)


        #perfroming delete peration
@app.delete('/stock/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,db:Session= Depends(get_db)):
            db.query(models.Item).filter(models.Item.id == id).delete(synchronize_session=False)
            db.commit()
            return {'message':'deletion performed!'}




