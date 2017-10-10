from enum import Enum


class ViewAction(Enum):
    LIST = "list"
    CREATE = "create"
    EDIT = "edit"
    EDIT_NAME = "edit_name"
    DELETE = "delete"
    UPLOAD = "upload"
    DOWNLOAD = "download"
    DOWNLOAD_TEMPLATE = "download_template"
    ACTIVATE = "activate"
    DEACTIVATE = "deactivate"
    APPROVE = "approve"
    REJECT = "reject"
