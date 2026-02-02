
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from ssqatest.src.SeleniumExtended import SeleniumExtended
from ssqatest.src.pages.locators.CartPageLocators import CartPageLocators
from ssqatest.src.helpers.config_helpers import get_base_url


class CartPage(CartPageLocators):

    endpoint = '/cart'

    def __init__(self, driver):
        self.driver = driver
        self.sl = SeleniumExtended(self.driver)

    def go_to_cart_page(self):
        base_url = get_base_url()
        cart_url = base_url + self.endpoint
        self.driver.get(cart_url)

    def verify_cart_page_url(self):
        self.sl.wait_until_url_contains('/cart/')

    def get_all_product_names_in_cart(self):
        product_name_elements = self.sl.wait_and_get_elements(self.PRODUCT_NAMES_IN_CART)
        product_names = []
        for elem in product_name_elements:
            # Get text from the element - this is what's actually displayed on the page
            text = elem.text.strip()
            if text:
                product_names.append(text)
        return product_names

    def get_quantity_for_product(self, product_name):
        """
        Returns the cart quantity for the given product name (exact or contains match).
        Uses CART_LINE_ITEMS: each line item contains product name and quantity in the same row/block.
        """
        try:
            items = self.sl.wait_and_get_elements(self.CART_LINE_ITEMS)
        except Exception:
            return None
        for item in items:
            try:
                name_el = item.find_element(By.CSS_SELECTOR, "[class*='product-name']")
                if product_name not in (name_el.text or "") and (name_el.text or "").strip() != product_name:
                    continue
                qty_el = item.find_element(By.CSS_SELECTOR, "input.qty")
                return qty_el.get_attribute("value")
            except NoSuchElementException:
                continue
        return None

    def has_quantity_value_2_on_page(self):
        """True if any quantity input on the cart page has value 2 (classic or block cart)."""
        try:
            # Classic cart: form.woocommerce-cart-form, tr.cart_item input.qty; block cart: various
            selectors = [
                "input.qty",
                "input[type='number'][class*='quantity']",
                "form.woocommerce-cart-form input[value='2']",
                "form.cart input[value='2']",
                ".cart_item input[value='2']",
                "[class*='cart'] input[value='2']",
            ]
            for sel in selectors:
                inputs = self.driver.find_elements(By.CSS_SELECTOR, sel)
                for el in inputs:
                    if el.is_displayed() and (el.get_attribute("value") or "").strip() == "2":
                        return True
            return False
        except Exception:
            return False

    def _expand_coupon_panel_if_collapsed(self):
        """Expand the coupon panel if it's collapsed. The coupon field is hidden inside a collapsible panel."""
        import time
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        # First, try to find the coupon field directly (panel might already be expanded)
        try:
            self.sl.wait_until_element_is_visible(self.COUPON_FIELD, timeout=2)
            return  # Field is already visible, no need to expand panel
        except:
            pass  # Field not visible, need to expand panel
        
        # Try to find and expand the panel
        try:
            # Wait for panel button to be present (may take a moment for page to load)
            panel_button = self.sl.wait_until_element_is_visible(self.COUPON_PANEL_BUTTON, timeout=10)
            aria_expanded = panel_button.get_attribute('aria-expanded')
            if aria_expanded == 'false':
                # Panel is collapsed, expand it
                # Use JavaScript click to ensure it works even if element is partially obscured
                self.driver.execute_script("arguments[0].click();", panel_button)
                # Wait for the coupon field to become visible (this confirms panel expanded)
                # Use WebDriverWait with explicit wait for visibility
                WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located(self.COUPON_FIELD)
                )
        except Exception as e:
            # If we still can't find the field after expanding, raise a clear error
            # Try one more time to find the field
            try:
                self.sl.wait_until_element_is_visible(self.COUPON_FIELD, timeout=3)
            except:
                raise TimeoutException(f"Could not find coupon field after expanding panel. Error: {str(e)}")

    def input_coupon(self, coupon_code):
        # Expand coupon panel first if it's collapsed
        self._expand_coupon_panel_if_collapsed()
        self.sl.wait_and_input_text(self.COUPON_FIELD, coupon_code)

    def click_apply_coupon(self):
        self.sl.wait_and_click(self.APPLY_COUPON_BTN)

    def apply_coupon(self, coupon_code, expect_success=True):
        self.input_coupon(coupon_code)
        self.click_apply_coupon()
        if expect_success:
            displayed_notice = self.get_displayed_message()
            # The actual message format is: "Coupon code "SSQA100" has been applied to your cart."
            # Check if the message contains the coupon code and indicates success
            assert coupon_code in displayed_notice and 'applied' in displayed_notice.lower(), \
                f"Applied coupon '{coupon_code}' but did not get successful message. " \
                f"Expected message to contain '{coupon_code}' and 'applied', but got: '{displayed_notice}'"
        # If expect_success=False, the caller will call get_displayed_error() separately

    def get_displayed_message(self):
        # Wait for message to appear (it may take a moment after applying coupon)
        element = self.sl.wait_until_element_is_visible(self.CART_PAGE_MESSAGE, timeout=10)
        return element.text

    def get_displayed_error(self):
        # Wait for error message to appear in the validation error box
        error_element = self.sl.wait_until_element_is_visible(self.ERROR_BOX, timeout=10)
        return error_element.text

    def click_on_proceed_to_checkout(self):
        self.sl.wait_and_click(self.PROCEED_TO_CHECKOUT_BTN)