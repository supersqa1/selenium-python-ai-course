"""
Simple product PDP tests for Beanie (slug: beanie).
Validates application functionality and UI against API as source of truth.
Batch 1: TC-103–TC-107. Batch 2: TC-108–TC-112.
"""

import pytest

from ssqatest.src.pages.ProductPage import ProductPage
from ssqatest.src.pages.CartPage import CartPage
from ssqatest.src.helpers.api_helpers import get_product_by_slug, update_product
from ssqatest.src.helpers.generic_helpers import convert_html_to_text


BEANIE_SLUG = "beanie"


@pytest.mark.usefixtures("init_driver")
class TestSimpleProductPDPBeanie:
    """PDP tests for simple product Beanie. API data used as source of truth for assertions."""

    @pytest.fixture(scope="class")
    def setup(self, request):
        """Load Beanie product from API and open Beanie PDP."""
        product = get_product_by_slug(BEANIE_SLUG)
        request.cls.product_api_data = product
        request.cls.product_page = ProductPage(self.driver)
        request.cls.product_page.go_to_product_page(BEANIE_SLUG)
        yield

    @pytest.mark.tcid103
    def test_beanie_pdp_product_name(self, setup):
        """UI must display the same product title as the catalog (API)."""
        displayed_name = self.product_page.get_displayed_product_name()
        expected_name = self.product_api_data["name"]
        assert displayed_name == expected_name, (
            f"Product title on PDP does not match catalog. Expected: '{expected_name}'. Displayed: '{displayed_name}'."
        )

    @pytest.mark.tcid104
    def test_beanie_pdp_main_image(self, setup):
        """Main product image must be visible and match catalog image URL."""
        main_image_src = self.product_page.get_url_of_displayed_main_image()
        assert main_image_src, "Main product image has no src/data-src."
        api_image_urls = [img["src"] for img in self.product_api_data.get("images", [])]
        assert api_image_urls, "API product has no images; cannot validate PDP image."
        # Site may serve same URL or a variant (e.g. resized); check main image is one of catalog images
        assert main_image_src in api_image_urls, (
            f"PDP main image URL not in catalog. Displayed: '{main_image_src}'. Catalog: {api_image_urls}."
        )

    @pytest.mark.tcid105
    def test_beanie_pdp_simple_product_type_text(self, setup):
        """UI must show 'This is a simple product.' so customers know no options are required."""
        product_type_text = self.product_page.get_product_type_text()
        expected = "This is a simple product."
        assert product_type_text == expected, (
            f"Product type text on PDP incorrect. Expected: '{expected}'. Actual: '{product_type_text}'."
        )

    @pytest.mark.tcid106
    def test_beanie_pdp_add_to_cart_button_visible(self, setup):
        """Add to cart button must be visible and labeled 'Add to cart'."""
        add_to_cart_elem = self.product_page.get_add_to_cart_button_element()
        assert add_to_cart_elem.is_displayed(), "Add to cart button is not visible."
        assert add_to_cart_elem.text.strip() == "Add to cart", (
            f"Add to cart button text incorrect. Expected: 'Add to cart'. Actual: '{add_to_cart_elem.text}'."
        )

    # --- Batch 2: Price, meta, description (run before add-to-cart so browser stays on PDP) ---

    def _normalize_price_text(self, text):
        """Collapse whitespace so UI text can be compared to API (HTML-stripped) text."""
        if not text:
            return ""
        normalized = " ".join(text.split())
        normalized = normalized.replace(". $", ".$")
        normalized = normalized.replace(" Current ", "Current ")
        return normalized

    @pytest.mark.tcid108
    def test_beanie_pdp_single_price_display(self, setup):
        """Single price must be displayed and match catalog (API price_html)."""
        displayed_price = self.product_page.get_displayed_product_price()
        assert displayed_price, "Price section has no displayed text."
        api_price_text = convert_html_to_text(self.product_api_data["price_html"]).strip()
        assert self._normalize_price_text(displayed_price) == self._normalize_price_text(api_price_text), (
            f"PDP price does not match catalog. Expected: '{api_price_text}'. Displayed: '{displayed_price}'."
        )

    @pytest.mark.tcid109
    def test_beanie_pdp_sale_price_display(self, setup):
        """When product is on sale, original and current price must be shown. API puts Beanie on sale, then we assert."""
        product_id = self.product_api_data["id"]
        original_regular = self.product_api_data.get("regular_price") or ""
        original_sale = self.product_api_data.get("sale_price") or ""
        regular_for_sale = self.product_api_data.get("regular_price") or "20"
        sale_price_value = "18"
        try:
            update_product(product_id, {"regular_price": regular_for_sale, "sale_price": sale_price_value})
            self.product_page.go_to_product_page(BEANIE_SLUG)
            product_on_sale = get_product_by_slug(BEANIE_SLUG)
            displayed_price = self.product_page.get_displayed_product_price()
            api_price_text = convert_html_to_text(product_on_sale["price_html"]).strip()
            assert self._normalize_price_text(displayed_price) == self._normalize_price_text(api_price_text), (
                f"Sale price display does not match catalog. Expected: '{api_price_text}'. Displayed: '{displayed_price}'."
            )
        finally:
            update_product(product_id, {"regular_price": original_regular, "sale_price": original_sale})

    @pytest.mark.tcid110
    def test_beanie_pdp_sku(self, setup):
        """SKU on PDP must match catalog."""
        displayed_sku = self.product_page.get_displayed_sku_and_label()
        expected_sku = f'SKU: {self.product_api_data["sku"]}'
        assert displayed_sku == expected_sku, (
            f"SKU on PDP does not match catalog. Expected: '{expected_sku}'. Displayed: '{displayed_sku}'."
        )

    @pytest.mark.tcid111
    def test_beanie_pdp_category(self, setup):
        """Category on PDP must match catalog."""
        displayed_category = self.product_page.get_displayed_category_and_label()
        api_category_name = self.product_api_data["categories"][0]["name"]
        expected_category = f"Category: {api_category_name}"
        assert displayed_category == expected_category, (
            f"Category on PDP does not match catalog. Expected: '{expected_category}'. Displayed: '{displayed_category}'."
        )

    @pytest.mark.tcid112
    def test_beanie_pdp_description_section(self, setup):
        """Description header and content must be present and match catalog."""
        description_header = self.product_page.get_displayed_product_description_header()
        assert description_header == "Description", (
            f"Description section header incorrect. Expected: 'Description'. Actual: '{description_header}'."
        )
        displayed_description = self.product_page.get_displayed_product_description_full()
        api_description_text = convert_html_to_text(self.product_api_data["description"]).strip()
        assert displayed_description == api_description_text, (
            f"Description content does not match catalog. Expected: '{api_description_text[:80]}...'. "
            f"Displayed: '{displayed_description[:80] if displayed_description else ''}...'."
        )

    @pytest.mark.tcid107
    def test_beanie_pdp_add_simple_product_to_cart(self, setup):
        """User can add Beanie to cart and see correct product name in cart. Runs last (navigates to cart)."""
        expected_name_in_cart = self.product_api_data["name"]
        self.product_page.go_to_product_page(BEANIE_SLUG)
        self.product_page.click_add_to_cart_button()
        self.product_page.click_view_cart_btn_on_add_to_cart_success_message_box()
        cart_page = CartPage(self.driver)
        cart_page.verify_cart_page_url()
        products_in_cart = cart_page.get_all_product_names_in_cart()
        assert expected_name_in_cart in products_in_cart, (
            f"Product not found in cart after add to cart. Expected name: '{expected_name_in_cart}'. "
            f"Cart contents: {products_in_cart}."
        )
