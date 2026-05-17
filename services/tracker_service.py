import os
import shutil

from datetime import datetime

from openpyxl import load_workbook


class TrackerService:

    @staticmethod
    def create_tracker_file(
        date_folder_path
    ):

        today = datetime.now().strftime(
            "%d_%m_%Y"
        )

        template_path = (
            "Template.xlsx"
        )

        report_name = (
            f"Report_{today}.xlsx"
        )

        report_path = os.path.join(
            date_folder_path,
            report_name
        )

        shutil.copy(
            template_path,
            report_path
        )

        return report_path

    @staticmethod
    def update_tracker(
        report_path,
        file_name,
        upload_status="",
        extraction_status=""
    ):

        workbook = load_workbook(
            report_path
        )

        sheet = workbook.active

        next_row = (
            sheet.max_row + 1
        )

        sheet.cell(
            row=next_row,
            column=1
        ).value = file_name

        sheet.cell(
            row=next_row,
            column=2
        ).value = upload_status

        sheet.cell(
            row=next_row,
            column=3
        ).value = extraction_status

        workbook.save(
            report_path
        )

        workbook.close()