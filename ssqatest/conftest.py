# -*- coding: utf-8 -*-
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChOptions
from selenium.webdriver.firefox.options import Options as FFOptions

import os
import time
import allure
from dotenv import load_dotenv
from ssqatest.src.helpers.config_helpers import validate_environment, get_base_url, get_test_user
from ssqatest.src.helpers.auth_helpers import login_via_requests_and_inject_cookies

# Load environment variables from .env file (if it exists)
# This happens automatically before any fixtures or tests run
load_dotenv()

# Validate environment variables at startup
# This checks required variables and warns about missing optional ones
validate_environment()

@pytest.fixture(scope="class")
def init_driver(request):

    supported_browsers = ['chrome', 'ch', 'headlesschrome', 'firefox', 'ff', 'headlessfirefox']

    browser = os.environ.get('BROWSER', None)
    if not browser:
        supported_list = ", ".join(supported_browsers)
        raise EnvironmentError(
            "Missing required environment variable: BROWSER. "
            "Source env.sh or set export BROWSER=chrome. "
            "Supported browsers: {}".format(supported_list)
        )

    browser = browser.lower()
    if browser not in supported_browsers:
        raise ValueError(
            "Unsupported browser: '{}'. Supported: {}. Set via: export BROWSER=chrome".format(
                browser, ", ".join(supported_browsers)
            )
        )

    if browser in ('chrome', 'ch'):
        driver = webdriver.Chrome()
    elif browser in ('firefox', 'ff'):
        driver = webdriver.Firefox()
    elif browser in ('headlesschrome'):
        chrome_options = ChOptions()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_bin = os.environ.get('CHROME_BIN')
        if chrome_bin:
            chrome_options.binary_location = chrome_bin
        driver = webdriver.Chrome(options=chrome_options)
    elif browser == 'headlessfirefox':
        ff_options = FFOptions()
        ff_options.add_argument("--disable-gpu")
        ff_options.add_argument("--no-sandbox")
        ff_options.add_argument("--headless")
        driver = webdriver.Firefox(options=ff_options)

    # Standard viewport for deterministic UI tests (Full HD desktop)
    driver.set_window_size(1920, 1080)

    request.cls.driver = driver
    yield
    driver.quit()


@pytest.fixture(scope="class")
def logged_in_my_account_smoke(request):
    """
    Establishes a logged-in session once per test class using my_account_smoke_user
    (test_users.json, credentials from env). Depends on init_driver: use with
    @pytest.mark.usefixtures('init_driver', 'logged_in_my_account_smoke').
    Framework rule: new class, new login — if a test needs a fresh login, put it in a different class.
    """
    driver = request.cls.driver
    user = get_test_user("my_account_smoke_user")
    base_url = get_base_url()
    login_via_requests_and_inject_cookies(base_url, user["username"], user["password"], driver)
    driver.get(base_url.rstrip("/") + "/my-account/")
    yield


@pytest.fixture(scope="class")
def logged_in_user_with_one_order(request):
    """
    Logged-in session using user_with_one_order (test_users.json). Use for tests that need
    a user with at least one order (e.g. Orders tab order list). Depends on init_driver.
    """
    driver = request.cls.driver
    user = get_test_user("user_with_one_order")
    base_url = get_base_url()
    login_via_requests_and_inject_cookies(base_url, user["username"], user["password"], driver)
    driver.get(base_url.rstrip("/") + "/my-account/")
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    On test failure, capture a screenshot and attach it to the pytest-html report
    (only for tests that use init_driver and only when the html plugin is used).
    """
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when != "call" or not report.failed:
        report.extra = extra
        return

    xfail = hasattr(report, "wasxfail")
    if report.skipped and xfail:
        report.extra = extra
        return

    pytest_html = item.config.pluginmanager.getplugin("html")
    if pytest_html is None:
        report.extra = extra
        return

    if "init_driver" not in item.fixturenames:
        report.extra = extra
        return

    try:
        request = item.funcargs.get("request")
        driver = getattr(request.cls, "driver", None) if request and hasattr(request, "cls") else None
        if driver is None:
            report.extra = extra
            return

        # Brief pause so the page has time to paint (helps avoid white screenshot in CI/headless)
        time.sleep(0.5)
        screenshot_base64 = driver.get_screenshot_as_base64()
        extra.append(pytest_html.extras.image(screenshot_base64))

        results_dir = os.environ.get("RESULTS_DIR", ".")
        if results_dir:
            screenshot_dir = os.path.join(results_dir, "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            safe_name = item.nodeid.replace("::", "_").replace("/", "_").replace(" ", "_").strip("_") + ".png"
            screenshot_path = os.path.join(screenshot_dir, safe_name)
            try:
                driver.save_screenshot(screenshot_path)
            except Exception:
                pass
    except Exception:
        pass

    report.extra = extra

