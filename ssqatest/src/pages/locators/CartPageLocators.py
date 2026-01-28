
from selenium.webdriver.common.by import By

class CartPageLocators:

    PRODUCT_NAMES_IN_CART = (By.CSS_SELECTOR, '[class*="product-name"]')
    COUPON_PANEL_BUTTON = (By.CSS_SELECTOR, '.wc-block-components-totals-coupon .wc-block-components-panel__button')
    COUPON_FIELD = (By.ID, 'wc-block-components-totals-coupon__input-0')
    APPLY_COUPON_BTN = (By.CSS_SELECTOR, '.wc-block-components-totals-coupon__button')

    CART_PAGE_MESSAGE = (By.CSS_SELECTOR, '.wc-block-components-notice-snackbar .wc-block-components-notice-banner__content')
    ERROR_BOX = (By.CSS_SELECTOR, 'div.wc-block-components-validation-error')

    PROCEED_TO_CHECKOUT_BTN = (By.CSS_SELECTOR, 'div.wp-block-woocommerce-proceed-to-checkout-block a.wc-block-components-button')