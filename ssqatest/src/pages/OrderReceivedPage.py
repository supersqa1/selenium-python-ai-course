
from ssqatest.src.SeleniumExtended import SeleniumExtended
from ssqatest.src.pages.locators.OrderReceivedPageLocators import OrderReceivedPageLocators

class OrderReceivedPage(OrderReceivedPageLocators):

    def __init__(self, driver):
        self.driver = driver
        self.sl = SeleniumExtended(self.driver)

    def verify_order_received_page_loaded(self):
        # Wait for URL to change to order-received page first
        import time
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        # Wait for URL to contain order-received (up to 10 seconds)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains('order-received')
            )
        except:
            # If URL doesn't change, check current URL for debugging
            current_url = self.driver.current_url
            raise Exception(f"Page did not navigate to order-received page. Current URL: {current_url}")
        
        # Small delay to ensure page is fully loaded
        time.sleep(1)
        
        # Wait for the header element to be visible, then check text
        header_element = self.sl.wait_until_element_is_visible(self.PAGE_MAIN_HEADER, timeout=10)
        header_text = header_element.text.strip()
        # Check if header contains the expected text (case-insensitive)
        assert "order received" in header_text.lower(), \
            f"Order received page header not found. Expected 'Order received' but got '{header_text}'"

    def get_order_number(self):
        return self.sl.wait_and_get_text(self.ORDER_NUMBER)