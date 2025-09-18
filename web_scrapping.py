from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
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

    option = uc.ChromeOptions();
    option.add_argument(f"--user-data-dir={path}");
    option.add_argument(f"--profile-directory={prf}");

    driver = uc.Chrome( version_main= 127, options=option);
    try:
        print("Đang khởi động Chrome với profile thật...");
        # Truy cập một trang đòi hỏi đăng nhập, ví dụ như Gmail hoặc Google Drive
        # Bạn sẽ thấy mình đã được đăng nhập sẵn!
        driver.get("https://tuoitre.vn");
        
        print("Truy cập thành công! Trình duyệt đang được điều khiển tự động.");
        time.sleep(5) # Giữ trình duyệt mở để bạn kiểm tra
    finally:
        driver.quit()

def f_get_data():
    print("Get data!");

def main():
    path = 'C:\\Users\\admin\\AppData\\Local\\Google\\Chrome\\User Data'
    prf = 'Profile 1'

    f_config(path= path, prf= prf)

    # f_get_data()

if __name__ == "__main__":
    main()
