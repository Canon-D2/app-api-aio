from fastapi import Request, Response
from app.utils.helper import Helper
from app.mongo.base import BaseCRUD
from app.mongo.engine import engine_logs
from starlette.middleware.base import BaseHTTPMiddleware

logs_crud = BaseCRUD("loggings", engine_logs)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = Helper.get_timestamp()

        # Skip certain endpoints (like health checks)
        skip_paths = ["/v1/home/ping"]
        if any(str(request.url).endswith(path) for path in skip_paths):
            return await call_next(request)

        # Prepare request data
        request_data = {
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
            "client": request.client.host if request.client else None,
        }

        # Try to read request body
        try:
            body_bytes = await request.body()
            request_data["body"] = body_bytes.decode("utf-8") if body_bytes else None
        except Exception:
            request_data["body"] = None

        # Extract user_id from JWT if available
        user_id = None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            payload = await Helper.decode_access_token(token=token)
            user_id = payload.get("uid")

        # Call the actual endpoint
        response: Response = await call_next(request)

        # Read and restore response body
        try:
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
            response.body_iterator = iterate_in_chunks(body)
            response_data = body.decode("utf-8")
        except Exception:
            response_data = None

        # Prepare logging data
        log_entry = {
            "user_id": user_id,
            "request": request_data,
            "response": {
                "status_code": response.status_code,
                "body": response_data,
            },
            "process_time": round((Helper.get_timestamp() - start_time) * 1000, 2)  # in ms
        }

        # Save log to database
        try:
            await logs_crud.create(log_entry)
        except Exception as e:
            print("⚠️ Error saving log:", e)

        return response


# Async generator to replace response.body_iterator
async def iterate_in_chunks(data: bytes, chunk_size: int = 4096):
    for i in range(0, len(data), chunk_size):
        yield data[i : i + chunk_size]
