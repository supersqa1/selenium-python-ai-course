"""
My Account (logged-in) smoke tests. Test case IDs: TC-148, TC-149, TC-150, TC-151, TC-152, TC-153, TC-154.
Uses pre-seeded user (my_account_smoke_user) and logged_in_my_account_smoke fixture
to establish session via API/cookie injection; no UI login.
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
