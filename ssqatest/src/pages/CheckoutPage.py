
from ssqatest.src.SeleniumExtended import SeleniumExtended
from ssqatest.src.pages.locators.CheckoutPageLocators import CheckoutPageLocators
from ssqatest.src.helpers.generic_helpers import generate_random_email_and_password
from ssqatest.src.helpers.config_helpers import get_base_url

class CheckoutPage(CheckoutPageLocators):

    endpoint = '/checkout'

    def __init__(self, driver):
        self.driver = driver
        self.sl = SeleniumExtended(self.driver)

    def go_to_checkout_page(self):
        base_url = get_base_url()
        checkout_url = base_url + self.endpoint
        self.driver.get(checkout_url)

    def _field_exists(self, locator, timeout=2):
        """Check if a field exists on the page."""
        try:
            self.sl.wait_until_element_is_visible(locator, timeout=timeout)
            return True
        except:
            return False

    def input_billing_first_name(self, first_name=None):
        first_name = first_name if first_name else 'AutomationFname'
        if self._field_exists(self.BILLING_FIRST_NAME_FIELD):
            self.sl.wait_and_input_text(self.BILLING_FIRST_NAME_FIELD, first_name)

    def input_billing_last_name(self, last_name=None):
        last_name = last_name if last_name else 'AutomationLname'
        if self._field_exists(self.BILLING_LAST_NAME_FIELD):
            self.sl.wait_and_input_text(self.BILLING_LAST_NAME_FIELD, last_name)

    def input_billing_street_address_1(self, address1=None):
        address1 = address1 if address1 else "123 Main st."
        if self._field_exists(self.BILLING_ADDRESS_1_FIELD):
            self.sl.wait_and_input_text(self.BILLING_ADDRESS_1_FIELD, address1)

    def input_billing_city(self, city=None):
        city = 'San Francisco' if not city else city
        if self._field_exists(self.BILLING_CITY_FIELD):
            self.sl.wait_and_input_text(self.BILLING_CITY_FIELD, city)

    def input_billing_zip(self, zip_code=None):
        zip_code = '94016' if not zip_code else str(zip_code)
        if self._field_exists(self.BILLING_ZIP_FIELD):
            self.sl.wait_and_input_text(self.BILLING_ZIP_FIELD, zip_code)

    def input_billing_phone_number(self, phone=None):
        phone = '4151111111' if not phone else phone
        if self._field_exists(self.BILLING_PHONE_FIELD):
            self.sl.wait_and_input_text(self.BILLING_PHONE_FIELD, phone)

    def input_billing_email(self, email=None):
        if not email:
            rand_email = generate_random_email_and_password()
            email = rand_email['email']
        if self._field_exists(self.BILLING_EMAIL_FIELD):
            self.sl.wait_and_input_text(self.BILLING_EMAIL_FIELD, email)

    def select_billing_country(self, country="United States (US)"):
        if self._field_exists(self.BILLING_COUNTRY_DROPDOWN):
            self.sl.wait_and_select_dropdown(self.BILLING_COUNTRY_DROPDOWN, to_select=country, select_by="visible_text")
            # Wait a moment for state dropdown to populate after country selection
            import time
            time.sleep(0.5)

    def select_billing_state(self, state='California'):
        if self._field_exists(self.BILLING_STATE_DROPDOWN):
            self.sl.wait_and_select_dropdown(self.BILLING_STATE_DROPDOWN, to_select=state, select_by="visible_text")

    def fill_in_billing_info(self, f_name=None, l_name=None, street1=None, city=None, zip_code=None, phone=None, email=None, state=None, country=None):
        # Fill in billing fields only if they exist on the page
        # This handles cases where products are digital/virtual and don't require all fields
        # Order matters: email first, then country (which populates state dropdown), then rest
        self.input_billing_email(email=email)
        country = country if country else "United States (US)"
        self.select_billing_country(country=country)
        self.input_billing_first_name(first_name=f_name)
        self.input_billing_last_name(last_name=l_name)
        self.input_billing_street_address_1(address1=street1)
        self.input_billing_city(city=city)
        self.input_billing_zip(zip_code=zip_code)
        self.input_billing_phone_number(phone=phone)
        state = state if state else 'California'
        self.select_billing_state(state=state)

    def click_place_order(self):
        """
        Click the place order button with retry logic.
        TODO: There appears to be a bug where clicking the button sometimes doesn't trigger navigation.
        If the order received page doesn't appear within 5 seconds and the button is still visible,
        we retry clicking it once more.
        """
        import time
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        # Click the button
        self.sl.wait_and_click(self.PLACE_ORDER_BTN)
        
        # Wait up to 5 seconds for navigation to order received page
        try:
            WebDriverWait(self.driver, 5).until(
                EC.url_contains('order-received')
            )
            # Navigation successful, return
            return
        except:
            # Navigation didn't happen, check if button is still visible
            try:
                # Check if button is still present and visible
                button = self.driver.find_element(*self.PLACE_ORDER_BTN)
                if button.is_displayed():
                    # Button still visible, click again (retry)
                    self.sl.wait_and_click(self.PLACE_ORDER_BTN)
            except:
                # Button not found or not visible, assume navigation happened
                pass