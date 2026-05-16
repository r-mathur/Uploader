from dotenv import load_dotenv

import os


load_dotenv()


class Config:

    BASE_URL = os.getenv("MKS_URL")

    USERNAME = os.getenv("MKS_USERNAME")

    PASSWORD = os.getenv("MKS_PASSWORD")

    HEADLESS = False

    BASE_FOLDER_PATH = r"C:\Users\rishabh.mathur.ext\Videos\Main_Processes\PO_Processing"