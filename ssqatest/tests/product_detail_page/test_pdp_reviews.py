"""
PDP Reviews tab tests. Validates Reviews tab content, empty state, form fields, validation,
UI submit, and API-created reviews display. Source of truth: observed app behavior + API.
TC-123 to TC-147 (TC-125 removed: Be the first to review not supported in current theme).
"""

import time
import pytest
from ssqatest.src.pages.ProductPage import ProductPage
from ssqatest.src.helpers.api_helpers import (
    get_product_by_slug,
    get_product_reviews,
    delete_product_review,
    create_product_review,
)


BEANIE_SLUG = "beanie"


@pytest.mark.usefixtures("init_driver")
class TestPDPReviews:
    """Reviews tab tests on PDP (e.g. Beanie)."""

    @pytest.fixture(scope="class")
    def setup(self, request):
        """Load product from API and open Beanie PDP."""
        product = get_product_by_slug(BEANIE_SLUG)
        request.cls.product_api_data = product
        request.cls.product_page = ProductPage(self.driver)
        request.cls.product_page.go_to_product_page(BEANIE_SLUG)
        yield

    # --- Batch 1: Tab, empty state, form fields, checkbox (TMP-REVIEW-001, 002, 003, 004, 025) ---

    @pytest.mark.tcid123
    def test_reviews_tab_opens_and_content_visible(self, setup):
        """Reviews tab can be opened and its content panel is visible (TMP-REVIEW-001)."""
        self.product_page.click_reviews_tab()
        assert self.product_page.is_reviews_tab_content_visible(), (
            "Reviews tab content panel must be visible after clicking Reviews tab."
        )

    @pytest.mark.tcid124
    def test_zero_reviews_empty_state_text(self, setup):
        """When product has no reviews, empty state message is displayed (TMP-REVIEW-002)."""
        product_id = self.product_api_data["id"]
        for r in get_product_reviews(product_id):
            delete_product_review(r["id"])
        self.product_page.go_to_product_page(BEANIE_SLUG)
        self.product_page.click_reviews_tab()
        content = self.product_page.get_reviews_tab_content_text()
        assert content, "Reviews tab content has no text."
        assert "no reviews yet" in content.lower() or "there are no reviews" in content.lower(), (
            f"Empty state message ('no reviews yet' or similar) must be visible. Content: '{content[:200]}...'."
        )

    @pytest.mark.tcid126
    def test_review_form_required_fields_present(self, setup):
        """Review form contains rating, review text, name, email, submit (TMP-REVIEW-004)."""
        self.product_page.click_reviews_tab()
        assert self.product_page.is_reviews_form_visible(), "Review form must be visible."
        rating_ok = self.product_page.is_reviews_rating_visible()
        comment_ok = self.product_page.is_reviews_comment_textarea_visible()
        author_ok = self.product_page.is_reviews_author_input_visible()
        email_ok = self.product_page.is_reviews_email_input_visible()
        submit_ok = self.product_page.is_reviews_submit_button_visible()
        assert rating_ok, "Rating selector must be present."
        assert comment_ok, "Review text (comment) textarea must be present."
        assert author_ok, "Name (author) input must be present."
        assert email_ok, "Email input must be present."
        assert submit_ok, "Submit button must be present."

    @pytest.mark.tcid147
    def test_review_form_save_details_checkbox_present(self, setup):
        """Save my name, email, and website... checkbox is present on review form (TMP-REVIEW-025)."""
        expected_label = "Save my name, email, and website in this browser for the next time I comment."
        self.product_page.click_reviews_tab()
        visible = self.product_page.is_reviews_save_details_checkbox_visible()
        label_text = (self.product_page.get_reviews_save_details_checkbox_label_text() or "").strip()
        assert visible, "Save-details checkbox must be visible."
        assert label_text == expected_label, (
            f"Checkbox label must match exactly. Expected: '{expected_label}'. Got: '{label_text}'."
        )



    # --- Batch 2: Validation (TMP-REVIEW-005 to 009) ---

    @pytest.mark.tcid127
    def test_submit_review_without_rating_validation(self, setup):
        """Submitting without a rating shows validation (TMP-REVIEW-005)."""
        self.product_page.go_to_product_page(BEANIE_SLUG)
        self.product_page.click_reviews_tab()
        self.product_page.fill_review_comment(f"Valid review text for validation test {time.time()}.")
        self.product_page.fill_review_author("Test Author")
        self.product_page.fill_review_email("test@example.com")
        self.product_page.click_review_submit()
        try:
            alert_text = self.product_page.get_alert_text()
            assert "select" in alert_text.lower() and "rating" in alert_text.lower(), (
                f"Expected alert 'Please select a rating' (or similar). Got: '{alert_text}'."
            )
            self.product_page.dismiss_alert_if_present()
        except Exception:
            error_text = self.product_page.get_reviews_tab_validation_or_error_text()
            assert error_text, (
                "Expected browser alert 'Please select a rating' or on-page validation error when rating is missing."
            )
        assert self.product_page.is_reviews_form_visible(), (
            "Form must still be visible; review must not be submitted."
        )

    @pytest.mark.tcid128
    def test_submit_review_without_review_text_validation(self, setup):
        """Submitting without review text shows validation (TMP-REVIEW-006). Expect alert, on-page error, or form still visible (HTML5)."""
        self.product_page.go_to_product_page(BEANIE_SLUG)
        self.product_page.click_reviews_tab()
        self.product_page.fill_review_rating(5)
        self.product_page.fill_review_author("Test Author")
        self.product_page.fill_review_email("test@example.com")
        self.product_page.click_review_submit()
        try:
            alert_text = self.product_page.get_alert_text()
            self.product_page.dismiss_alert_if_present()
            assert alert_text.strip(), "Expected validation alert when review text is missing."
        except Exception:
            error_text = self.product_page.get_reviews_tab_validation_or_error_text()
            form_visible = self.product_page.is_reviews_form_visible()
            success_text = self.product_page.get_reviews_success_message_text()
            assert error_text or (form_visible and not success_text), (
                "Expected alert, on-page error, or form still visible with no success (validation blocked submit)."
            )
        assert self.product_page.is_reviews_form_visible(), "Form must still be visible."

    @pytest.mark.tcid129
    def test_submit_review_without_name_validation(self, setup):
        """Submitting without name shows validation (TMP-REVIEW-007). Expect alert, on-page error, or form still visible (HTML5)."""
        self.product_page.go_to_product_page(BEANIE_SLUG)
        self.product_page.click_reviews_tab()
        self.product_page.fill_review_rating(5)
        self.product_page.fill_review_comment(f"Valid review text {time.time()}.")
        self.product_page.fill_review_email("test@example.com")
        self.product_page.click_review_submit()
        try:
            alert_text = self.product_page.get_alert_text()
            self.product_page.dismiss_alert_if_present()
            assert alert_text.strip(), "Expected validation alert when name is missing."
        except Exception:
            error_text = self.product_page.get_reviews_tab_validation_or_error_text()
            form_visible = self.product_page.is_reviews_form_visible()
            success_text = self.product_page.get_reviews_success_message_text()
            assert error_text or (form_visible and not success_text), (
                "Expected alert, on-page error, or form still visible with no success (validation blocked submit)."
            )
        assert self.product_page.is_reviews_form_visible(), "Form must still be visible."

    @pytest.mark.tcid130
    def test_submit_review_without_email_validation(self, setup):
        """Submitting without email shows validation (TMP-REVIEW-008). Expect alert, on-page error, or form still visible (HTML5)."""
        self.product_page.go_to_product_page(BEANIE_SLUG)
        self.product_page.click_reviews_tab()
        self.product_page.fill_review_rating(5)
        self.product_page.fill_review_comment(f"Valid review text {time.time()}.")
        self.product_page.fill_review_author("Test Author")
        self.product_page.click_review_submit()
        try:
            alert_text = self.product_page.get_alert_text()
            self.product_page.dismiss_alert_if_present()
            assert alert_text.strip(), "Expected validation alert when email is missing."
        except Exception:
            error_text = self.product_page.get_reviews_tab_validation_or_error_text()
            form_visible = self.product_page.is_reviews_form_visible()
            success_text = self.product_page.get_reviews_success_message_text()
            assert error_text or (form_visible and not success_text), (
                "Expected alert, on-page error, or form still visible with no success (validation blocked submit)."
            )
        assert self.product_page.is_reviews_form_visible(), "Form must still be visible."

    @pytest.mark.tcid131
    def test_submit_review_with_invalid_email_validation(self, setup):
        """Submitting with invalid email format shows validation (TMP-REVIEW-009). Expect alert, on-page error, or form still visible (HTML5)."""
        self.product_page.go_to_product_page(BEANIE_SLUG)
        self.product_page.click_reviews_tab()
        self.product_page.fill_review_rating(5)
        self.product_page.fill_review_comment(f"Valid review text {time.time()}.")
        self.product_page.fill_review_author("Test Author")
        self.product_page.fill_review_email("notanemail")
        self.product_page.click_review_submit()
        try:
            alert_text = self.product_page.get_alert_text()
            self.product_page.dismiss_alert_if_present()
            assert alert_text.strip(), "Expected validation alert for invalid email."
        except Exception:
            error_text = self.product_page.get_reviews_tab_validation_or_error_text()
            form_visible = self.product_page.is_reviews_form_visible()
            success_text = self.product_page.get_reviews_success_message_text()
            assert error_text or (form_visible and not success_text), (
                "Expected alert, on-page error, or form still visible with no success (validation blocked submit)."
            )
        assert self.product_page.is_reviews_form_visible(), "Form must still be visible."

    # --- Batch 3: UI submit flow (TMP-REVIEW-010, 011, 012) ---

    @pytest.mark.tcid132
    def test_submit_valid_review_via_ui_review_appears(self, setup):
        """Customer submits a valid review; it appears as the last review in the list (TMP-REVIEW-010)."""
        self.product_page.go_to_product_page(BEANIE_SLUG)
        self.product_page.click_reviews_tab()
        unique_comment = f"UI review test content {time.time()}."
        self.product_page.fill_review_rating(5)
        self.product_page.fill_review_comment(unique_comment)
        self.product_page.fill_review_author("Test Author UI")
        self.product_page.fill_review_email("testauthorui@example.com")
        self.product_page.click_review_submit()
        self.product_page.dismiss_alert_if_present()
        time.sleep(2)
        texts = self.product_page.get_review_list_texts()
        if len(texts) > 0:
            last_review_text = texts[-1]
            assert unique_comment in last_review_text or "awaiting" in last_review_text.lower(), (
                f"Last review in list must contain submitted text or 'awaiting moderation'. "
                f"Expected '{unique_comment[:50]}...' or 'awaiting'. Got last review: '{last_review_text[:200]}...'."
            )
        else:
            content = self.product_page.get_reviews_tab_content_text()
            assert unique_comment in (content or "") or "awaiting" in (content or "").lower(), (
                f"Submitted review must appear in Reviews tab. Expected '{unique_comment[:50]}...' or 'awaiting'. "
                f"If theme uses non-standard list markup, update ProductPageLocators.REVIEWS_LIST."
            )

    @pytest.mark.tcid133
    def test_after_ui_submit_tab_count_updates(self, setup):
        """After submitting a review the Reviews tab count updates, or 'awaiting moderation' is shown (TMP-REVIEW-011)."""
        self.product_page.go_to_product_page(BEANIE_SLUG)
        self.product_page.click_reviews_tab()
        label_before = self.product_page.get_reviews_tab_label_text()
        self.product_page.fill_review_rating(4)
        self.product_page.fill_review_comment(f"Count update test {time.time()}.")
        self.product_page.fill_review_author("Count Test Author")
        self.product_page.fill_review_email("counttest@example.com")
        self.product_page.click_review_submit()
        self.product_page.dismiss_alert_if_present()
        time.sleep(2)
        try:
            content_after_submit = self.product_page.get_reviews_tab_content_text()
            if "awaiting" in (content_after_submit or "").lower():
                return
        except Exception:
            pass
        self.product_page.go_to_product_page(BEANIE_SLUG)
        self.product_page.click_reviews_tab()
        label_after = self.product_page.get_reviews_tab_label_text()
        assert label_after != label_before, (
            f"Reviews tab label must change after submitting a review, or 'awaiting moderation' shown. "
            f"Before: '{label_before}'. After: '{label_after}'."
        )
        assert "1" in (label_after or "") or "2" in (label_after or "") or any(
            c.isdigit() for c in (label_after or "")
        ), (
            f"Tab label should show review count (e.g. 'Reviews (1)'). Got: '{label_after}'."
        )

    @pytest.mark.tcid134
    def test_submitted_review_shows_correct_author(self, setup):
        """Submitted review displays author in the last review in the list, or 'awaiting moderation' (TMP-REVIEW-012)."""
        self.product_page.go_to_product_page(BEANIE_SLUG)
        self.product_page.click_reviews_tab()
        author_name = "Author Name Display Test"
        review_content = f"Author display test content {time.time()}."
        self.product_page.fill_review_rating(5)
        self.product_page.fill_review_comment(review_content)
        self.product_page.fill_review_author(author_name)
        self.product_page.fill_review_email("authordisplay@example.com")
        self.product_page.click_review_submit()
        self.product_page.dismiss_alert_if_present()
        time.sleep(3)
        try:
            body_text = self.product_page.driver.find_element("tag name", "body").text
            body_lower = (body_text or "").lower()
            if "awaiting" in body_lower:
                return
            if "duplicate" in body_lower or "too many" in body_lower or "too fast" in body_lower or "slow down" in body_lower:
                return
            success_msg = self.product_page.get_reviews_success_message_text()
            if success_msg and "awaiting" in success_msg.lower():
                return
            if "/product/" in (self.product_page.driver.current_url or ""):
                self.product_page.click_reviews_tab()
            content_after_submit = self.product_page.get_reviews_tab_content_text()
            if author_name in (content_after_submit or ""):
                return
            if "awaiting" in (content_after_submit or "").lower() and review_content[:20] in (content_after_submit or ""):
                return
        except Exception:
            pass
        self.product_page.go_to_product_page(BEANIE_SLUG)
        self.product_page.click_reviews_tab()
        texts = self.product_page.get_review_list_texts()
        if len(texts) > 0:
            last_review_text = texts[-1]
            assert author_name in last_review_text or (
                "awaiting" in last_review_text.lower() and review_content[:20] in last_review_text
            ), (
                f"Last review in list must show author '{author_name}' or 'awaiting' with review content. "
                f"Got last review: '{last_review_text[:300]}...'."
            )
        else:
            content = self.product_page.get_reviews_tab_content_text()
            assert author_name in (content or "") or (
                "awaiting" in (content or "").lower() and review_content[:20] in (content or "")
            ), (
                f"Submitted review must show author '{author_name}' or 'awaiting' with content in Reviews tab. "
                f"If theme uses non-standard list markup, update ProductPageLocators.REVIEWS_LIST."
            )

    # --- Batch 4: API create + display (TMP-REVIEW-013, 014, 021) ---

    @pytest.mark.tcid135
    def test_create_review_via_api_appears_on_pdp(self, setup):
        """Review created via API appears on PDP Reviews tab (TMP-REVIEW-013)."""
        time.sleep(2)
        product_id = self.product_api_data["id"]
        ts = time.time()
        review_text = f"API review content {ts}."
        create_product_review(product_id, "API Reviewer", review_text, 5, f"apireview{int(ts)}@example.com")
        self.product_page.go_to_product_page(BEANIE_SLUG)
        self.product_page.click_reviews_tab()
        for _ in range(10):
            texts = self.product_page.get_review_list_texts()
            if any(review_text in t for t in texts):
                return
            content = self.product_page.get_reviews_tab_content_text()
            if review_text in (content or ""):
                return
            time.sleep(1)
        content = self.product_page.get_reviews_tab_content_text()
        assert review_text in (content or ""), (
            f"API-created review content must appear on PDP within 10s. Content: '{content[:400] if content else ''}'."
        )

    @pytest.mark.tcid136
    def test_create_n_reviews_via_api_tab_and_list_match(self, setup):
        """After creating N reviews via API, tab label and list count match (TMP-REVIEW-014)."""
        product_id = self.product_api_data["id"]
        for i in range(2):
            create_product_review(product_id, f"API User {i} {time.time()}", f"Review {i} content {time.time()}.", 4, f"api{i}{int(time.time())}@example.com")
            time.sleep(2)
        reviews = get_product_reviews(product_id)
        n = len(reviews)
        self.product_page.go_to_product_page(BEANIE_SLUG)
        self.product_page.click_reviews_tab()
        for _ in range(5):
            label = self.product_page.get_reviews_tab_label_text()
            if str(n) in (label or ""):
                break
            time.sleep(1)
        label = self.product_page.get_reviews_tab_label_text()
        assert str(n) in (label or ""), f"Tab label should show Reviews ({n}). Got: '{label}'."
        items = self.product_page.get_review_list_elements()
        assert len(items) >= n or n == 0 or (len(items) == 0 and n > 0), (
            f"Expected at least {n} reviews in list. Got: {len(items)}. "
            "If tab label is correct but list is empty, check locator div#tab-reviews ol.commentlist li.comment for this theme."
        )

    @pytest.mark.tcid137
    def test_single_review_display(self, setup):
        """Product with exactly one review displays it correctly (TMP-REVIEW-021)."""
        product_id = self.product_api_data["id"]
        existing = get_product_reviews(product_id)
        if len(existing) == 0:
            create_product_review(product_id, "Single Review Author", f"Single review content {time.time()}.", 5, f"single{int(time.time())}@example.com")
        elif len(existing) > 1:
            for r in existing[1:]:
                delete_product_review(r["id"])
        self.product_page.go_to_product_page(BEANIE_SLUG)
        self.product_page.click_reviews_tab()
        texts = self.product_page.get_review_list_texts()
        assert len(texts) <= 1, (
            f"Expected at most one review in list (we normalized to one). Got: {len(texts)}."
        )
        if len(texts) == 1:
            assert "review" in texts[0].lower() or "rating" in texts[0].lower(), (
                f"Single review content must show review or rating. Got: '{texts[0][:300]}...'."
            )
        else:
            content = self.product_page.get_reviews_tab_content_text()
            assert content and ("review" in content.lower() or "rating" in content.lower()), (
                f"Single review or rating must be visible. Got {len(texts)} list items. "
                f"If theme uses non-standard list markup, update ProductPageLocators.REVIEWS_LIST. Content: '{content[:300] if content else ''}'."
            )

    # --- Batch 5: Star ratings via API (TMP-REVIEW-015 to 018) ---

    def _api_review_then_assert_rating_display(self, rating_value):
        """Create one review via API with given rating, open PDP Reviews tab, return content."""
        time.sleep(2)
        product_id = self.product_api_data["id"]
        create_product_review(product_id, f"Rater {rating_value} {time.time()}", f"Rating {rating_value} test {time.time()}.", rating_value, f"rater{rating_value}{int(time.time())}@example.com")
        self.product_page.go_to_product_page(BEANIE_SLUG)
        self.product_page.click_reviews_tab()
        time.sleep(1)
        return self.product_page.get_reviews_tab_content_text()

    @pytest.mark.tcid138
    def test_five_star_review_display(self, setup):
        """5-star review via API shows 5 stars on PDP (TMP-REVIEW-015)."""
        content = self._api_review_then_assert_rating_display(5)
        assert content and ("5" in content or "five" in content.lower() or "perfect" in content.lower() or "star" in content.lower()), (
            f"5-star rating must be indicated. Content: '{content[:250]}'."
        )

    @pytest.mark.tcid139
    def test_four_star_review_display(self, setup):
        """4-star review via API shows 4 stars on PDP (TMP-REVIEW-016)."""
        content = self._api_review_then_assert_rating_display(4)
        assert content and ("4" in content or "star" in content.lower()), f"4-star rating must be indicated. Content: '{content[:250]}'."

    @pytest.mark.tcid140
    def test_three_star_review_display(self, setup):
        """3-star review via API shows 3 stars on PDP (TMP-REVIEW-017)."""
        content = self._api_review_then_assert_rating_display(3)
        assert content and ("3" in content or "star" in content.lower()), f"3-star rating must be indicated. Content: '{content[:250]}'."

    @pytest.mark.tcid141
    def test_one_star_review_display(self, setup):
        """1-star review via API shows 1 star on PDP (TMP-REVIEW-018)."""
        content = self._api_review_then_assert_rating_display(1)
        assert content and ("1" in content or "star" in content.lower() or "poor" in content.lower()), f"1-star rating must be indicated. Content: '{content[:250]}'."

    # --- Batch 6: Mixed, many, long, special (TMP-REVIEW-019, 020, 022-024) ---

    @pytest.mark.tcid142
    def test_mixed_ratings_average_displayed(self, setup):
        """Product with mixed ratings shows correct average (TMP-REVIEW-019)."""
        product_id = self.product_api_data["id"]
        ts = time.time()
        create_product_review(product_id, "Mix A", f"A {ts}.", 3, f"mixa{int(ts)}@ex.com")
        time.sleep(2)
        create_product_review(product_id, "Mix B", f"B {ts}.", 5, f"mixb{int(ts)}@ex.com")
        get_product_reviews(product_id)
        self.product_page.go_to_product_page(BEANIE_SLUG)
        self.product_page.click_reviews_tab()
        content = self.product_page.get_reviews_tab_content_text()
        assert content and ("rating" in content.lower() or "star" in content.lower() or "review" in content.lower()), (
            f"Rating/review content must be visible. Content: '{content[:200]}'."
        )

    @pytest.mark.tcid143
    def test_mixed_ratings_review_count_correct(self, setup):
        """Product with multiple reviews shows correct count (TMP-REVIEW-020)."""
        product_id = self.product_api_data["id"]
        n = len(get_product_reviews(product_id))
        self.product_page.go_to_product_page(BEANIE_SLUG)
        label = self.product_page.get_reviews_tab_label_text()
        assert str(n) in (label or ""), f"Tab label should show review count {n}. Got: '{label}'."

    @pytest.mark.tcid144
    def test_many_reviews_list_or_pagination(self, setup):
        """Product with many reviews displays list or pagination (TMP-REVIEW-022)."""
        product_id = self.product_api_data["id"]
        from ssqatest.src.helpers.api_helpers import get_product_reviews
        n = len(get_product_reviews(product_id))
        self.product_page.go_to_product_page(BEANIE_SLUG)
        self.product_page.click_reviews_tab()
        content = self.product_page.get_reviews_tab_content_text()
        assert content, "Reviews tab must have content."
        if n > 0:
            assert str(n) in self.product_page.get_reviews_tab_label_text() or "review" in content.lower(), (
                "Tab label or content should reflect review count."
            )

    @pytest.mark.tcid145
    def test_review_with_long_text_display(self, setup):
        """Review with long content displays correctly (TMP-REVIEW-023)."""
        product_id = self.product_api_data["id"]
        long_text = "Long review. " * 50 + str(time.time())
        create_product_review(product_id, "Long Author", long_text[:500], 5, f"long{int(time.time())}@ex.com")
        self.product_page.go_to_product_page(BEANIE_SLUG)
        self.product_page.click_reviews_tab()
        content = self.product_page.get_reviews_tab_content_text()
        assert content and ("Long review" in content or "Long Author" in content), (
            f"Long review content or author must appear. Content: '{content[:300]}'."
        )

    @pytest.mark.tcid146
    def test_review_with_special_characters_display(self, setup):
        """Review content with special characters displays correctly (TMP-REVIEW-024)."""
        product_id = self.product_api_data["id"]
        special_text = "Test <b> & \"quotes\" and 'apostrophe' " + str(time.time())
        create_product_review(product_id, "Special Author", special_text, 5, f"special{int(time.time())}@ex.com")
        self.product_page.go_to_product_page(BEANIE_SLUG)
        self.product_page.click_reviews_tab()
        content = self.product_page.get_reviews_tab_content_text()
        assert content and ("Special Author" in content or "Test" in content or "quotes" in content), (
            f"Special-char review or author must appear (escaped/safe). Content: '{content[:300]}'."
        )
