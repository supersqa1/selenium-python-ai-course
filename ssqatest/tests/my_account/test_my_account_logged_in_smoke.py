"""
My Account (logged-in) smoke tests. Test case IDs: TC-148–TC-154, TC-155 (Orders tab), TC-156 (Orders empty state).
Uses pre-seeded user (my_account_smoke_user) and logged_in_my_account_smoke fixture
to establish session via API/cookie injection; no UI login.
TC-157 (Orders tab with order list) is in a separate class with user_with_one_order.
"""

import pytest
from ssqatest.src.pages.MyAccountSignedIn import MyAccountSignedIn
from ssqatest.src.pages.Header import Header


EXPECTED_LEFT_NAV_LINKS = ["Dashboard", "Orders", "Downloads", "Addresses", "Account details", "Log out"]
EXPECTED_HEADER_MENU_ITEMS = ["Home", "Cart", "Checkout", "My account", "Sample Page"]


@pytest.mark.usefixtures("init_driver", "logged_in_my_account_smoke")
class TestMyAccountLoggedInSmoke:
    """Smoke tests for My Account when user is logged in (session via fixture)."""

    @pytest.mark.tcid148
    def test_my_account_page_loads_account_area_visible(self):
        """TC-148: Logged-in My Account page loads; account area visible; login form NOT shown; Log out visible."""
        page = MyAccountSignedIn(self.driver)
        assert page.is_account_area_visible(), "Account area should be visible and login form should not be shown."
        assert page.is_logout_link_visible(), "Log out link should be visible."
        assert 1 == 2, "fail on purpose to test the test"

    @pytest.mark.tcid149
    def test_left_nav_shows_expected_links(self):
        """TC-149: Left sidebar shows all expected account navigation links."""
        page = MyAccountSignedIn(self.driver)
        link_texts = page.get_left_nav_link_texts()
        for expected in EXPECTED_LEFT_NAV_LINKS:
            assert expected in link_texts, f"Left nav should contain '{expected}'. Got: {link_texts}"

    @pytest.mark.tcid150
    def test_main_content_visible(self):
        """TC-150: Main content area is visible (default tab)."""
        page = MyAccountSignedIn(self.driver)
        assert page.is_main_content_visible(), "Main content area should be visible."

    @pytest.mark.tcid151
    def test_log_out_link_visible_in_left_nav(self):
        """TC-151: Log out link is present and visible in left nav."""
        page = MyAccountSignedIn(self.driver)
        assert page.is_logout_link_visible(), "Log out link should be visible in left sidebar."

    @pytest.mark.tcid152
    def test_breadcrumb_shows_my_account(self):
        """TC-152: Breadcrumb trail includes My account."""
        page = MyAccountSignedIn(self.driver)
        breadcrumb = page.get_breadcrumb_text()
        assert "My account" in breadcrumb, f"Breadcrumb should contain 'My account'. Got: {breadcrumb}"

    @pytest.mark.tcid153
    def test_account_details_tab_shows_form_elements(self):
        """TC-153: Account details tab opens and shows key form elements."""
        page = MyAccountSignedIn(self.driver)
        page.click_account_details_link()
        assert page.is_account_details_form_visible(), (
            "Account details section should show First name, Last name, Display name, Email, Save changes button."
        )

    @pytest.mark.tcid154
    def test_header_nav_visible_when_logged_in(self):
        """TC-154: Header navigation is present when logged in."""
        header = Header(self.driver)
        menu_texts = header.get_all_menu_item_text()
        for expected in EXPECTED_HEADER_MENU_ITEMS:
            assert expected in menu_texts, f"Header should show '{expected}'. Got: {menu_texts}"

    @pytest.mark.tcid155
    def test_orders_tab_opens_and_content_visible(self):
        """TC-155: Orders tab opens and order section content is visible."""
        page = MyAccountSignedIn(self.driver)
        page.click_orders_link()
        assert page.is_main_content_visible(), "Orders section (main content) should be visible."
        content = page.get_orders_content_text()
        assert content, "Orders tab content should not be empty (table or empty state)."

    @pytest.mark.tcid156
    def test_orders_tab_empty_state_when_no_orders(self):
        """TC-156: When user has no orders, Orders tab shows empty state message."""
        page = MyAccountSignedIn(self.driver)
        page.click_orders_link()
        content = page.get_orders_content_text()
        assert "no order" in content.lower() or "no orders" in content.lower() or "have been made" in content.lower(), (
            f"Empty state message expected (e.g. 'No order has been made yet'). Got: {content[:200]}..."
        )


@pytest.mark.usefixtures("init_driver", "logged_in_user_with_one_order")
class TestMyAccountOrdersTabWithOrders:
    """Orders tab when user has at least one order (user_with_one_order)."""

    @pytest.mark.tcid157
    def test_orders_tab_shows_order_list(self):
        """TC-157: When user has at least one order, Orders tab shows at least one order in the list."""
        page = MyAccountSignedIn(self.driver)
        page.click_orders_link()
        assert page.is_orders_table_visible(), "Orders table should be visible when user has orders."
        row_count = page.get_orders_table_row_count()
        assert row_count >= 1, f"At least one order row expected. Got: {row_count}"
