# streamhg_worker.py
import time
import random
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_autoinstaller.install()

def run_browser_instance(thread_id, url):
    start_time = time.time()
    driver = None
    print(f"Thread-{thread_id}: Launching browser for {url}")

    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        ua = UserAgent()
        options.add_argument(f"user-agent={ua.random}")
        options.add_argument('--start-maximized')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')

        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        def random_mouse_move():
            try:
                window_width = driver.execute_script("return window.innerWidth;")
                window_height = driver.execute_script("return window.innerHeight;")
                x_offset = random.randint(-50, 50)
                y_offset = random.randint(-50, 50)
                new_x = max(10, min(500 + x_offset, window_width - 10))
                new_y = max(10, min(300 + y_offset, window_height - 10))
                action = ActionChains(driver)
                action.move_by_offset(new_x, new_y).perform()
                time.sleep(random.uniform(0.5, 1.5))
            except WebDriverException as e:
                print(f"Thread-{thread_id}: Mouse move error: {e}")

        driver.get(url)
        time.sleep(5)
        random_mouse_move()

        while time.time() - start_time < 420:  # chạy trong tối đa 7 phút
            try:
                play_button_xpath = '//div[@aria-label="Play"]'
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, play_button_xpath)))
                play_button = driver.find_element(By.XPATH, play_button_xpath)
                driver.execute_script("arguments[0].scrollIntoView(true);", play_button)
                play_button.click()

                driver.execute_script("""
                    var playButton = document.evaluate("//div[@id='vplayer']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    if (playButton) {
                        playButton.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        setTimeout(function() { playButton.click(); }, 500);
                    }
                """)

                random_mouse_move()
                time.sleep(random.randint(10, 30))

            except Exception as e:
                print(f"Thread-{thread_id}: Error during interaction: {e}")
                try:
                    driver.execute_script("""
                        var element = document.getElementById('vplayer');
                        var clickEvent = new MouseEvent('click', {
                            bubbles: true,
                            cancelable: true,
                            view: window
                        });
                        element.dispatchEvent(clickEvent);
                    """)
                except:
                    pass

        print(f"Thread-{thread_id}: Done after 7 minutes.")

    except Exception as e:
        print(f"Thread-{thread_id}: Unexpected error: {e}")

    finally:
        if driver:
            driver.quit()
            print(f"Thread-{thread_id}: Browser closed.")
