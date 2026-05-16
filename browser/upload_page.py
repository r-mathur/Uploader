from time import sleep

from browser.base_page import BasePage
import time


class UploadPage(BasePage):

    UPLOAD_DOCUMENT = "button[data-sidebar='menu-button']:has-text('Upload Documents')"

    FOLDER_INPUT = "#folder-upload"

    BROWSER_UPLOAD_BUTTON = "button:has-text('Upload')"

    ADD_TO_QUEUE = "button:has-text('Add to Processing Queue')"

    SCHEMA_CHECKBOX = "div:has-text('Schema: Purchase Order') button[role='checkbox']"

    PROCESS_SELECTED_BUTTON = "button:has-text('Process Selected')"

    PROCESSING_BUTTON = "button:has-text('Processing...')"

    def open_upload_page(self):

        self.click(
            self.UPLOAD_DOCUMENT
        )

    def upload_folder(self, folder_path):

        self.page.locator(
            self.FOLDER_INPUT
        ).set_input_files(folder_path)

        self.click(
            self.BROWSER_UPLOAD_BUTTON,
            timeout=60000
        )

        self.click(
            self.ADD_TO_QUEUE,
            timeout=60000
        )

    def select_schema(self):
        self.click(
            self.SCHEMA_CHECKBOX
        )

    def click_process_selected(self):
        self.click(
            self.PROCESS_SELECTED_BUTTON,
            timeout=60000
        )

    def wait_for_processing_completion(
            self,
            max_wait_minutes=120
    ):

        print("Waiting for document processing to complete...")

        start_time = time.time()

        while True:

            processing_count = self.page.locator(
                self.PROCESSING_BUTTON
            ).count()

            if processing_count == 0:
                print("Processing Completed")

                break

            elapsed_minutes = (
                                      time.time() - start_time
                              ) / 60

            if elapsed_minutes > max_wait_minutes:
                raise Exception(
                    f"Processing exceeded "
                    f"{max_wait_minutes} minutes"
                )

            print(
                "Documents still processing..."
            )

            time.sleep(5)