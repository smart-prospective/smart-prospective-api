from django.http import JsonResponse


class APIError(RuntimeError):
    """
    Exception for a API error, can be converted into an error

    :param string msg: The msg
    """
    status = 400

    def __init__(self, msg):
        super(APIError, self).__init__(msg)
        self.msg = msg

    def __str__(self):
        """
        Format for str

        :return: The exception message
        :rtype: string
        """
        return f"APIError: {self.msg}"
