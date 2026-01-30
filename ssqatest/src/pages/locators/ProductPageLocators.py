
from selenium.webdriver.common.by import By

class ProductPageLocators:

    PRODUCT_TITLE = (By.CSS_SELECTOR, 'div.entry-summary h1.product_title.entry-title')
    PRODUCT_IMAGE_MAIN = (By.CSS_SELECTOR, 'div.woocommerce-product-gallery__image img')
    PRODUCT_ALTERNATE_IMAGES = (By.CSS_SELECTOR, 'div.woocommerce-product-gallery.images ol.flex-control-thumbs li img')
    PRODUCT_TYPE_TEXT = (By.CSS_SELECTOR, 'div.entry-summary div.woocommerce-product-details__short-description')
    PRODUCT_PRICE = (By.CSS_SELECTOR, 'div.entry-summary p.price')
    # Works for both simple (single_add_to_cart_button) and variable (add_to_cart_button) product pages
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, 'form.cart button[type="submit"]')
    VIEW_CART_BTN_IN_SUCCESS_MESSAGE = (By.CSS_SELECTOR, 'div.woocommerce-message[role="alert"] a.button.wc-forward')
    # Works for both simple (form.cart) and variable (div.add-to-cart) product pages
    PRODUCT_PAGE_QUANTITY_FIELD = (By.CSS_SELECTOR, 'form.cart div.quantity input.input-text.qty')
    PRODUCT_PAGE_SKU_AND_LABEL = (By.CSS_SELECTOR, 'div.product_meta span.sku_wrapper')
    PRODUCT_PAGE_CATEGORY_AND_LABEL = (By.CSS_SELECTOR, 'div.product_meta span.posted_in')
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, 'div#tab-description p')
    PRODUCT_DESCRIPTION_HEADER = (By.CSS_SELECTOR, 'div#tab-description h2')
    RELATED_PRODUCTS_SECTION_HEADER = (By.CSS_SELECTOR, 'section.related.products > h2')
    RELATED_PRODUCTS_LIST = (By.CSS_SELECTOR, 'section.related.products ul li.type-product')
    LEFT_NAV_TABS = (By.CSS_SELECTOR, 'div.woocommerce-tabs ul.tabs.wc-tabs li')
    ADDITIONAL_INFO_TAB_LINK = (By.CSS_SELECTOR, 'div.woocommerce-tabs ul.tabs li a[href="#tab-additional_information"]')
    ADDITIONAL_INFO_CONTENT = (By.CSS_SELECTOR, 'div#tab-additional_information')
    # Reviews tab (WooCommerce / WordPress comment form)
    REVIEWS_TAB_LINK = (By.CSS_SELECTOR, 'div.woocommerce-tabs ul.tabs li a[href="#tab-reviews"]')
    REVIEWS_TAB_CONTENT = (By.CSS_SELECTOR, 'div#tab-reviews')
    REVIEWS_EMPTY_MESSAGE = (By.CSS_SELECTOR, 'div#tab-reviews .woocommerce-noreviews, div#tab-reviews p')
    REVIEWS_FORM = (By.CSS_SELECTOR, 'div#tab-reviews form#commentform')
    REVIEWS_RATING_SELECT = (By.CSS_SELECTOR, 'div#tab-reviews p.stars select#rating, div#tab-reviews select#rating')
    REVIEWS_COMMENT_TEXTAREA = (By.CSS_SELECTOR, 'div#tab-reviews textarea#comment')
    REVIEWS_AUTHOR_INPUT = (By.CSS_SELECTOR, 'div#tab-reviews input#author')
    REVIEWS_EMAIL_INPUT = (By.CSS_SELECTOR, 'div#tab-reviews input#email')
    REVIEWS_SUBMIT_BUTTON = (By.CSS_SELECTOR, 'div#tab-reviews input#submit')
    REVIEWS_SAVE_DETAILS_CHECKBOX = (By.CSS_SELECTOR, 'div#tab-reviews input#comment_form_cookies_consent, div#tab-reviews .comment-form-cookies-consent input')
    REVIEWS_LIST = (By.CSS_SELECTOR, 'div#tab-reviews ol.commentlist li.comment')
    REVIEWS_FORM_ERROR = (By.CSS_SELECTOR, 'div#tab-reviews .woocommerce-error, div#tab-reviews .comment-form .error, div#tab-reviews #commentform .error, div#tab-reviews .comment-notes')
    # Breadcrumb: WooCommerce uses nav.woocommerce-breadcrumb
    BREADCRUMB = (By.CSS_SELECTOR, 'nav.woocommerce-breadcrumb')
    # Sale badge (WooCommerce .onsale); main product only – filter out section.related in code
    SALE_BADGE = (By.CSS_SELECTOR, 'span.onsale')
    VARIABLE_PRODUCT_COLOR_ATTRIBUTE_LABEL = (By.CSS_SELECTOR, 'table.variations tr th.label label[for="pa_color"]')
    VARIABLE_PRODUCT_LOGO_ATTRIBUTE_LABEL = (By.CSS_SELECTOR, 'table.variations tr th.label label[for="logo"], table.variations tr th.label label[for="attribute_logo"]')
    VARIABLE_PRODUCT_COLOR_ATTRIBUTE_DROPDOWN = (By.CSS_SELECTOR, 'table.variations tr select[name="attribute_pa_color"]')
    VARIABLE_PRODUCT_COLOR_ATTRIBUTE_OPTIONS = (By.CSS_SELECTOR, 'table.variations tr select[name="attribute_pa_color"] option')
    VARIABLE_PRODUCT_LOGO_ATTRIBUTE_OPTIONS = (By.CSS_SELECTOR, 'table.variations tr select[name="attribute_logo"] option')
    VARIABLE_PRODUCT_LOGO_ATTRIBUTE_DROPDOWN = (By.CSS_SELECTOR, 'table.variations tr select#logo')

    RESET_VARIATIONS_BTN = (By.CSS_SELECTOR, 'table.variations a.reset_variations')

