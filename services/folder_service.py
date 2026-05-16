import os


class FolderService:

    @staticmethod
    def get_customer_folders(base_path):

        customer_folders = []

        for item in os.listdir(base_path):

            full_path = os.path.join(base_path, item)

            if os.path.isdir(full_path):

                customer_folders.append(full_path)

        return customer_folders