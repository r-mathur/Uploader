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

    customer_folders = FolderService.get_customer_folders(
        Config.BASE_FOLDER_PATH
    )

    for folder in customer_folders:

        print(f"Uploading Folder: {folder}")

        upload_page.upload_folder(folder)

    input("Press Enter to close browser...")

    browser.close_browser()


if __name__ == "__main__":

    main()