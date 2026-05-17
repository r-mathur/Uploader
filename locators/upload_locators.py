class UploadLocators:

    EXPAND_SCHEMA = (
        "span:has-text('Schema: Purchase Order')"
    )

    DOCUMENT_ROWS = (
        "div.rounded-lg"
    )

    STATUS_BADGE = (
        "div.inline-flex.rounded-full"
    )

    FILE_NAME = (
        "p.font-medium.truncate"
    )

    ALL_DOCUMENTS_MENU = (
        "button[data-sidebar='menu-button']:has-text('All Documents')"
    )

    SEARCH_BOX = (
        "input[placeholder*='Search by Document ID']"
    )

    DOCUMENT_CHECKBOX = (
        "button[role='checkbox']"
    )

    EXPORT_SELECTED_BUTTON = (
        "button:has-text('Export Selected')"
    )