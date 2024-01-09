from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 启动 Chrome 浏览器
driver = webdriver.Chrome()

# 打开目标网站
driver.get("https://www.gaokao.cn/school/search")

# 等待页面加载
wait = WebDriverWait(driver, 10)

# 点击位置
location_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "school-search_locationMenu__1mP_Z")))
location_button.click()

# 点击广东
guangdong_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '广东')]")))
guangdong_button.click()

# 点击所有城市
all_cities_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "school-search_allLocation__2AYU-")))
all_cities_button.click()

# 点击确定
confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '确定')]")))
confirm_button.click()

# 等待页面加载学校列表
school_list = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "school-search_schoolItem__3q7R2")))

# 提取学校名称
for school in school_list:
    print(school.text)

# 关闭浏览器
driver.quit()
