from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementNotVisibleException
import time
import random
import os

def f_random(fact: float):
    f_min = fact * 0
    f_max = fact * 1

    # Calculate float number return
    f_num = random.uniform(f_min, f_max)

    # return float number
    return f_num


def f_config( path: str, prf: str ):  # path: duong dan thu muc profile chrome, prf: profile chrome
    if not os.path.exists(path=path):
        print("No path profile exists.");
        return;
    
    file = "\\".join([path, prf]);
    if not os.path.isdir(s=file):
        print("No path profile exists.");
        return;

    # Config option
    options = webdriver.ChromeOptions();
    options.add_argument("--headless=new");

    # Initial driver
    try:
        driver = webdriver.Chrome(options=options);
    except WebDriverException as e:
        print("Initial WebDriver error!");
        return;

    # Return driver
    return driver;

def f_get_data(driver: webdriver.Chrome):
    if driver is None:
        return;
    
    try:
        #driver.get("https://cafef.vn/du-lieu/hose/hpg-cong-ty-co-phan-tap-doan-hoa-phat.chn");
        driver.get("https://finance.vietstock.vn/HPG-ctcp-tap-doan-hoa-phat.htm");
        driver.set_window_size(1920, 1080);
        title = driver.title;
        print(title);
        
        # Gia tham chieu
        element = driver.find_element(by=By.ID, value="openprice");
        print("Gia tham chieu: ",element.text);
    
        # Gia cao nhat
        element = driver.find_element(by=By.ID, value="highestprice");
        print("Gia cao nhat: ", element.text);
    
        # Gia thap nhat
        element = driver.find_element(by=By.ID, value="lowestprice");
        print("Gia thap nhat: ", element.text);

        # khoi ngoai
        # Khoi ngoai mua
        element = driver.find_element(by=By.ID, value="foreignBuy");
        print("Khoi ngoai mua: ", element.text);
    
        # Khoi ngoai ban
        element = driver.find_element(by=By.ID, value="foregin__sellvol");
        print("Khoi ngoai ban: ", element.text);
    
        # Khoi ngoai so huu %
        element = driver.find_element(by=By.ID, value="ownedratio");
        print("% khoi ngoai so huu: ", element.text);
    except ElementNotVisibleException as e:
        print("Exception element", format(e));
    finally:
        driver.quit();

def main():
    # chrome://version/
    path = 'C:\\Users\\admin\\AppData\\Local\\Google\\Chrome\\User Data';
    prf = 'Profile 2';
    
    # Create driver
    driver = f_config(path= path, prf= prf);

    # Get data
    f_get_data( driver );

if __name__ == "__main__":
    main()
