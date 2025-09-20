from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementNotVisibleException
from datetime import datetime
import random
import os
import csv

def f_random(fact: float):
    f_min = fact * 0;
    f_max = fact * 1;

    # Calculate float number return
    f_num = random.uniform(f_min, f_max);

    # return float number
    return f_num;

def f_config( path: str, prf: str ):  # path: duong dan thu muc profile chrome, prf: profile chrome
    if not os.path.exists(path=path):
        print("No path profile exists.");
        return;
    
    file = os.path.join(path, prf);
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
        driver.get("https://finance.vietstock.vn/HPG-ctcp-tap-doan-hoa-phat.htm");
        driver.set_window_size(1920, 1080);
    
        # Khoi ngoai ban
        table = driver.find_element(by=By.ID, value="stock-transactions");
        rows = table.find_elements(by=By.XPATH, value=".//tbody/tr");

        row = rows[0];
        # Ngày
        cell = row.find_elements( By.TAG_NAME, "td" )[0];
        date = datetime.strptime(cell.text, "%d/%m/%Y").strftime("%Y%m%d");     # Format date(DD/mm/YYYY => YYYYmmDD)

        # Gia tham chieu
        element = driver.find_element(by=By.ID, value="openprice");
        o_price = element.text.replace(",","");
    
        # Gia cao nhat
        element = driver.find_element(by=By.ID, value="highestprice");
        h_price = element.text.replace(",","");

        # Gia thap nhat
        element = driver.find_element(by=By.ID, value="lowestprice");
        l_price = element.text.replace(",","");

        # Khoi luong
        cell = row.find_elements( By.TAG_NAME, "td" )[3];    
        kl = cell.text.replace(",","");

        # Binh quan mua(BQ mua)   
        cell = row.find_elements( By.TAG_NAME, "td" )[4];
        m_bq = cell.text.replace(",","");

        # Binh quan bán(BQ bán)         
        cell = row.find_elements( By.TAG_NAME, "td" )[5];  
        b_bq = cell.text.replace(",","");

        # NN mua      
        cell = row.find_elements( By.TAG_NAME, "td" )[6];
        m_nn = cell.text.replace(",","");

        # NN bán
        cell = row.find_elements( By.TAG_NAME, "td" )[7];
        b_nn = cell.text.replace(",","");
    
        # Khoi ngoai so huu %
        element = driver.find_element(by=By.ID, value="ownedratio");
        p_nn = element.text;

        item = { 
                    "Ngày" : date, 
                    "Giá mở cửa": o_price, 
                    "Giá cao nhất": h_price, 
                    "Giá thấp nhất": l_price, 
                    "Khối lượng": kl, 
                    "BQ mua": m_bq, 
                    "BQ Bán": b_bq, 
                    "NN mua": m_nn, 
                    "NN bán": b_nn, 
                    "% NN sở hữu":p_nn 
                };

        items = list();
        items.append(item);
    
        return items;
    except ElementNotVisibleException as e:
        print("Exception element", format(e));
    finally:
        driver.quit();

def f_write_data(path: str, file: str, data: list):
    if not os.path.exists(path):
        print("Path không tồn tại! ");
        return;

    csv_header = ["Ngày", "Giá mở cửa", "Giá cao nhất", "Giá thấp nhất", "Khối lượng", "BQ mua", "BQ Bán", "NN mua", "NN bán", "% NN sở hữu"];
    fpath = os.path.join(path, file);
    if not os.path.exists(fpath):
        with open(fpath, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_header);
            writer.writeheader();
            writer.writerows(data);
    else:
        with open(fpath, 'a', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_header);
            writer.writerows(data);
    
def main():
    # chrome://version/
    chr_path = r"C:\Users\admin\AppData\Local\Google\Chrome\User Data";
    chr_prf = "Profile 2";

    wrt_path = r"D:\Github\2. Python";
    wrt_file = "HPG.csv";
    
    # Create driver
    driver = f_config(path= chr_path, prf= chr_prf);

    # Get data
    data = f_get_data( driver=driver );

    # Write data
    f_write_data(path=wrt_path, file=wrt_file, data= data);

if __name__ == "__main__":
    main();