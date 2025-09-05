import sentry_sdk
from fastapi import FastAPI
from routers import api_router
from fastapi.openapi.utils import get_openapi
from worker.sentry.config import DSN_SENTRY, ENVIRONMENT
from app.middlewares.logging import LoggingMiddleware


app = FastAPI(
    title="APP-API-AIO",
    version="1.0.0",
    description="RestfulAPI backend with JWT authentication",
)

# ✅ Swagger JWT config
def custom_openapi():
    if app.openapi_schema: return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["info"]["contact"] = {
        "name": "Dev quèn",
        "url": "https://dcbao.com/",
        "email": "dcbao.dev@gmail.com"
    }
    openapi_schema["info"]["termsOfService"] = "https://github.com/canon-d2"

    # 🔹 Config security scheme for JWT
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter: **'Bearer <JWT>'**, where JWT is the access token"
        }
    }

    # 🔹 BearerAuth request for all Paths
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method in ["get", "post", "put", "delete", "patch"]: 
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


# ⚙️ App function custom schema for Swagger
app.openapi = custom_openapi

# 🔹 Router & Middleware & Sentry
app.include_router(api_router)
app.add_middleware(LoggingMiddleware)
sentry_sdk.init(dsn=DSN_SENTRY, environment=ENVIRONMENT, traces_sample_rate=1.0,)
