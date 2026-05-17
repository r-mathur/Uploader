from time import sleep

from browser.base_page import BasePage
from locators.upload_locators import UploadLocators

from urllib.parse import quote

from config import Config

import time


class UploadPage(BasePage):

    UPLOAD_DOCUMENT = (
        "button[data-sidebar='menu-button']:"
        "has-text('Upload Documents')"
    )

    FOLDER_INPUT = "#folder-upload"

    BROWSER_UPLOAD_BUTTON = (
        "button:has-text('Upload')"
    )

    ADD_TO_QUEUE = (
        "button:has-text('Add to Processing Queue')"
    )

    SCHEMA_CHECKBOX = (
        "div:has-text('Schema: Purchase Order') "
        "button[role='checkbox']"
    )

    PROCESS_SELECTED_BUTTON = (
        "button:has-text('Process Selected')"
    )

    PROCESSING_BUTTON = (
        "button:has-text('Processing...')"
    )

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

        print(
            "Waiting for document "
            "processing to complete..."
        )

        start_time = time.time()

        while True:

            processing_count = (
                self.page.locator(
                    self.PROCESSING_BUTTON
                ).count()
            )

            if processing_count == 0:

                print(
                    "Processing Completed"
                )

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

    def get_processing_results(self):

        self.page.locator(
            UploadLocators.EXPAND_SCHEMA
        ).click()

        self.page.wait_for_timeout(2000)

        results = []

        document_rows = self.page.locator(
            "div.flex.items-center."
            "gap-3.p-3.border.rounded-lg"
        )

        row_count = document_rows.count()

        for i in range(row_count):

            row = document_rows.nth(i)

            try:

                file_name = row.locator(
                    "p.font-medium.truncate"
                ).inner_text()

                if row.locator(
                        "div:has-text('Processed')"
                ).count() > 0:

                    status = "Successful"

                elif row.locator(
                        "div:has-text('Error')"
                ).count() > 0:

                    status = "Failed"

                else:

                    status = "Unknown"

                file_name = (
                    file_name
                    .replace("gpt-4o", "")
                    .strip()
                )

                results.append({
                    "file_name": file_name,
                    "status": status
                })

            except Exception as e:

                print(
                    f"Error reading row: {e}"
                )

        return results

    def open_all_documents(self):

        self.click(
            UploadLocators.ALL_DOCUMENTS_MENU
        )

        self.page.wait_for_timeout(3000)

    def search_document(
            self,
            file_name
    ):

        self.fill(
            UploadLocators.SEARCH_BOX,
            file_name
        )

        self.page.wait_for_timeout(3000)

    def select_document_checkbox(self):

        checkboxes = self.page.locator(
            UploadLocators.DOCUMENT_CHECKBOX
        )

        checkboxes.nth(1).click()

        self.page.wait_for_timeout(2000)

    def get_extraction_json_direct(
            self,
            file_name,
            security_group_id,
            folder_date
    ):

        encoded_file_name = quote(
            file_name
        )

        raw_blob_name = quote(
            f"{security_group_id}/"
            f"Purchase Order/"
            f"{folder_date}/"
            f"{file_name}"
        )

        url = (
            f"{Config.DOCUMENT_DATA_URL}"
            f"/document-data/"
            f"{security_group_id}"
            f"__Purchase%20Order__"
            f"{folder_date}__"
            f"{encoded_file_name}"
            f"?raw_blob_name={raw_blob_name}"
            f"&security_group_id="
            f"{security_group_id}"
        )

        response = self.page.request.get(
            url
        )

        if response.status != 200:

            raise Exception(
                f"API Failed: "
                f"{response.status}"
            )

        json_data = response.json()

        return json_data