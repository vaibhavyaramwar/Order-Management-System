from Apps.Response.CommonResponse import CommonResponse

@staticmethod
def create_common_response(status: str, message: str, data: dict = None) -> CommonResponse:
    """
    Creates a CommonResponse object with the provided status, message, and optional data.

    :param status: The status of the response (e.g., 'success', 'error').
    :param message: A message providing additional information about the response.
    :param data: Optional dictionary containing additional data related to the response.
    :return: An instance of CommonResponse.
    """
    return CommonResponse(status=status, message=message, data=data)