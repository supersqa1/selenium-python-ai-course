from selenium.webdriver.common.by import By


class MyAccountSignedInLocators:
    # Left sidebar navigation (WooCommerce My Account)
    LEFT_NAV_LOGOUT_BTN = (By.CSS_SELECTOR, "li.woocommerce-MyAccount-navigation-link--customer-logout")
    LEFT_NAV_LINKS = (By.CSS_SELECTOR, "nav.woocommerce-MyAccount-navigation li a")
    LEFT_NAV_ACCOUNT_DETAILS_LINK = (By.PARTIAL_LINK_TEXT, "Account details")
    LEFT_NAV_ORDERS_LINK = (By.PARTIAL_LINK_TEXT, "Orders")

    # Main content area (default tab / dashboard)
    MAIN_CONTENT = (By.CSS_SELECTOR, ".woocommerce-MyAccount-content")

    # Breadcrumb (WooCommerce or theme)
    BREADCRUMB = (By.CSS_SELECTOR, ".woocommerce-breadcrumb, nav.woocommerce-breadcrumb, .breadcrumb")

    # Account details tab form
    ACCOUNT_DETAILS_FORM = (By.CSS_SELECTOR, ".woocommerce-EditAccountForm")
    ACCOUNT_FIRST_NAME = (By.ID, "account_first_name")
    ACCOUNT_LAST_NAME = (By.ID, "account_last_name")
    ACCOUNT_DISPLAY_NAME = (By.ID, "account_display_name")
    ACCOUNT_EMAIL = (By.ID, "account_email")
    PASSWORD_CURRENT = (By.ID, "password_current")
    SAVE_CHANGES_BTN = (By.CSS_SELECTOR, "button[type='submit'][name='save_account_details']")

    # Login form (when signed out) – assert NOT visible when logged in
    LOGIN_FORM = (By.CSS_SELECTOR, "form.woocommerce-form.woocommerce-form-login")

    # Orders tab
    ORDERS_CONTENT = (By.CSS_SELECTOR, ".woocommerce-MyAccount-content")
    ORDERS_TABLE = (By.CSS_SELECTOR, "table.woocommerce-orders-table")
    ORDERS_TABLE_ROWS = (By.CSS_SELECTOR, "table.woocommerce-orders-table tbody tr")
