class APIBaseHttpException(Exception):

    def __str__(self):
        http_status = getattr(self, 'http_status', '')
        error_message = getattr(self, 'error_message', '')
        return '{class_name}: {http_status} - {error_message}'.format(
            class_name=self.__class__.__name__,
            http_status=http_status,
            error_message=error_message
        )

    def get_detailed_info(self):
        return {
            'error_message': getattr(self, 'error_message', '')
        }
