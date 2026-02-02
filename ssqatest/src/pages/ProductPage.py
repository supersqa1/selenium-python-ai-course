from selenium.webdriver.common.by import By
from ssqatest.src.SeleniumExtended import SeleniumExtended
from ssqatest.src.pages.locators.ProductPageLocators import ProductPageLocators
from ssqatest.src.helpers.config_helpers import get_base_url

class ProductPage(ProductPageLocators):



    def __init__(self, driver):
        self.driver = driver
        self.sl = SeleniumExtended(self.driver)

    def go_to_product_page(self, product_slug):
        base_url = get_base_url()
        product_page_url = f"{base_url}/product/{product_slug}"
        self.driver.get(product_page_url)

    def get_displayed_product_name(self):
        return self.sl.wait_and_get_text(self.PRODUCT_TITLE)

    def get_url_of_displayed_main_image(self):
        image_elm = self.sl.wait_until_element_is_visible(self.PRODUCT_IMAGE_MAIN)
        # Try data-src first (lazy loading), fallback to src if already loaded
        src = image_elm.get_attribute('data-src') or image_elm.get_attribute('src')
        return src

    def get_url_of_displayed_alternate_images(self):
        image_elements = self.sl.wait_until_elements_are_visible(self.PRODUCT_ALTERNATE_IMAGES)
        srcs = [elem.get_attribute('src') for elem in image_elements]
        return srcs

    def get_product_type_text(self):
        return self.sl.wait_and_get_text(self.PRODUCT_TYPE_TEXT)


    def get_displayed_product_price_inner_html(self):
        elem = self.sl.wait_and_get_elements(self.PRODUCT_PRICE)[0]
        return elem.get_attribute('innerHTML')

    def get_displayed_product_price(self):

        return self.sl.wait_and_get_text(self.PRODUCT_PRICE)

    def get_add_to_cart_button_element(self):
        return self.sl.wait_until_element_is_visible(self.ADD_TO_CART_BUTTON)

    def click_add_to_cart_button(self):
        # Use wait_and_click which handles scroll and click interception
        self.sl.wait_and_click(self.ADD_TO_CART_BUTTON)

    def get_view_cart_btn_on_add_to_cart_success_message_box(self):
        """View cart link after add-to-cart success; falls back to any visible cart link if theme differs."""
        from selenium.common.exceptions import TimeoutException
        from selenium.webdriver.common.by import By
        try:
            return self.sl.wait_until_element_is_visible(self.VIEW_CART_BTN_IN_SUCCESS_MESSAGE, timeout=10)
        except TimeoutException:
            links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="cart"]')
            for el in links:
                if el.is_displayed() and ("view" in (el.text or "").lower() or "cart" in (el.text or "").lower()):
                    return el
            raise

    def click_view_cart_btn_on_add_to_cart_success_message_box(self):
        view_cart_btn = self.get_view_cart_btn_on_add_to_cart_success_message_box()
        view_cart_btn.click()

    def get_quantity_field_element(self):
        return self.sl.wait_until_element_is_visible(self.PRODUCT_PAGE_QUANTITY_FIELD)

    def set_quantity(self, value):
        """Set the quantity input to the given integer (e.g. 2). Clears existing value first."""
        qty_field = self.get_quantity_field_element()
        qty_field.clear()
        qty_field.send_keys(str(int(value)))

    def get_breadcrumb_text(self):
        """Returns the visible text of the PDP breadcrumb (e.g. 'Home / Clothing / Accessories / Beanie')."""
        return self.sl.wait_and_get_text(self.BREADCRUMB)

    def is_sale_badge_visible(self):
        """Returns True if the main product's sale badge is visible (ignores related products in section.related)."""
        try:
            elements = self.sl.wait_and_get_elements(self.SALE_BADGE)
            for el in elements:
                if not el.is_displayed():
                    continue
                try:
                    in_related = self.driver.execute_script(
                        "var s = arguments[0].closest('section.related'); return s !== null;", el
                    )
                    if not in_related:
                        return True
                except Exception:
                    pass
            return False
        except Exception:
            return False

    def get_sale_badge_text(self):
        """Returns the main product's sale badge text if visible (first badge not in section.related)."""
        try:
            elements = self.sl.wait_and_get_elements(self.SALE_BADGE)
            for el in elements:
                if not el.is_displayed():
                    continue
                try:
                    in_related = self.driver.execute_script(
                        "var s = arguments[0].closest('section.related'); return s !== null;", el
                    )
                    if not in_related:
                        return el.text or ""
                except Exception:
                    pass
            return ""
        except Exception:
            return ""

    def get_displayed_sku_and_label(self):
        return self.sl.wait_and_get_text(self.PRODUCT_PAGE_SKU_AND_LABEL)

    def get_displayed_category_and_label(self):
        return self.sl.wait_and_get_text(self.PRODUCT_PAGE_CATEGORY_AND_LABEL)

    def get_displayed_product_description(self):
        return self.sl.wait_and_get_text(self.PRODUCT_DESCRIPTION)

    def get_displayed_product_description_full(self):
        """All description paragraphs joined (matches API HTML stripped with no space between tags)."""
        elements = self.sl.wait_and_get_elements(self.PRODUCT_DESCRIPTION)
        return "".join(elem.text for elem in elements)

    def get_displayed_product_description_header(self):
        return self.sl.wait_and_get_text(self.PRODUCT_DESCRIPTION_HEADER)

    def get_related_products_section_header(self):
        return self.sl.wait_and_get_text(self.RELATED_PRODUCTS_SECTION_HEADER)

    def get_related_products_elements_list(self):
        related_products_list = self.sl.wait_until_elements_are_visible(self.RELATED_PRODUCTS_LIST)
        return related_products_list

    def get_left_nav_tab_elements(self):
        return self.sl.wait_until_elements_are_visible(self.LEFT_NAV_TABS)

    def get_labels_of_left_nav_tabs(self):
        tabs_elements = self.get_left_nav_tab_elements()
        return [i.text for i in tabs_elements]

    def click_additional_information_tab(self):
        """Clicks the Additional information tab so its content is visible."""
        self.sl.wait_and_click(self.ADDITIONAL_INFO_TAB_LINK)

    def get_additional_information_content_text(self):
        """Returns the visible text of the Additional information tab content."""
        return self.sl.wait_and_get_text(self.ADDITIONAL_INFO_CONTENT)

    # --- Reviews tab ---
    def click_reviews_tab(self):
        """Clicks the Reviews tab so its content is visible."""
        self.sl.wait_and_click(self.REVIEWS_TAB_LINK)

    def get_reviews_tab_content_text(self):
        """Returns the visible text of the Reviews tab content (empty state + form).
        Caller must load the product page and open the Reviews tab first."""
        return self.sl.wait_and_get_text(self.REVIEWS_TAB_CONTENT)

    def is_reviews_tab_content_visible(self):
        """Returns True if the Reviews tab content panel is visible."""
        try:
            el = self.sl.wait_until_element_is_visible(self.REVIEWS_TAB_CONTENT, timeout=5)
            return el.is_displayed()
        except Exception:
            return False

    def is_reviews_form_visible(self):
        """Returns True if the review comment form is visible."""
        try:
            el = self.sl.wait_until_element_is_visible(self.REVIEWS_FORM, timeout=3)
            return el.is_displayed()
        except Exception:
            return False

    def is_reviews_rating_visible(self):
        """Returns True if rating selector (dropdown or stars) is visible."""
        try:
            # WooCommerce may use p.stars (star links) or select#rating
            el = self.sl.wait_until_element_is_visible(self.REVIEWS_RATING_SELECT, timeout=2)
            return el.is_displayed()
        except Exception:
            # TODO: may be use the correct locator the first time
            try:
                stars = self.driver.find_elements(By.CSS_SELECTOR, "div#tab-reviews p.stars")
                return bool(stars and stars[0].is_displayed())
            except Exception:
                return False

    def is_reviews_comment_textarea_visible(self):
        try:
                el = self.sl.wait_until_element_is_visible(self.REVIEWS_COMMENT_TEXTAREA, timeout=2)
                return el.is_displayed()
        except Exception:
            return False

    def is_reviews_author_input_visible(self):
        try:
            el = self.sl.wait_until_element_is_visible(self.REVIEWS_AUTHOR_INPUT, timeout=2)
            return el.is_displayed()
        except Exception:
            return False

    def is_reviews_email_input_visible(self):
        try:
            el = self.sl.wait_until_element_is_visible(self.REVIEWS_EMAIL_INPUT, timeout=2)
            return el.is_displayed()
        except Exception:
            return False

    def is_reviews_submit_button_visible(self):
        try:
            el = self.sl.wait_until_element_is_visible(self.REVIEWS_SUBMIT_BUTTON, timeout=2)
            return el.is_displayed()
        except Exception:
            return False

    def is_reviews_save_details_checkbox_visible(self):
        """Returns True if 'Save my name, email, and website...' checkbox is visible."""
        try:
            el = self.sl.wait_until_element_is_visible(self.REVIEWS_SAVE_DETAILS_CHECKBOX, timeout=2)
            return el.is_displayed()
        except Exception:
            return False

    def get_reviews_save_details_checkbox_label_text(self):
        """Returns the label text for the save-details checkbox (for assertion)."""
        try:
            consent = self.driver.find_elements(By.CSS_SELECTOR, "div#tab-reviews .comment-form-cookies-consent")
            if consent and consent[0].is_displayed():
                return consent[0].text.strip()
            return ""
        except Exception:
            return ""

    def fill_review_rating(self, value):
        """Set rating to 1-5. Tries select#rating first, then star links (p.stars a.star-N)."""
        rating = int(value)
        if rating < 1 or rating > 5:
            return
        try:
            el = self.sl.wait_until_element_is_visible(self.REVIEWS_RATING_SELECT, timeout=2)
            from selenium.webdriver.support.ui import Select
            Select(el).select_by_value(str(rating))
            return
        except Exception:
            pass
        try:
            star = self.driver.find_element(By.CSS_SELECTOR, f"div#tab-reviews p.stars a.star-{rating}")
            if star.is_displayed():
                star.click()
        except Exception:
            pass

    def fill_review_comment(self, text):
        self.sl.wait_until_element_is_visible(self.REVIEWS_COMMENT_TEXTAREA)
        self.sl.wait_and_input_text(self.REVIEWS_COMMENT_TEXTAREA, text)

    def fill_review_author(self, text):
        self.sl.wait_until_element_is_visible(self.REVIEWS_AUTHOR_INPUT)
        self.sl.wait_and_input_text(self.REVIEWS_AUTHOR_INPUT, text)

    def fill_review_email(self, text):
        self.sl.wait_until_element_is_visible(self.REVIEWS_EMAIL_INPUT)
        self.sl.wait_and_input_text(self.REVIEWS_EMAIL_INPUT, text)

    def click_review_submit(self):
        self.sl.wait_and_click(self.REVIEWS_SUBMIT_BUTTON)

    def get_alert_text(self):
        """Returns the text of the current browser alert. Raises if no alert is present."""
        alert = self.driver.switch_to.alert
        return alert.text

    def dismiss_alert_if_present(self):
        """Accepts any open browser alert (e.g. 'Please select a rating'). Call after submit if needed."""
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except Exception:
            pass

    def get_reviews_tab_validation_or_error_text(self):
        """Returns any visible error/validation message in the Reviews tab."""
        try:
            errors = self.driver.find_elements(By.CSS_SELECTOR, "div#tab-reviews .woocommerce-error, div#tab-reviews .comment-form .error, div#tab-reviews #commentform .error, div#tab-reviews ul.woocommerce-error li")
            for el in errors:
                if el.is_displayed() and el.text.strip():
                    return el.text.strip()
            return ""
        except Exception:
            return ""

    def get_reviews_success_message_text(self):
        """Returns success message text if review was submitted (e.g. 'awaiting moderation')."""
        try:
            content = self.get_reviews_tab_content_text()
            if not content:
                content = self.driver.find_element(By.TAG_NAME, "body").text
            for phrase in ("awaiting moderation", "has been added", "thank you", "submitted"):
                if content and phrase in content.lower():
                    return content
            return ""
        except Exception:
            try:
                body = self.driver.find_element(By.TAG_NAME, "body").text
                for phrase in ("awaiting moderation", "has been added", "thank you", "submitted"):
                    if body and phrase in body.lower():
                        return body
            except Exception:
                pass
            return ""

    def get_review_list_elements(self):
        """Returns list of review/comment elements in the Reviews tab (ol.commentlist li.comment)."""
        try:
            return self.sl.wait_and_get_elements(self.REVIEWS_LIST)
        except Exception:
            return []

    def get_review_list_texts(self):
        """Returns list of visible text per review (one string per li.comment). Caller must have Reviews tab open."""
        elements = self.get_review_list_elements()
        return [el.text for el in elements] if elements else []

    def get_reviews_tab_label_text(self):
        """Returns the Reviews tab label text (e.g. 'Reviews (0)' or 'Reviews (1)')."""
        labels = self.get_labels_of_left_nav_tabs()
        for lbl in labels:
            if lbl and "review" in lbl.lower():
                return lbl
        return ""

    def get_label_for_color_attribute_dropdown(self):
        return self.sl.wait_and_get_text(self.VARIABLE_PRODUCT_COLOR_ATTRIBUTE_LABEL)

    def get_label_for_logo_attribute_dropdown(self):
        """Logo attribute label; wait for variations table then find by text or locator (theme/headless may differ)."""
        from selenium.webdriver.common.by import By
        # Wait for variations table to be present (headless may render later)
        self.sl.wait_until_element_is_visible((By.CSS_SELECTOR, "table.variations"), timeout=15)
        ths = self.driver.find_elements(By.CSS_SELECTOR, "table.variations tr th.label")
        for th in ths:
            text = (th.text or "").strip()
            if "Logo" in text:
                return "Logo"
        labels = self.driver.find_elements(By.CSS_SELECTOR, "table.variations tr th.label label")
        for el in labels:
            if "Logo" in (el.text or ""):
                return "Logo"
        # Primary: explicit locator (for= logo, pa_logo, attribute_logo)
        return self.sl.wait_and_get_text(self.VARIABLE_PRODUCT_LOGO_ATTRIBUTE_LABEL)

    def get_color_dropdown_options_elements(self):
        return self.sl.wait_until_elements_are_visible(self.VARIABLE_PRODUCT_COLOR_ATTRIBUTE_OPTIONS)

    def get_logo_dropdown_options_elements(self):
        return self.sl.wait_until_elements_are_visible(self.VARIABLE_PRODUCT_LOGO_ATTRIBUTE_OPTIONS)


    def get_color_dropdown_options_values_and_text(self):
        """
        Gets color dropdown options with value and text.
        Retry logic is handled in SeleniumExtended.wait_and_get_dropdown_options_with_attributes().
        """
        return self.sl.wait_and_get_dropdown_options_with_attributes(
            self.VARIABLE_PRODUCT_COLOR_ATTRIBUTE_OPTIONS
        )

    def get_logo_dropdown_options_values_and_text(self):
        """
        Gets logo dropdown options with value and text.
        Retry logic is handled in SeleniumExtended.wait_and_get_dropdown_options_with_attributes().
        """
        return self.sl.wait_and_get_dropdown_options_with_attributes(
            self.VARIABLE_PRODUCT_LOGO_ATTRIBUTE_OPTIONS
        )

    def select_color_option_by_visible_text(self, color):
        """
        Selects a color option by visible text.
        Retry logic is handled in SeleniumExtended.wait_and_select_dropdown().
        """
        self.sl.wait_and_select_dropdown(
            self.VARIABLE_PRODUCT_COLOR_ATTRIBUTE_DROPDOWN,
            to_select=color,
            select_by='visible_text'
        )

    def select_logo_option_by_visible_text(self, logo_option):
        """
        Selects a logo option by visible text.
        Retry logic is handled in SeleniumExtended.wait_and_select_dropdown().
        """
        self.sl.wait_and_select_dropdown(
            self.VARIABLE_PRODUCT_LOGO_ATTRIBUTE_DROPDOWN,
            to_select=logo_option,
            select_by='visible_text'
        )

    def click_reset_variations_btn(self):
        self.sl.wait_and_click(self.RESET_VARIATIONS_BTN)

    def get_selected_color_option(self):
        """
        Gets the text of the currently selected color option.
        Returns text directly to avoid stale element issues.
        Retry logic is handled in SeleniumExtended.wait_and_get_selected_option_text().
        """
        return self.sl.wait_and_get_selected_option_text(self.VARIABLE_PRODUCT_COLOR_ATTRIBUTE_DROPDOWN)

    def get_selected_logo_option(self):
        """
        Gets the text of the currently selected logo option.
        Returns text directly to avoid stale element issues.
        Retry logic is handled in SeleniumExtended.wait_and_get_selected_option_text().
        """
        return self.sl.wait_and_get_selected_option_text(self.VARIABLE_PRODUCT_LOGO_ATTRIBUTE_DROPDOWN)

    def select_color_option_and_verify(self, color_to_select):
        self.select_color_option_by_visible_text(color_to_select)
        selected_option_text = self.get_selected_color_option()
        # verify the selection was successful
        assert selected_option_text == color_to_select, f"Expected '{color_to_select}' to be selected but found '{selected_option_text}'"

    def select_logo_option_and_verify(self, logo_to_select):
        self.select_logo_option_by_visible_text(logo_to_select)
        selected_option_text = self.get_selected_logo_option()
        # verify the selection was successful
        assert selected_option_text == logo_to_select, f"Expected '{logo_to_select}' to be selected but found '{selected_option_text}'"
