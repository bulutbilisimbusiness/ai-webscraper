import os
from selenium import webdriver
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def scrape_website(website):
    # Get SBR_WEBDRIVER from environment variable
    sbr_webdriver = os.getenv("SBR_WEBDRIVER")
    
    # Use local Chrome if Bright Data is not available or not working
    if not sbr_webdriver or "USE_LOCAL_CHROME" in os.environ:
        return scrape_website_local(website)
    
    # Bright Data usage
    try:
        sbr_connection = ChromiumRemoteConnection(sbr_webdriver, 'goog', 'chrome')
        with Remote(sbr_connection, options=ChromeOptions()) as driver:
            driver.get(website)
            solve_res=driver.execute('executeCdpCommand',{
                'cmd': 'Captcha.waitForSolve',
                'params': {'detectTimeout': 10000}
            })
            html = driver.page_source
            return html
    except Exception as e:
        # Fall back to local Chrome if Bright Data fails
        return scrape_website_local(website)

def scrape_website_local(website):
    """Scraping with local Chrome driver"""
    try:
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Create Chrome driver service
        try:
            # Try to use existing chromedriver.exe
            service = Service("./chromedriver.exe")
            driver = webdriver.Chrome(service=service, options=options)
        except:
            try:
                # Try to use chromedriver from system PATH
                driver = webdriver.Chrome(options=options)
            except Exception as driver_error:
                                 return f"Chrome driver error: {str(driver_error)}. Please install Chrome and chromedriver."
         
         driver.get(website)
         
         # Wait for page to load
         driver.implicitly_wait(3)
         
         html = driver.page_source
         driver.quit()
         
         if len(html) < 100:
             return f"Warning: Page content seems too short ({len(html)} chars). Check if page loaded correctly."
        return html
        
    except Exception as e:
        return f"Scraping error: {str(e)}"

def extract_body_content(html_content):
    if html_content.startswith("Error") or html_content.startswith("Warning"):
        return html_content
        
    soup= BeautifulSoup(html_content, 'html.parser')
    body_content = soup.body
    if body_content:
        return str(body_content)
    return "No body content found"
   
def clean_body_content(body_content):
    if body_content.startswith("Error") or body_content.startswith("Warning") or body_content == "No body content found":
        return body_content
        
    soup = BeautifulSoup(body_content, 'html.parser')
    for script_or_style in soup(['script', 'style']):
        script_or_style.extract()  # Remove script and style elements
    cleaned_content= soup.get_text(separator="\n")   
    cleaned_content= "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)
    ]
    
  