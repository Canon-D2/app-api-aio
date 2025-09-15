import sentry_sdk
from art import tprint
from fastapi import FastAPI
from routers import api_router
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from worker.sentry.config import DSN_SENTRY, ENVIRONMENT
from app.middlewares.logging import LoggingMiddleware
from worker.kafka.services import kafka_service

tprint("APP-API-AIO", font="slant")

app = FastAPI(
    title="APP-API-AIO",
    version="1.0.0",
    description="RestfulAPI backend with JWT authentication",
)

origins = ["http://localhost:3000", "https://dcbao.site"] # Frondend Dev/Production

app.add_middleware(CORSMiddleware,
    # allow_origins=["*"]
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],       # GET, POST, PUT, DELETE, PATCH, OPTIONS
    allow_headers=["*"],       # Content-Type, Authorization,...
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

# Startup event
@app.on_event("startup")
async def startup_event():
    await kafka_service.start_producer()
    await kafka_service.start_consumer()

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    await kafka_service.stop_consumer()
    await kafka_service.stop_producer()