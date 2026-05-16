from playwright.sync_api import TimeoutError


class BasePage:

    def __init__(self, page):

        self.page = page

    def navigate(self, url):

        self.page.goto(url)

    def click(self, locator, timeout=30000):

        self.page.locator(locator).wait_for(
            state="visible",
            timeout=timeout
        )

        self.page.locator(locator).click()

    def fill(self, locator, text, timeout=30000):

        self.page.locator(locator).wait_for(
            state="visible",
            timeout=timeout
        )

        self.page.locator(locator).fill(text)

    def get_text(self, locator, timeout=30000):

        self.page.locator(locator).wait_for(
            state="visible",
            timeout=timeout
        )

        return self.page.locator(locator).inner_text()

    def is_visible(self, locator, timeout=5000):

        try:

            self.page.locator(locator).wait_for(
                state="visible",
                timeout=timeout
            )

            return True

        except TimeoutError:

            return False

    def wait_for_load(self):

        self.page.wait_for_load_state(
            "networkidle"
        )

    def screenshot(self, path):

        self.page.screenshot(path=path)

    def press(self, locator, key):

        self.page.locator(locator).press(key)