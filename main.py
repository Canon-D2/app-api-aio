import sentry_sdk
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from worker.sentry.config import DSN_SENTRY, ENVIRONMENT

from app.modules.home.routers import router as home_router
from app.modules.user.routers import router as user_router
from app.modules.account.router import router as account_router
from app.modules.agent.routers import router as agent_router
from worker.sentry.routers import router as sentry_router
from app.modules.appsheet.routers import router as appsheet_router


app = FastAPI(
    title="APP-API-AIO",
    description="API backend with JWT authentication",
    version="1.0.0",
    terms_of_service="https://github.com/canon-d2",
    contact={
        "name": "DCBAO",
        "url": "https://dcbao.com/",
        "email": "dcbao.dev@gmail.com"
    }
)

sentry_sdk.init(
    dsn=DSN_SENTRY,
    environment=ENVIRONMENT,
    traces_sample_rate=1.0,
)

# Subscribe router
app.include_router(home_router)
app.include_router(user_router)
app.include_router(account_router)
app.include_router(sentry_router)
app.include_router(agent_router)
app.include_router(appsheet_router)


# ✅ Swagger JWT config
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Config security scheme for JWT
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token"
        }
    }

    # BearerAuth request for all Paths
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method in ["get", "post", "put", "delete", "patch"]:  # tránh lỗi OPTIONS
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


# App function custom schema for app
app.openapi = custom_openapi
