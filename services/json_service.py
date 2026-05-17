import os
import json


class JsonService:

    @staticmethod
    def save_json_file(
            json_data,
            date_folder_path,
            file_name
    ):

        json_folder = os.path.join(
            date_folder_path,
            "JSON"
        )

        os.makedirs(
            json_folder,
            exist_ok=True
        )

        txt_file_name = (
            file_name
            .replace(".pdf", ".txt")
        )

        file_path = os.path.join(
            json_folder,
            txt_file_name
        )

        extraction_output = (
            json_data
            .get("extracted_data", {})
            .get("gpt_extraction_output", {})
        )

        with open(
                file_path,
                "w",
                encoding="utf-8"
        ) as file:

            json.dump(
                extraction_output,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"JSON Saved: {file_path}"
        )