class CommonResponse:
    """
    A class to represent a common response structure.
    """

    def __init__(self, status: str, message: str, data: dict = None):
        """
        Initializes the CommonResponse with status, message, and optional data.

        :param status: The status of the response (e.g., 'success', 'error').
        :param message: A message providing additional information about the response.
        :param data: Optional dictionary containing additional data related to the response.
        """
        self.status = status
        self.message = message
        self.data = data if data is not None else {}