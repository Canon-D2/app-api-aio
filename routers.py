from fastapi import APIRouter

from app.modules.home.routers import router as home_router
from app.modules.user.routers import router as user_router
from app.modules.product.routers import router as product_router
from app.modules.account.router import router as account_router
from app.modules.agent.routers import router as agent_router
from app.modules.appsheet.routers import router as appsheet_router
from app.modules.invoices.routers import router as invoice_router
from app.modules.forum.routers import router as forum_router
from app.modules.festival.routers import router as festival_router
from app.modules.tax.routers import router as tax_router
from app.modules.socket.routers import router as socket_router
from worker.sentry.routers import router as sentry_router
from worker.redis.routers import router as redis_router


api_router = APIRouter()


# Subscribe router
api_router.include_router(home_router)
api_router.include_router(user_router)
api_router.include_router(product_router)
api_router.include_router(account_router)
api_router.include_router(agent_router)
api_router.include_router(appsheet_router)
api_router.include_router(invoice_router)
api_router.include_router(forum_router)
api_router.include_router(festival_router)
api_router.include_router(tax_router)
api_router.include_router(socket_router)
api_router.include_router(sentry_router)
api_router.include_router(redis_router)
