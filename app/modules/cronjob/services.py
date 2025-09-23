import pytz, httpx
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.base import JobLookupError

from app.mongo.base import BaseCRUD
from app.mongo.engine import engine_aio
from .exception import ErrorCode

cron_crud = BaseCRUD("cronjobs", engine_aio)

class CronsJob:
    def __init__(self, scheduler: AsyncIOScheduler):
        self.scheduler = scheduler
        self.timezone_vn = pytz.timezone("Asia/Ho_Chi_Minh")

    async def add_cron(self, cron: dict):
        cron_id = str(cron["_id"])
        try:
            trigger = CronTrigger.from_crontab(cron["schedule"], timezone=self.timezone_vn)
            self.scheduler.add_job(
                self.execute_job,
                trigger=trigger,
                id=cron_id,
                kwargs={"cron_id": cron_id},
                replace_existing=True,
            )
            print(f"[CRON] Added job: {cron['task']} ({cron_id})")
        except Exception as e:
            print(f"[CRON][ERROR] Failed to add job {cron_id}: {e}")

    async def update_cron(self, cron: dict):
        cron_id = str(cron["_id"])
        try:
            await self.add_cron(cron)
            print(f"[CRON] Updated job: {cron['task']} ({cron_id})")
        except Exception as e:
            print(f"[CRON][ERROR] Failed to update job {cron_id}: {e}")

    async def delete_cron(self, cron: dict):
        cron_id = str(cron["_id"])
        try:
            self.scheduler.remove_job(cron_id)
            print(f"[CRON] Deleted job: {cron['task']} ({cron_id})")
        except JobLookupError:
            print(f"[CRON][WARN] Tried to delete non-existing job {cron_id}")
        except Exception as e:
            print(f"[CRON][ERROR] Failed to delete job {cron_id}: {e}")

    async def execute_job(self, cron_id: str):
        cron = await cron_crud.get_by_id(cron_id)
        if not cron:
            print(f"[CRON][WARN] Job not found in DB: {cron_id}")
            return

        if not cron.get("enable", True):
            print(f"[CRON] Job disabled: {cron.get('task')} ({cron_id})")
            return

        print(f"[CRON] Executing job: {cron.get('task')} ({cron_id})")
        print("  Endpoint:", cron["endpoint"])
        print("  Datetime UTC:", datetime.utcnow())
        print("  Datetime HCM:", datetime.now(tz=self.timezone_vn))

        headers = {}
        if cron.get("header"): headers["Authorization"] = cron["header"]

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                method = cron["method"].upper()
                if method == "GET":
                    response = await client.get(cron["endpoint"], headers=headers)
                elif method == "POST":
                    response = await client.post(cron["endpoint"], headers=headers, json=cron.get("request"))
                elif method == "PUT":
                    response = await client.put(cron["endpoint"], headers=headers, json=cron.get("request"))
                else:
                    print(f"[CRON][ERROR] Unsupported method {method} for job {cron_id}")
                    return

            print("Status code:", response.status_code)
            try:
                data = response.json()
            except Exception:
                data = response.text

            await cron_crud.update_by_id(cron_id, {"response": data})

        except Exception as e:
            print(f"[CRON][ERROR] Exception while executing job {cron_id}: {e}")

    async def add_all_crons(self):
        crons = await cron_crud.search({}, page=1, limit=500)
        for cron in crons["results"]:
            if cron.get("enable", True):
                await self.add_cron(cron)


class CronServices:
    def __init__(self, crud: BaseCRUD):
        self.crud = crud

    async def create(self, data: dict):
        result = await self.crud.create(data)
        await crons_job.add_cron(result)
        return result

    async def update(self, _id: str, data: dict):
        result = await self.crud.update_by_id(_id, data)
        if not result:
            raise ErrorCode.InvalidCronId()
        await crons_job.update_cron(result)
        return result

    async def get(self, _id):
        result = await self.crud.get_by_id(_id)
        if not result:
            raise ErrorCode.InvalidCronId()
        return result

    async def delete(self, _id):
        result = await self.crud.delete_by_id(_id)
        if not result:
            raise ErrorCode.InvalidCronId()
        await crons_job.delete_cron(result)
        return result

    async def search(self, query: dict, page: int, limit: int):
        result = await self.crud.search(query, page, limit)
        return result


scheduler = AsyncIOScheduler(timezone="Asia/Ho_Chi_Minh")
crons_job = CronsJob(scheduler)
