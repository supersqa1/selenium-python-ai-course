# Test Failure Report

**Date:** January 24, 2026  
**Total Tests:** 36  
**Passed:** 29  
**Failed:** 7  
**Pass Rate:** 80.6%

---

## Failure Summary Table

| Test File | Test Name | Error Type | Root Cause | Impact |
|-----------|-----------|------------|------------|--------|
| `test_verify_expired_coupon_message.py` | `test_expired_coupon_message` | `TimeoutException` | Element not found - likely locator issue or timing problem in `get_displayed_error()` | Medium - Cart functionality |
| `test_end_to_end_checkout_guest_user.py` | `test_end_to_end_checkout_guest_user` | `TimeoutException` | Cannot find cart items: `'tr.cart_item td.product-name'` - element not present after navigation | High - E2E flow broken |
| `test_product_detail_page_variable_product_smoke.py` | `test_variable_product_page_verify_main_image` | `TimeoutException` | Element not found - likely image element locator or timing issue | Medium - Product page validation |
| `test_product_detail_page_variable_product_smoke.py` | `test_variable_product_page_logo_dropdown_label` | `TimeoutException` | Element not found - logo dropdown label locator issue | Low - UI validation |
| `test_variable_product_add_to_cart.py` | `test_variable_product_pdp_select_options_add_to_cart` | `TimeoutException` | Cannot find cart items: `'tr.cart_item td.product-name'` - cart page element not found | High - Add to cart flow |
| `test_variable_product_options.py` | `test_variable_product_clear_selection_btn_when_only_logo_is_selected` | `StaleElementReferenceException` | `get_selected_logo_option()` returns WebElement that becomes stale after DOM changes | High - Stale element handling |
| `test_variable_product_options.py` | `test_variable_product_clear_selection_btn_when_both_color_and_logo_are_selected` | `StaleElementReferenceException` | `get_selected_logo_option()` returns WebElement that becomes stale after reset button click | High - Stale element handling |

---

## Detailed Analysis

### StaleElementReferenceException Failures (2 tests)

**Problem:** 
- `get_selected_color_option()` and `get_selected_logo_option()` return `select.first_selected_option` which is a WebElement
- When the reset button is clicked, the DOM changes and the stored WebElement reference becomes stale
- The retry logic in `SeleniumExtended` doesn't help because the WebElement is already stored before the DOM change

**Affected Methods:**
- `ProductPage.get_selected_color_option()` - line 173
- `ProductPage.get_selected_logo_option()` - line 178

**Why Retry Logic Doesn't Help:**
- The WebElement is obtained and stored before the DOM change
- When accessing `.text` property later, the element is already stale
- Need to re-fetch the element each time, not store the WebElement reference

---

### TimeoutException Failures (5 tests)

**Common Pattern:**
- Elements not found within 10-second timeout
- Likely causes:
  1. Locator issues (wrong selector)
  2. Timing issues (page not fully loaded)
  3. Element not present (application behavior changed)

**Specific Issues:**

1. **Cart Item Locator** (2 tests):
   - Locator: `'tr.cart_item td.product-name'`
   - Tests: `test_end_to_end_checkout_guest_user`, `test_variable_product_pdp_select_options_add_to_cart`
   - Issue: Cart items not found after navigation/adding to cart

2. **Error Message Element** (1 test):
   - Test: `test_expired_coupon_message`
   - Issue: `get_displayed_error()` cannot find error element

3. **Product Image Element** (1 test):
   - Test: `test_variable_product_page_verify_main_image`
   - Issue: Main product image element not found

4. **Logo Dropdown Label** (1 test):
   - Test: `test_variable_product_page_logo_dropdown_label`
   - Issue: Logo dropdown label element not found

---

## Recommendations

### Priority 1: Fix StaleElementReferenceException
- Modify `get_selected_color_option()` and `get_selected_logo_option()` to return text directly instead of WebElement
- Or re-fetch the element each time before accessing properties

### Priority 2: Investigate TimeoutException Issues
- Verify locators are correct
- Add explicit waits before accessing elements
- Check if application behavior has changed

### Priority 3: Improve Error Handling
- Add better error messages with context
- Consider increasing timeout for specific operations
- Add element presence checks before interactions
