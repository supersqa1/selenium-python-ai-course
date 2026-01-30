
from selenium.webdriver.common.by import By

class CartPageLocators:

    PRODUCT_NAMES_IN_CART = (By.CSS_SELECTOR, '[class*="product-name"]')
    # One row/block per product; product name and quantity live in the same line item.
    # Demostore: classic WooCommerce cart table. If your store uses block cart, update to the
    # correct line-item selector (e.g. .wc-block-components-order-summary-item or inspect cart HTML).
    CART_LINE_ITEMS = (By.CSS_SELECTOR, 'tr.cart_item')
    COUPON_PANEL_BUTTON = (By.CSS_SELECTOR, '.wc-block-components-totals-coupon .wc-block-components-panel__button')
    COUPON_FIELD = (By.ID, 'wc-block-components-totals-coupon__input-0')
    APPLY_COUPON_BTN = (By.CSS_SELECTOR, '.wc-block-components-totals-coupon__button')

    CART_PAGE_MESSAGE = (By.CSS_SELECTOR, '.wc-block-components-notice-snackbar .wc-block-components-notice-banner__content')
    ERROR_BOX = (By.CSS_SELECTOR, 'div.wc-block-components-validation-error')

    PROCEED_TO_CHECKOUT_BTN = (By.CSS_SELECTOR, 'div.wp-block-woocommerce-proceed-to-checkout-block a.wc-block-components-button')