import os
import time

from datetime import datetime
from tkinter import messagebox  # remove later for unattended mode

from browser.browser_manager import BrowserManager
from browser.login_page import LoginPage
from browser.upload_page import UploadPage

from services.folder_service import FolderService
from services.tracker_service import TrackerService
from services.json_service import JsonService

from services.validation_excel_service import (
    ValidationExcelService
)

from config import Config


def main():

    browser = BrowserManager()

    page = browser.start_browser()

    login_page = LoginPage(page)

    upload_page = UploadPage(page)

    login_page.login_to_application()

    upload_page.open_upload_page()

    customer_folders = (
        FolderService.get_customer_folders(
            Config.BASE_FOLDER_PATH
        )
    )

    today_folder = datetime.now().strftime(
        "%d_%m_%Y"
    )

    for customer_folder in customer_folders:

        customer_name = os.path.basename(
            customer_folder
        )

        today_folder_path = os.path.join(
            customer_folder,
            today_folder
        )

        if not os.path.exists(
                today_folder_path
        ):

            print(
                f"Today's folder not found for "
                f"{customer_name}"
            )

            continue

        report_path = (
            TrackerService.create_tracker_file(
                today_folder_path
            )
        )

        validation_excel_path = os.path.join(
            today_folder_path,
            f"{customer_name}_Validation.xlsx"
        )

        print(
            f"Uploading Folder: "
            f"{today_folder_path}"
        )

        upload_page.upload_folder(
            today_folder_path
        )

        time.sleep(4)

        upload_page.select_schema()

        time.sleep(1)

        upload_page.click_process_selected()

        upload_page.wait_for_processing_completion()

        results = (
            upload_page.get_processing_results()
        )

        for item in results:

            extraction_status = ""

            if item["status"] == "Failed":

                extraction_status = (
                    "Failed"
                )

            TrackerService.update_tracker(
                report_path=report_path,
                file_name=item["file_name"],
                upload_status=item["status"],
                extraction_status=extraction_status
            )

        print(results)

        successful_files = [

            item["file_name"]

            for item in results

            if item["status"] == "Successful"
        ]

        upload_page.open_all_documents()

        for file in successful_files:

            print(
                f"Searching: {file}"
            )

            upload_page.search_document(
                file
            )

            upload_page.select_document_checkbox()

            json_data = (
                upload_page.get_extraction_json_direct(
                    file_name=file,
                    security_group_id=(
                        Config.SECURITY_GROUP_ID
                    ),
                    folder_date=today_folder
                )
            )

            import json

            print(
                json.dumps(
                    json_data,
                    indent=4
                )
            )

            time.sleep(5)
            upload_page.select_document_checkbox()

            JsonService.save_json_file(
                json_data=json_data,
                date_folder_path=today_folder_path,
                file_name=file
            )
    input(
        "Press Enter to close browser..."
    )

    browser.close_browser()


if __name__ == "__main__":

    main()