from rest_framework import status
from drf.exceptions import APIBaseHttpException


class CsvFileFormatError(APIBaseHttpException):
    http_status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

    def __init__(self):
        self.error_message = 'Only CSV files are accepted.'


class ImportCsvError(APIBaseHttpException):
    http_status_code = status.HTTP_409_CONFLICT

    def __init__(self, msg):
        self.error_message = msg
