
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import Select

import time

class SeleniumExtended:

    def __init__(self, driver):
        self.driver = driver
        self.default_timeout = 10
        self.max_retries = 3
        self.retry_delay = 0.5  # Delay in seconds between retries
    
    def wait_and_input_text(self, locator, text, timeout=None):
        timeout = timeout if timeout else self.default_timeout
        
        for attempt in range(self.max_retries):
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located(locator)
                )
                element.send_keys(text)
                return  # Success
            except StaleElementReferenceException:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise  # Re-raise on final attempt

    def wait_and_click(self, locator, timeout=None):
        timeout = timeout if timeout else self.default_timeout
        
        for attempt in range(self.max_retries):
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(locator)
                )
                element.click()
                return  # Success
            except StaleElementReferenceException:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise  # Re-raise on final attempt

    def wait_until_element_contains_text(self, locator, text, timeout=None):
        timeout = timeout if timeout else self.default_timeout

        WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text),
            message=f'Element with locator = {locator}, does not contain text: "{text}", after waiting {timeout} seconds.'
        )

    def wait_until_element_is_visible(self, locator_or_element, timeout=None):
        timeout = timeout if timeout else self.default_timeout

        if isinstance(locator_or_element, tuple):
            elem = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator_or_element)
            )
        else:
            import selenium.webdriver.remote.webelement
            if isinstance(locator_or_element, selenium.webdriver.remote.webelement.WebElement):
                elem = WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of(locator_or_element)
                )
            else:
                raise TypeError(f"The locator to check visibility must be a 'tuple' or a 'WebElement'. It was {type(locator_or_element)}")

        return elem

    def wait_until_elements_are_visible(self, locator, timeout=None):
        timeout = timeout if timeout else self.default_timeout

        elem = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_all_elements_located(locator)
        )

        return elem

    def wait_and_get_elements(self, locator, timeout=None, err=None):
        timeout = timeout if timeout else self.default_timeout
        err = err if err else f"Unable to find elements located by '{locator}'," \
                              f"after timeout of {timeout}"
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_all_elements_located(locator)
            )
        except TimeoutException:
            raise TimeoutException(err)

        return elements

    def wait_and_get_text(self, locator, timeout=None):
        timeout = timeout if timeout else self.default_timeout
        
        for attempt in range(self.max_retries):
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located(locator)
                )
                return element.text
            except StaleElementReferenceException:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise  # Re-raise on final attempt

    def wait_until_url_contains(self, url_substring, timeout=None):
        timeout = timeout if timeout else self.default_timeout

        elem = WebDriverWait(self.driver, timeout).until(
            EC.url_contains(url_substring)
        )

    def wait_and_select_dropdown(self, locator, to_select, select_by='visible_text', timeout=None):
        """
        Selects an option from a dropdown with retry logic for stale elements.
        
        :param locator: Locator tuple for the dropdown element
        :param to_select: Value to select (text, index, or value depending on select_by)
        :param select_by: Options are 'visible_text', 'index', or 'value'
        :param timeout: Optional timeout (defaults to self.default_timeout)
        :return: None
        """
        timeout = timeout if timeout else self.default_timeout
        
        for attempt in range(self.max_retries):
            try:
                select_element = self.wait_until_element_is_visible(locator, timeout=timeout)
                select = Select(select_element)
                if select_by.lower() == 'visible_text':
                    select.select_by_visible_text(to_select)
                elif select_by.lower() == 'index':
                    select.select_by_index(to_select)
                elif select_by.lower() == 'value':
                    select.select_by_value(to_select)
                else:
                    raise ValueError(f"Invalid option for 'select_by' parameter. Valid values are 'visible_text', 'index', or 'value'.")
                return  # Success
            except StaleElementReferenceException:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise  # Re-raise on final attempt
    
    def wait_and_get_selected_option_text(self, locator, timeout=None):
        """
        Gets the text of the currently selected option in a dropdown.
        Returns text directly to avoid stale element issues.
        Includes retry logic for stale elements.
        
        :param locator: Locator tuple for the dropdown element
        :param timeout: Optional timeout (defaults to self.default_timeout)
        :return: Text of the selected option (string)
        """
        timeout = timeout if timeout else self.default_timeout
        
        for attempt in range(self.max_retries):
            try:
                select_element = self.wait_until_element_is_visible(locator, timeout=timeout)
                select = Select(select_element)
                return select.first_selected_option.text
            except StaleElementReferenceException:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise  # Re-raise on final attempt
    
    def wait_and_get_dropdown_options_with_attributes(self, locator, value_attr='value', timeout=None):
        """
        Gets dropdown option elements and extracts their value and text attributes.
        Handles stale element exceptions during element retrieval and attribute access.
        
        :param locator: Locator tuple for the dropdown option elements
        :param value_attr: Attribute name to extract as 'value' (default: 'value')
        :param timeout: Optional timeout (defaults to self.default_timeout)
        :return: List of dictionaries with 'value' and 'text' keys
        """
        timeout = timeout if timeout else self.default_timeout
        
        for attempt in range(self.max_retries):
            try:
                options_elements = self.wait_until_elements_are_visible(locator, timeout=timeout)
                value_and_text = []
                for element in options_elements:
                    # Re-check visibility to ensure element is not stale before accessing attributes
                    self.wait_until_element_is_visible(element)
                    value_and_text.append({
                        'value': element.get_attribute(value_attr),
                        'text': element.text
                    })
                return value_and_text
            except StaleElementReferenceException:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    raise  # Re-raise on final attempt