from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

# Set up headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0")

# Launch browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

data = []

try:
    url = "https://bccci-bd.org/member-of-bccci/"
    driver.get(url)

    # Wait until the members section is loaded
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'member25'))
    )

    # Get HTML content
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    members = soup.find_all('div', class_='member25')

    for member in members:
        try:
            name = member.find('h2', class_='member-name').get_text(strip=True)
        except:
            name = "N/A"

        try:
            membership_no = member.find('p', class_='member-no').get_text(strip=True)
        except:
            membership_no = "N/A"

        details = member.find_all('p')
        details_text = [p.get_text(separator=' ', strip=True) for p in details
                        if 'member-no' not in p.get('class', []) and not p.find('a')]
        details_text = ' '.join(details_text).strip()

        email_tag = member.find('a', href=lambda x: x and x.startswith('mailto:'))
        email = email_tag['href'].replace('mailto:', '').strip() if email_tag else 'No email provided'

        data.append({
            "Company Name": name,
            "Membership No": membership_no,
            "Details": details_text,
            "Email": email
        })

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()

# Save to Excel
df = pd.DataFrame(data)
df.to_excel("BCCCI_Members.xlsx", index=False)
print("Data saved to BCCCI_Members.xlsx")
