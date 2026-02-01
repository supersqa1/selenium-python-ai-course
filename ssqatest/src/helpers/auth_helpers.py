"""
Authentication helpers for tests that need a logged-in session.
Uses HTTP login (e.g. wp-login.php) to obtain cookies and injects them
into the Selenium WebDriver so the browser is logged in without UI login.
"""

import requests


def login_via_requests_and_inject_cookies(base_url, username, password, driver):
    """
    Log in via WordPress wp-login.php using requests, then inject the
    session cookies into the given Selenium WebDriver so subsequent
    navigations are authenticated.

    :param base_url: Site base URL (e.g. https://demostore.supersqa.com), no trailing slash.
    :param username: Login username (or email).
    :param password: Login password.
    :param driver: Selenium WebDriver instance.
    :raises AssertionError: If login response indicates failure (e.g. still on wp-login).
    """
    login_url = base_url.rstrip("/") + "/wp-login.php"
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (selenium-test)"})

    resp = session.post(
        login_url,
        data={
            "log": username,
            "pwd": password,
            "wp-submit": "Log In",
        },
        allow_redirects=True,
        timeout=15,
    )
    resp.raise_for_status()

    # If we still have wp-login in the final URL, login likely failed
    if "wp-login.php" in resp.url:
        raise AssertionError(
            f"Login failed: final URL is still wp-login.php. Check credentials for user '{username}'."
        )

    # Ensure driver is on the same origin so cookies apply
    driver.get(base_url)

    # Selenium add_cookie uses current page domain; do not pass domain so it matches.
    for cookie in session.cookies:
        cookie_dict = {
            "name": cookie.name,
            "value": cookie.value,
            "path": cookie.path or "/",
        }
        if cookie.expires:
            cookie_dict["expiry"] = int(cookie.expires)
        if cookie.secure:
            cookie_dict["secure"] = True
        try:
            driver.add_cookie(cookie_dict)
        except Exception as e:
            if "wordpress_logged_in" in cookie.name or "wordpress_" in cookie.name:
                raise e
