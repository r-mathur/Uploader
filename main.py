import os
import time
import json
from pathlib import Path

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

    # Open Upload Page ONLY ONCE
    upload_page.open_upload_page()

    customer_folders = (
        FolderService.get_customer_folders(
            Config.BASE_FOLDER_PATH
        )
    )

    today_folder = datetime.now().strftime(
        "%d_%m_%Y"
    )

    reports_folder = os.path.join(
        Config.VALIDATION_REPORT_PATH,
        today_folder
    )

    os.makedirs(
        reports_folder,
        exist_ok=True
    )

    validation_excel_path = os.path.join(
        reports_folder,
        "Validation_Report.xlsx"
    )

    for customer_folder in customer_folders:

        if os.path.basename(customer_folder) == "Reports":
            continue

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

        ValidationExcelService.create_excel_if_not_exists(
            excel_path=validation_excel_path,
            sheet_name=customer_name
        )

        # Capture existing files before upload
        existing_files = set()

        try:

            existing_results = (
                upload_page.get_processing_results()
            )

            existing_files = set(

                item["file_name"]

                for item in existing_results
            )

        except:

            pass

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

        # Keep ONLY current customer files
        results = [

            item

            for item in results

            if item["file_name"]
            not in existing_files
        ]

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

            print(
                json.dumps(
                    json_data,
                    indent=4,
                    ensure_ascii=False
                )
            )

            JsonService.save_json_file(
                json_data=json_data,
                date_folder_path=today_folder_path,
                file_name=file
            )

            extraction_data = (
                json_data
                .get("extracted_data", {})
                .get(
                    "gpt_extraction_output",
                    {}
                )
            )

            items = extraction_data.get(
                "items",
                []
            )

            item_count = len(items)

            ValidationExcelService.ensure_item_headers(
                excel_path=validation_excel_path,
                sheet_name=customer_name,
                item_count=item_count
            )

            ValidationExcelService.append_row(
                excel_path=validation_excel_path,
                sheet_name=customer_name,
                file_name=file,
                file_path=os.path.join(
                    today_folder_path,
                    file
                ),
                extraction_data=extraction_data
            )

            TrackerService.update_tracker(
                report_path=report_path,
                file_name=file,
                upload_status="Successful",
                extraction_status="Successful"
            )
            upload_page.select_document_checkbox()

            time.sleep(3)

        # Return to Upload Page for next customer
        upload_page.open_upload_page()

    input(
        "Press Enter to close browser..."
    )

    browser.close_browser()


if __name__ == "__main__":

    main()