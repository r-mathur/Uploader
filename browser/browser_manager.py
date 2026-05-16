from playwright.sync_api import sync_playwright

from config import Config


class BrowserManager:

    def __init__(self):

        self.playwright = sync_playwright().start()

        self.browser = None

        self.page = None

    def start_browser(self):

        self.browser = self.playwright.chromium.launch(
            channel="msedge",
            headless=False,
            args=["--start-maximized"]
        )

        context = self.browser.new_context(
            no_viewport=True
        )

        self.page = context.new_page()

        self.page.goto(
            Config.BASE_URL
        )

        self.page.wait_for_load_state(
            "networkidle"
        )

        return self.page

    def close_browser(self):

        self.browser.close()

        self.playwright.stop()