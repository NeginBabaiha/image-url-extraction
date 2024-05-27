

link_urls_thumb  = False
high_res_urls = False
search_for_doi = False

if link_urls_thumb:

    import os
    import time
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import StaleElementReferenceException

    def google_image_search(query, download_path, num_images=100):
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
        
        # Using the specific selector for images found in the developer console
        selector = ".H8Rx8c img"
        images = driver.find_elements(By.CSS_SELECTOR, selector)
        print(f"Tried selector '{selector}': found {len(images)} elements")
        
        if not images:
            print("No thumbnails found with the selector.")
            driver.quit()
            return

        image_urls = []
        
        for img in images[:num_images]:
            try:
                src = img.get_attribute("src")
                if src and "http" in src:
                    image_urls.append(src)
                    #print(f"Found image URL: {src}")   # uncomment this to see URLs .. 
                    if len(image_urls) >= num_images:
                        break
            except Exception as e:
                print(f"Error getting image URL: {str(e)}")
        
        driver.quit()
        
        # Save URLs to a text file
        if not image_urls:
            print("No image URLs found.")
        else:
            name_txt = input("Type name of .txt:")
            txt_str = ".txt"
            name_txt = name_txt +txt_str
            print("here", name_txt)
            file_path = os.path.join(download_path, name_txt)
            with open(file_path, "w") as file:
                for url in image_urls:
                    file.write(url + "\n")
            print(f"Saved {len(image_urls)} image URLs to {file_path}")

    if __name__ == "__main__":
        query = input("Enter the search query: ")
        download_path = "./"
        # You can change the number of images to download by modifying the num_images parameter
        google_image_search(query, download_path, num_images=100)


if high_res_urls:
    import os
    import time
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException

    def google_image_search(query, download_path, num_images=100):
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')  # Uncomment to run in headless mode
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
        
        # Using the specific selector for images found in the developer console
        selector = ".H8Rx8c img"
        thumbnails = driver.find_elements(By.CSS_SELECTOR, selector)
        print(f"Tried selector '{selector}': found {len(thumbnails)} elements")
        
        if not thumbnails:
            print("No thumbnails found with the selector.")
            driver.quit()
            return

        image_urls = []
        
        for thumbnail in thumbnails[:num_images]:
            try:
                thumbnail.click()
                time.sleep(1)  # Wait for the high-resolution image to load
                # Manually found selectors for high-resolution images
                possible_selectors = [
                    "img.n3VNCb",
                    "img.irc_mi",
                    "img.TSKP0c",  # Adding the new potential selector
                    "img[jsname='HiaYvf']",  # Additional selector
                    "img[jsname='dTDiAc']",  # Additional selector
                    "img[jsname='Q4LuWd']"   # Additional selector
                ]
                actual_images = []
                for possible_selector in possible_selectors:
                    actual_images = driver.find_elements(By.CSS_SELECTOR, possible_selector)
                    print(f"Found {len(actual_images)} high-resolution images using '{possible_selector}' selector")
                    if actual_images:
                        break
                
                if not actual_images:
                    print("No high-resolution images found for clicked thumbnail.")
                
                for actual_image in actual_images:
                    src = actual_image.get_attribute("src")
                    if not src or "http" not in src:
                        src = actual_image.get_attribute("data-src")
                    if src and "http" in src:
                        image_urls.append(src)
                        print(f"Found high-resolution image URL: {src}")
                        if len(image_urls) >= num_images:
                            break
            except (StaleElementReferenceException, ElementClickInterceptedException) as e:
                print(f"Exception encountered: {str(e)}. Retrying...")
                continue
            except Exception as e:
                print(f"Error clicking image: {str(e)}")
            if len(image_urls) >= num_images:
                break
        
        driver.quit()
        
        # Save URLs to a text file
        if not image_urls:
            print("No image URLs found.")
        else:
            name_txt = input("Type name of .txt:")
            txt_str = ".txt"
            name_txt = name_txt + txt_str
            file_path = os.path.join(download_path, name_txt)
            with open(file_path, "w") as file:
                for url in image_urls:
                    file.write(url + "\n")
            print(f"Saved {len(image_urls)} high-resolution image URLs to {file_path}")

    if __name__ == "__main__":
        query = input("Enter the search query: ")
        download_path = "./"
        # You can change the number of images to download by modifying the num_images parameter
        google_image_search(query, download_path, num_images=100)

if search_for_doi: 

    import os
    import time
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
    import re

    def find_doi_on_page(driver):
        try:
            # Extract all text from the page
            page_text = driver.find_element(By.TAG_NAME, "body").text
            print(f"Page text length: {len(page_text)}")  # Debugging line
            # Regular expression to find DOI
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
        
        # Using the specific selector for images found in the developer console
        selector = ".H8Rx8c img"
        thumbnails = driver.find_elements(By.CSS_SELECTOR, selector)
        print(f"Tried selector '{selector}': found {len(thumbnails)} elements")
        
        if not thumbnails:
            print("No thumbnails found with the selector.")
            driver.quit()
            return

        dois = []
        
        for thumbnail in thumbnails[:num_images]:
            try:
                thumbnail.click()
                time.sleep(1)  # Wait for the high-resolution image to load
                # Click on the visit button to go to the source page
                visit_button = driver.find_element(By.CSS_SELECTOR, "a.VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb")
                source_url = visit_button.get_attribute("href")
                print(f"Visiting source URL: {source_url}")  # Debugging line
                driver.execute_script("window.open(arguments[0], '_blank');", source_url)
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(5)  # Wait for the source page to load
                
                doi = find_doi_on_page(driver)
                if doi:
                    dois.append(doi)
                    print(f"Found DOI: {doi}")
                
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            except (StaleElementReferenceException, ElementClickInterceptedException) as e:
                print(f"Exception encountered: {str(e)}. Retrying...")
                continue
            except Exception as e:
                print(f"Error processing thumbnail: {str(e)}")
            if len(dois) >= num_images:
                break
        
        driver.quit()
        
        # Save DOIs to a text file
        if not dois:
            print("No DOIs found.")
        else:
            file_path = os.path.join(download_path, "dois.txt")
            with open(file_path, "w") as file:
                for doi in dois:
                    file.write(doi + "\n")
            print(f"Saved {len(dois)} DOIs to {file_path}")

    if __name__ == "__main__":
        query = input("Enter the search query: ")
        download_path = "./"
        # You can change the number of images to process by modifying the num_images parameter
        google_image_search(query, download_path, num_images=10)
