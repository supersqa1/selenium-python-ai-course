# -*- coding: utf-8 -*-
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChOptions
from selenium.webdriver.firefox.options import Options as FFOptions

import os
import allure
from dotenv import load_dotenv
from ssqatest.src.helpers.config_helpers import validate_environment

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
        raise EnvironmentError(
            "❌ Missing required environment variable: BROWSER\n"
            "   This is required for all tests.\n"
            "   \n"
            "   To fix:\n"
            "   1. Source the environment file: source env.sh\n"
            "   2. Or set manually: export BROWSER=chrome\n"
            "   \n"
            f"   Supported browsers: {', '.join(supported_browsers)}"
        )

    browser = browser.lower()
    if browser not in supported_browsers:
        raise ValueError(
            f"❌ Unsupported browser: '{browser}'\n"
            f"   \n"
            f"   Supported browsers: {', '.join(supported_browsers)}\n"
            f"   Set via: export BROWSER=chrome (or one of the supported options)"
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
        driver = webdriver.Chrome(options=chrome_options)
    elif browser == 'headlessfirefox':
        ff_options = FFOptions()
        ff_options.add_argument("--disable-gpu")
        ff_options.add_argument("--no-sandbox")
        ff_options.add_argument("--headless")
        driver = webdriver.Firefox(options=ff_options)

    request.cls.driver = driver
    yield
    driver.quit()



# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     pytest_html = item.config.pluginmanager.getplugin("html")
#     outcome = yield
#     report = outcome.get_result()
#     if report.when == "call":
#         # always add url to report
#         xfail = hasattr(report, "wasxfail")
#         # check if test failed
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             is_frontend_test = True if 'init_driver' in item.fixturenames else False
#             if is_frontend_test:
#                 results_dir = os.environ.get("RESULTS_DIR")
#                 if not results_dir:
#                     raise Exception("Environment variable 'RESULTS_DIR' must be set.")
#
#                 screen_shot_path = os.path.join(results_dir, item.name + '.png')
#                 driver_fixture = item.funcargs['request']
#                 allure.attach(driver_fixture.cls.driver.get_screenshot_as_png(),
#                               name='screenshot',
#                               attachment_type=allure.attachment_type.PNG)


### FOR: generating only pytest-html report
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     pytest_html = item.config.pluginmanager.getplugin("html")
#     outcome = yield
#     report = outcome.get_result()
#     extra = getattr(report, "extra", [])

#     if report.when == "call":
#         # always add url to report
#         xfail = hasattr(report, "wasxfail")
#         # check if test failed
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             is_frontend_test = True if 'init_driver' in item.fixturenames else False
#             if is_frontend_test:
#                 results_dir = os.environ.get("RESULTS_DIR")
#                 if not results_dir:
#                     raise Exception("Environment variable 'RESULTS_DIR' must be set.")
#
#                 screen_shot_path = os.path.join(results_dir, item.name + '.png')
#                 driver_fixture = item.funcargs['request']
#                 driver_fixture.cls.driver.save_screenshot(screen_shot_path)
#                 # only add additional html on failure
#                 # extra.append(pytest_html.extras.html('<div style="background:orange;">Additional HTML</div>'))
#                 extra.append(pytest_html.extras.image(screen_shot_path))
#
#         report.extra = extra

#                 allure.attach(driver_fixture.cls.driver.get_screenshot_as_png(),
#                               name='screenshot',
#                               attachment_type=allure.attachment_type.PNG)


## FOR: generating only pytest-html report
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     pytest_html = item.config.pluginmanager.getplugin("html")
#     outcome = yield
#     report = outcome.get_result()
#     extra = getattr(report, "extra", [])
#     if report.when == "call":
#         # always add url to report
#         xfail = hasattr(report, "wasxfail")
#         # check if test failed
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             is_frontend_test = True if 'init_driver' in item.fixturenames else False
#             if is_frontend_test:
#                 results_dir = os.environ.get("RESULTS_DIR")
#                 if not results_dir:
#                     raise Exception("Environment variable 'RESULTS_DIR' must be set.")
#
#                 screen_shot_path = os.path.join(results_dir, item.name + '.png')
#                 driver_fixture = item.funcargs['request']
#                 driver_fixture.cls.driver.save_screenshot(screen_shot_path)
#                 # only add additional html on failure
#                 # extra.append(pytest_html.extras.html('<div style="background:orange;">Additional HTML</div>'))
#                 extra.append(pytest_html.extras.image(screen_shot_path))
#
#         report.extra = extra


# #========
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     pytest_html = item.config.pluginmanager.getplugin("html")
#     outcome = yield
#     report = outcome.get_result()
#     extra = getattr(report, "extra", [])
#     if report.when == "call":
#         # always add url to report
#         extra.append(pytest_html.extras.url("http://www.example.com/"))
#         xfail = hasattr(report, "wasxfail")
#         # check if test failed
#         if (report.skipped and xfail) or (report.failed and not xfail):
#             is_frontend_test = True if 'init_driver' in item.fixturenames else False
#             if is_frontend_test:
#                 results_dir = os.environ.get("RESULTS_DIR")
#                 if not results_dir:
#                     raise Exception("Environment variables 'RESULTS_DIR' must be set")
#                 screenshot_path = os.path.join(results_dir, item.name + '.png')
#                 driver_fixture = item.funcargs['request']
#                 driver = driver_fixture.cls.driver.save_screenshot(screenshot_path)
#             # only add additional html on failure
#             # extra.append(pytest_html.extras.html("<div>Additional HTML</div>"))
#             # extra.append(pytest_html.extras.image("/Users/mneelaka/PycharmProjects/python_selenium_course/ssqatest/image.jpeg"))
#             extra.append(pytest_html.extras.image("screenshot_path"))
#
#         report.extra = extra

