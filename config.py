from dotenv import load_dotenv

import os


load_dotenv()


class Config:

    BASE_URL = os.getenv("MKS_URL")

    USERNAME = os.getenv("MKS_USERNAME")

    PASSWORD = os.getenv("MKS_PASSWORD")

    HEADLESS = False

    BASE_FOLDER_PATH = r"C:\Users\rishabh.mathur.ext\Videos\Main_Processes\Input"

    VALIDATION_REPORT_PATH = (
        r"C:\Users\rishabh.mathur.ext\Videos\Main_Processes\Validation"
    )


    DOCUMENT_DATA_URL = (
        "https://mks-docvalidator-backend-prod-"
        "hae9d6ecbmfebmdh.eastus2-01.azurewebsites.net"
    )

    SECURITY_GROUP_ID = (
        "6f2e215d-5311-4d52-8793-bcb4e1f848c7"
    )