import time
from datetime import datetime
from tkinter import messagebox  # remove later for unattended mode

from browser.browser_manager import BrowserManager
from browser.login_page import LoginPage
from browser.upload_page import UploadPage

from services.folder_service import FolderService

from config import Config


def main():

    browser = BrowserManager()

    page = browser.start_browser()

    login_page = LoginPage(page)

    upload_page = UploadPage(page)

    login_page.login_to_application()

    upload_page.open_upload_page()

    customer_folders = FolderService.get_customer_folders(
        Config.BASE_FOLDER_PATH
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

        if not os.path.exists(today_folder_path):

            print(
                f"Today's folder not found for "
                f"{customer_name}"
            )

            continue

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

        messagebox.showinfo(
            "Debug",
            f"Files Uploaded for {customer_name}"
        )

    input("Press Enter to close browser...")

    browser.close_browser()


if __name__ == "__main__":

    import os

    main()