import logging
from config.setting import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

import jwt
from starlette.requests import Request
from typing import Callable, Coroutine, Any
from starlette.responses import Response, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("CustomMiddleware")


def error_response(error_msg: str, status_code: int) -> JSONResponse:
    """
    Logs the error message and returns a JSONResponse with the error message.

    Args:
        error_msg (str): the error message to be logged and returned in the JSONResponse
        status_code (int): the HTTP status code

    Returns:
        JSONResponse: JSONResponse containing the error message
    """
    logger.error(error_msg)
    return JSONResponse(
        content={"error": {"message": error_msg}},
        status_code=status_code,
    )


def validate_token(token: str) -> bool:
    """
    Validates the token by checking if it is equal to the SECRET_KEY.

    Args:
        token (str): The token to be validated.

    Returns:
        bool: True if the token is valid, False otherwise.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise False
        return True
    except jwt.ExpiredSignatureError:
        return False


class CustomMiddleware(BaseHTTPMiddleware):
    """
    Custom middleware for handling content-type of JavaScript files and serving
    index.html as a fallback for other requests.
    """

    async def dispatch(
            self,
            request: Request,
            call_next: Callable[[Request], Coroutine[Any, Any, Response]],
    ) -> Response:
        """
        Process the request and set the content-type header for JavaScript files or
        serve the index.html file as a fallback for other requests.

        Args:
            request (Request): The incoming request.
            call_next (Callable): The next middleware or handler in the stack.

        Returns:
            Response: The generated response.
        """
        logger.debug(f"Request URL path: {request.url.path}")
        if request.url.path.startswith("/api"):
            try:
                if "Authorization" not in request.headers:
                    return error_response("Unauthorized", 401)
                token_header = request.headers["Authorization"]
                if token_header.startswith("Bearer "):
                    token = token_header.split("Bearer ")[-1]
                    if not validate_token(token):
                        return error_response("Unauthorized", 401)
                else:
                    return error_response("Token should begin with Bearer", 400)
            except Exception as e:
                return error_response(f"{e}", 400)
            response = await call_next(request)
            return response
