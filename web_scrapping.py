from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import ElementNotVisibleException
from datetime import datetime
from pathlib import Path
import pandas as pd
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

def f_get_data(driver: webdriver.Chrome, mck:str, url: str, lpath: str):
    if driver is None:
        return;
    
    try:
        driver.get(url);
        driver.set_window_size(1920, 1080);

        title = driver.title;
        err_page = ["404", "Not Found", "Page not found", "không tìm thấy"];
        is_err_page = any(keyword.lower() in title.lower() for keyword in err_page);

        # neu co loi xay ra ghi log file txt
        if is_err_page:
            f_write_log(path=lpath, name="error", data="Page not found");

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

def f_write_data(path: str, file: str, mck: str, data: list):
    if not os.path.exists(path):
        print("Path không tồn tại! ");
        return;

    csv_header = ["Ngày", "Giá mở cửa", "Giá cao nhất", "Giá thấp nhất", "Khối lượng", "BQ mua", "BQ Bán", "NN mua", "NN bán", "% NN sở hữu"];
    fpath = os.path.join(path, file);
    if not os.path.exists(fpath):
        with open(fpath, "w", newline="", encoding="utf-8-sig") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_header);
            writer.writeheader();
            writer.writerows(data);
    else:
        with open(fpath, "a", newline="", encoding="utf-8-sig") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_header);
            writer.writerows(data);

def f_write_log(path: str, name: str, data: str):
    if not os.path.exists(path=path):
        return;
    
    # Define file name
    fname = name + "_log_" + datetime.today().strftime("%Y%m%d") + ".txt";
    fpath = os.path.join(path, fname);

    # set time if error occur
    err_time = datetime.today().strftime("%H:%M:%S");
    data = f"[{err_time}] "  + data;

    if not os.path.exists(fpath):
        with open(fpath, "w", encoding= "utf-8") as file:
            file.write(data);
    else:
        with open(fpath, "a", encoding= "utf-8") as file:
            file.write(data);

def f_read_excel(path: str, sheet: str):
    df = pd.read_excel(path, sheet_name=sheet, header=0 );
    df.rename(columns={"STATUS" : "status", "MCK": "mck", "LINK": "url"}, inplace=True);
    dlist = df.to_dict("records");

    list = [];
    for item in dlist:
        if item.get("status") == 0:
            list.append({ "mck": item.get("mck"), "url": item.get("url")});
        else: 
            continue;

    return list;

def f_update_excel(path: str, sheet: str, mck: str):
    print(mck);
    df = pd.read_excel(path, sheet_name=sheet);
    df.loc[df["MCK"] == mck , "STATUS"] = 1;
    df.to_excel(path, index= False);

def f_check_excel(fpath: str, sheet: str):
    df = pd.read_excel(fpath, sheet_name=sheet);

    # Count so dong co trong excel
    cnt_row = df.shape[0];

    # Count so dong thoa dk
    chk_dk = df["STATUS"] == 1;
    cnt_dk = chk_dk.sum();

    if cnt_dk == cnt_row:
        df["STATUS"] = 0;

        # Save file
        df.to_excel(fpath, index=False);
    
def main():
    """
        Đang có 1 lỗi nghiêm trọng update 1 sheet file excel => có thể xóa tất cả các sheet data còn lại
        sử dụng lệnh: ctr + shift + P => Focus on Outline View
    """
    # chrome://version/
    chr_path = r"C:\Users\MY GEAR\AppData\Local\Google\Chrome\User Data";
    chr_prf = "Profile 1";

    # Write file csv
    wrt_path = r"E:\3. SCRAPPING_MCK";
    l_path = wrt_path + r'\log';

    #  Get python current path
    sfolder = Path(__file__).parent

    # Set full path name excel
    e_path = os.path.join(sfolder, "URL.xlsx");

    # Update file truoc khi chay ngay hom nay
    f_check_excel(fpath=e_path, sheet="MCK");

    link = f_read_excel(path=e_path, sheet="MCK");

    # Check not link
    if link == []:
        f_write_log(path=l_path, name="error", data="Excel no link!");
        return;

    # Create driver
    driver = f_config(path= chr_path, prf= chr_prf);

    #for item in link:
        # wrt_file = item["mck"] + ".csv";
    
        # # Get data
        # data = f_get_data( driver=driver, mck= item["mck"], url=item["url"], lpath= l_path );

        # # Write data
        # f_write_data(path=wrt_path, file=wrt_file, mck= item["mck"], data= data);

        # Update file excel
        #f_update_excel(path=e_path, sheet="MCK", mck= item["mck"]);
if __name__ == "__main__":
    main();