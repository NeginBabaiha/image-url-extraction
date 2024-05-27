import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException, NoSuchElementException
import re

def find_doi_on_page(driver):
    try:
        page_text = driver.find_element(By.TAG_NAME, "body").text
        doi_pattern = r'\b10.\d{4,9}/[-._;()/:A-Z0-9]+\b'
        doi_match = re.search(doi_pattern, page_text, re.IGNORECASE)
        if doi_match:
            return doi_match.group(0)
    except Exception as e:
        print(f"Error finding DOI: {str(e)}")
    return None

def google_image_search(query, download_path, num_images=10):
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Uncomment to run in headless mode
    driver = webdriver.Chrome(options=options)
    
    search_url = f"https://www.google.com/search?tbm=isch&q={query}"
    driver.get(search_url)
    print(f"Opened URL: {search_url}")
    
    time.sleep(2)  # Wait for the page to load

    for _ in range(20):
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
        except StaleElementReferenceException:
            print("StaleElementReferenceException encountered. Retrying...")
            continue
    
    selectors = [".rg_i.Q4LuWd", ".isv-r.PNCib.MSM1fd.BUooTd img", ".rg_i", ".H8Rx8c img"]
    thumbnails = []

    for selector in selectors:
        try:
            print(f"Trying selector '{selector}'")
            thumbnails = driver.find_elements(By.CSS_SELECTOR, selector)
            print(f"Tried selector '{selector}': found {len(thumbnails)} elements")
            if thumbnails:
                break
        except Exception as e:
            print(f"Error with selector '{selector}': {str(e)}")

    if not thumbnails:
        print("No thumbnails found with the selectors.")
        driver.quit()
        return

    dois = []
    
    for thumbnail in thumbnails[:num_images]:
        try:
            thumbnail.click()
            time.sleep(1)  # Wait for the high-resolution image to load
            
            # Search for the visit button using the provided classes
            visit_button = None
            try:
                visit_button = driver.find_element(By.CSS_SELECTOR, "a.Hnk30e.indIKd")
            except NoSuchElementException:
                print("No visit button found with the first selector. Trying alternative.")
                try:
                    visit_button = driver.find_element(By.XPATH, "//a[h1[contains(@class, 'GW0XC') and contains(@class, 'cS4Vcb-pGL6qe-fwJd0c')]]")
                except NoSuchElementException:
                    print("No visit button found with the second selector. Trying alternative.")
                    try:
                        visit_button = driver.find_element(By.XPATH, "//a[contains(@href, 'http')]")
                    except NoSuchElementException:
                        visit_button = None
            
            if visit_button:
                source_url = visit_button.get_attribute("href")
                print(f"Visiting source URL: {source_url}")
                
                driver.execute_script("window.open(arguments[0], '_blank');", source_url)
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(5)  # Wait for the source page to load
                
                doi = find_doi_on_page(driver)
                if doi:
                    dois.append(doi)
                    print(f"Found DOI: {doi}")
                
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            else:
                print("No visit button found.")
        except (StaleElementReferenceException, ElementClickInterceptedException, NoSuchElementException) as e:
            print(f"Exception encountered: {str(e)}. Retrying...")
            continue
        except Exception as e:
            print(f"Error processing thumbnail: {str(e)}")
        if len(dois) >= num_images:
            break
    
    driver.quit()
    
    if not dois:
        print("No DOIs found.")
    else:
        name_txt = input("Type name of .txt:")
        txt_str = ".txt"
        name_txt = name_txt + txt_str
        file_path = os.path.join(download_path, name_txt)
        with open(file_path, "w") as file:
            for doi in dois:
                file.write(doi + "\n")
        print(f"Saved {len(dois)} DOIs to {file_path}")


# you can querry for e.g. "covid-19 neurodegeneration"
# uncomment line  10 # options.add_argument(.... if you dont want to see google :D 
# increase  num_images=20 to download more images !!! 


if __name__ == "__main__":
    query = input("Enter the search query: ")
    download_path = "./"
    google_image_search(query, download_path, num_images=20)
