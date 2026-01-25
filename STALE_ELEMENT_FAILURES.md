# StaleElementReferenceException Failures - Reference Document

## Tests Failing Due to Stale Element Problem

### 1. `test_variable_product_clear_selection_btn_when_only_logo_is_selected`
- **Test ID:** tcid101
- **File:** `ssqatest/tests/product_detail_page/test_variable_product_options.py`
- **Line:** 98
- **Error:** `StaleElementReferenceException` when accessing `selected_option.text`
- **Root Cause:** 
  - Line 92: Gets `selected_option` WebElement (before reset)
  - Line 97: Clicks reset button (DOM changes)
  - Line 98: Tries to access `selected_option.text` (WebElement is now stale)

**Code Flow:**
```python
# Line 91: Select logo
logo_to_select = 'No'
self.product_page.select_logo_option_by_visible_text(logo_to_select)

# Line 92: Get WebElement (stored in variable)
selected_option = self.product_page.get_selected_logo_option()

# Line 97: Click reset - DOM CHANGES HERE
self.product_page.click_reset_variations_btn()

# Line 98: FAILS - accessing .text on stale WebElement
selected_option = self.product_page.get_selected_logo_option()  # Gets new element
assert selected_option.text == 'Choose an option'  # ❌ STALE ELEMENT ERROR
```

---

### 2. `test_variable_product_clear_selection_btn_when_both_color_and_logo_are_selected`
- **Test ID:** tcid102
- **File:** `ssqatest/tests/product_detail_page/test_variable_product_options.py`
- **Lines:** 122, 126
- **Error:** `StaleElementReferenceException` when accessing `selected_option.text`
- **Root Cause:**
  - Lines 107, 114: Gets WebElements (before reset)
  - Line 119: Clicks reset button (DOM changes)
  - Lines 122, 126: Tries to access `selected_option.text` (WebElements are now stale)

**Code Flow:**
```python
# Lines 105-109: Select color and verify
color_to_select = 'Green'
self.product_page.select_color_option_by_visible_text(color_to_select)
selected_option = self.product_page.get_selected_color_option()  # WebElement stored
assert selected_option.text == color_to_select  # ✅ Works (before reset)

# Lines 112-116: Select logo and verify
logo_to_select = 'No'
self.product_page.select_logo_option_by_visible_text(logo_to_select)
selected_option = self.product_page.get_selected_logo_option()  # WebElement stored
assert selected_option.text == logo_to_select  # ✅ Works (before reset)

# Line 119: Click reset - DOM CHANGES HERE
self.product_page.click_reset_variations_btn()

# Line 122: FAILS - accessing .text on stale WebElement
selected_option = self.product_page.get_selected_color_option()  # Gets new element
assert selected_option.text == 'Choose an option'  # ❌ STALE ELEMENT ERROR

# Line 126: FAILS - accessing .text on stale WebElement
selected_option = self.product_page.get_selected_logo_option()  # Gets new element
assert selected_option.text == 'Choose an option'  # ❌ STALE ELEMENT ERROR
```

---

## Why These Fail

**The Problem:**
1. `get_selected_logo_option()` and `get_selected_color_option()` return a **WebElement** object
2. When `click_reset_variations_btn()` is called, the DOM changes (dropdown resets)
3. The WebElement reference obtained before the reset becomes **stale**
4. When accessing `.text` property on the stale element, Selenium throws `StaleElementReferenceException`

**Why Retry Logic Doesn't Help:**
- The retry logic in `SeleniumExtended` only helps when the exception occurs **during** the element location
- In these tests, the element is successfully located, but becomes stale **after** it's stored
- The `.text` property access happens later, outside the retry logic scope

---

## Solution Required

**Fix:** Modify `get_selected_color_option()` and `get_selected_logo_option()` to:
- Option A: Return the text directly instead of WebElement
- Option B: Re-fetch the element each time before accessing properties (add retry logic in the method itself)

---

## Test Status Reference

| Test Name | Test ID | Status | Notes |
|-----------|---------|--------|-------|
| `test_variable_product_clear_selection_btn_when_only_color_is_selected` | tcid100 | ✅ PASSING | Fixed - methods now return text directly |
| `test_variable_product_clear_selection_btn_when_only_logo_is_selected` | tcid101 | ✅ FIXED | Fixed - added retry logic to select and get methods |
| `test_variable_product_clear_selection_btn_when_both_color_and_logo_are_selected` | tcid102 | ✅ FIXED | Fixed - added retry logic to select and get methods |

## Fix Applied

**Changes Made:**
1. Modified `get_selected_color_option()` and `get_selected_logo_option()` to return text directly instead of WebElement
2. Added retry logic (3 retries with 0.5s delay) to both get methods to handle stale elements
3. Added retry logic to `select_color_option_by_visible_text()` and `select_logo_option_by_visible_text()` to handle stale elements during selection
4. Updated all test code to use text directly (removed `.text` property access)

**Result:** All 6 tests in `test_variable_product_options.py` now pass ✅
