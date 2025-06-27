import time
import threading
import random
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Cài tự động đúng ChromeDriver theo phiên bản Chrome đang cài
chromedriver_autoinstaller.install()

# Danh sách liên kết
link_list = [
    "https://gradehgplus.com/nqtgnz8x2dx9",
    "https://gradehgplus.com/hfip1hmdbutz",
    "https://gradehgplus.com/gd466mm36ade",
    "https://gradehgplus.com/86pbb3fb14i2",
    "https://gradehgplus.com/j8edjxkcfz7y",
    "https://gradehgplus.com/f0bm2v25r7jl",
    "https://gradehgplus.com/gd7t22p8s8jb",
]

def run_browser(thread_id, url):
    print(f"Thread-{thread_id}: Starting browser session for {url}")
    
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

        random_mouse_move()
        driver.get(url)
        time.sleep(5)
        driver.save_screenshot(f"screenshot_thread{thread_id}_{time.time()}.png")

        random_mouse_move()

        play_button_xpath = '//div[@aria-label="Play"]'
        clicked = False

        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, play_button_xpath)))
            play_button = driver.find_element(By.XPATH, play_button_xpath)
            driver.execute_script("arguments[0].scrollIntoView(true);", play_button)
            play_button.click()
            print(f"Thread-{thread_id}: Clicked play button via element.click()")
            clicked = True
        except Exception as e:
            print(f"Thread-{thread_id}: Primary click failed: {e}")

        if not clicked:
            try:
                driver.execute_script("""
                    var playButton = document.evaluate("//div[@id='vplayer']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    if (playButton) {
                        playButton.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        setTimeout(function() { playButton.click(); }, 500);
                    }
                """)
                print(f"Thread-{thread_id}: Attempted JS click on vplayer")
                clicked = True
            except Exception as e:
                print(f"Thread-{thread_id}: JS click failed: {e}")

        if not clicked:
            try:
                driver.execute_script("""
                    var element = document.getElementById('vplayer');
                    if (element) {
                        var clickEvent = new MouseEvent('click', {
                            bubbles: true,
                            cancelable: true,
                            view: window
                        });
                        element.dispatchEvent(clickEvent);
                    }
                """)
                print(f"Thread-{thread_id}: Attempted dispatchEvent click")
                clicked = True
            except Exception as e:
                print(f"Thread-{thread_id}: dispatchEvent failed: {e}")

        if not clicked:
            try:
                element = driver.find_element(By.XPATH, play_button_xpath)
                actions = ActionChains(driver)
                actions.move_to_element_with_offset(element, 5, 5).click().perform()
                print(f"Thread-{thread_id}: ActionChains click success")
                clicked = True
            except Exception as e:
                print(f"Thread-{thread_id}: ActionChains click failed: {e}")

        random_mouse_move()
        time.sleep(30)
        driver.save_screenshot(f"screenshot_thread{thread_id}_{time.time()}.png")

    except Exception as e:
        print(f"Thread-{thread_id}: Unexpected error: {e}")
    finally:
        driver.quit()
        print(f"Thread-{thread_id}: Browser session ended.")

# 👉 HÀM PUBLIC để import từ file khác
def run_streamhg_parallel():
    selected_links = random.sample(link_list, 4)
    threads = []
    for i, link in enumerate(selected_links):
        t = threading.Thread(target=run_browser, args=(i, link))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

# Cho phép chạy trực tiếp file để test
if __name__ == "__main__":
    run_streamhg_parallel()
