from ssqatest.src.pages.locators.MyAccountSignedInLocators import MyAccountSignedInLocators
from ssqatest.src.SeleniumExtended import SeleniumExtended


class MyAccountSignedIn(MyAccountSignedInLocators):
    def __init__(self, driver):
        self.driver = driver
        self.sl = SeleniumExtended(self.driver)

    def verify_user_is_signed_in(self):
        self.sl.wait_until_element_is_visible(self.LEFT_NAV_LOGOUT_BTN)

    def is_account_area_visible(self):
        """Account area visible: main content and logout link present; login form NOT shown."""
        self.sl.wait_until_element_is_visible(self.MAIN_CONTENT)
        self.sl.wait_until_element_is_visible(self.LEFT_NAV_LOGOUT_BTN)
        return not self._is_login_form_visible()

    def _is_login_form_visible(self):
        try:
            self.sl.wait_until_element_is_visible(self.LOGIN_FORM, timeout=2)
            return True
        except Exception:
            return False

    def get_left_nav_link_texts(self):
        """Returns list of visible link texts in left nav (e.g. Dashboard, Orders, Log out)."""
        elements = self.sl.wait_and_get_elements(self.LEFT_NAV_LINKS)
        return [el.text.strip() for el in elements if el.text]

    def is_main_content_visible(self):
        self.sl.wait_until_element_is_visible(self.MAIN_CONTENT)
        return True

    def is_logout_link_visible(self):
        self.sl.wait_until_element_is_visible(self.LEFT_NAV_LOGOUT_BTN)
        return True

    def get_breadcrumb_text(self):
        """Returns full breadcrumb text (e.g. Home > My account)."""
        element = self.sl.wait_until_element_is_visible(self.BREADCRUMB)
        return element.text.strip()

    def click_account_details_link(self):
        self.sl.wait_and_click(self.LEFT_NAV_ACCOUNT_DETAILS_LINK)

    def click_orders_link(self):
        self.sl.wait_and_click(self.LEFT_NAV_ORDERS_LINK)

    def get_orders_content_text(self):
        """Returns visible text in the main content area (after clicking Orders)."""
        el = self.sl.wait_until_element_is_visible(self.ORDERS_CONTENT)
        return el.text.strip()

    def is_orders_table_visible(self):
        """True if the orders table is present (user has orders)."""
        try:
            self.sl.wait_until_element_is_visible(self.ORDERS_TABLE, timeout=5)
            return True
        except Exception:
            return False

    def get_orders_table_row_count(self):
        """Number of order rows in the table (0 if no table or empty)."""
        try:
            rows = self.sl.wait_and_get_elements(self.ORDERS_TABLE_ROWS, timeout=5)
            return len(rows)
        except Exception:
            return 0

    def is_account_details_form_visible(self):
        """Account details tab: form with First name, Last name, Display name, Email; Save button."""
        self.sl.wait_until_element_is_visible(self.ACCOUNT_DETAILS_FORM)
        self.sl.wait_until_element_is_visible(self.ACCOUNT_FIRST_NAME)
        self.sl.wait_until_element_is_visible(self.ACCOUNT_LAST_NAME)
        self.sl.wait_until_element_is_visible(self.ACCOUNT_EMAIL)
        self.sl.wait_until_element_is_visible(self.SAVE_CHANGES_BTN)
        return True
