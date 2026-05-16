from browser.base_page import BasePage


class UploadPage(BasePage):

    SELECT_FOLDER_DROPDOWN = "button:has-text('Select Files / Folder')"

    SELECT_FOLDER_OPTION = "text=Select Folder"

    FILE_INPUT = "input[type='file']"

    def click_select_dropdown(self):

        self.click(
            self.SELECT_FOLDER_DROPDOWN
        )

    def click_select_folder(self):

        self.click(
            self.SELECT_FOLDER_OPTION
        )

    def upload_folder(self, folder_path):

        self.click_select_dropdown()

        self.click_select_folder()

        self.page.locator(
            self.FILE_INPUT
        ).set_input_files(folder_path)