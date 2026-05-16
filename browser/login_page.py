from browser.base_page import BasePage

from config import Config


class LoginPage(BasePage):

    LOGIN_BUTTON = "text=Login"

    USERNAME_INPUT = "input[placeholder='Username']"

    PASSWORD_INPUT = "input[placeholder='Password']"

    SUBMIT_BUTTON = "button:has-text('Login'):not(:has-text('Microsoft'))"

    SELECT_BUTTON = "button:has-text('Select')"

    def click_login(self):

        self.click(self.LOGIN_BUTTON)

    def enter_username(self):

        self.fill(
            self.USERNAME_INPUT,
            Config.USERNAME
        )

    def enter_password(self):

        self.fill(
            self.PASSWORD_INPUT,
            Config.PASSWORD
        )

    def click_submit(self):

        self.click(self.SUBMIT_BUTTON)

    def click_select(self):

        self.click(self.SELECT_BUTTON)

    def login_to_application(self):

        self.click_login()

        self.enter_username()

        self.enter_password()

        self.click_submit()

        self.wait_for_load()

        self.click_select()