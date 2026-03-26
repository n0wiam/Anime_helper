from urllib import request

from fastapi import FastAPI,Request,Form
from sql import show_anime_by_name
from sql import show_anime_by_page
from pydantic import BaseModel
from service.download_anime import download
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from service.subscribe_service import subscribe_anime as subscribe
from service.subscribe_service import unsubscribe_anime as unsubscribe
from service.subscribe_service import get_anime_subscribe
from service.ai_service import get_ai_anime_recommendation
from log import logger

app = FastAPI()
scheduler = AsyncIOScheduler()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
# class AnimeVO(BaseModel):
#     id : int
#     name : str
#     status : str
#     info : str
#     total_number : int
#     update_time : str
#     image_url : str
#     link : str

@app.get("/test")
def test():
    return {"test": "test"}

class QueryDTO(BaseModel):
    name: str
    number: int = 1
class SubscribeRequest(BaseModel):
    anime_id: int
    watch_number: int
    user_link: str
@app.post("/anime/search")
def get_anime(request: Request,query_dto: QueryDTO):
    limit = 10
    offset = (query_dto.number - 1) * limit
    res = show_anime_by_name(query_dto.name,offset,limit)
    result = [
        {
            "id": u.id,
            "name": u.name,
            "status": u.status,
            "info": u.info,
            "total_number": u.total_number,
            "update_time": u.update_time,
            "image_url": u.image_url,
            "link": u.link,
        }
        for u in res
    ]
    return templates.TemplateResponse(
        "anime.html",
        {
            "request": request,
            "animes": result,
            "keyword": query_dto.name,
            "page": query_dto.number
        }
    )

class DownloadDTO(BaseModel):
    id: int
    number: int
@app.post("/download")
async def download_anime(download_dto: DownloadDTO):
    url = "https://skr.skr2.cc:666/voddetail/"+str(download_dto.id)+"/"
    print(url)
    file_name = str(download_dto.id)+"-"+str(download_dto.number)
    # asyncio.create_task(download(url,download_dto.number,file_name))
    loop = asyncio.get_running_loop()
    loop.run_in_executor(None,download,url,download_dto.number,file_name)
    return {"status": "downloading..."}

@app.get("/anime/page/{number}")
def get_anime_page(number: int):
    limit = 10
    offset = (number-1)*limit
    res = show_anime_by_page(offset,limit)
    result = [
        {
            "id": u.id,
            "name": u.name,
            "status": u.status,
            "info": u.info,
            "total_number": u.total_number,
            "update_time": u.update_time,
            "image_url": u.image_url,
            "link": u.link,
        }
        for u in res
    ]
    return result

@app.get("/anime")
def anime_page(request: Request):
    return templates.TemplateResponse(
        "anime.html",
        {
            "request": request,
            "animes": [],
            "keyword": "",
            "page": 1
        }
    )
@app.post("/anime/sub")
def subscribe_anime(request: Request,anime_sub: SubscribeRequest):
    user_id = 1
    try:
        subscribe(anime_sub.anime_id,anime_sub.watch_number,user_id,anime_sub.user_link)
    except Exception as e:
        logger.error(e)
        return {
            "status": "error",
            "msg": "订阅失败"
        }
    return {
        "status": "success",
        "msg": "订阅成功"
    }
@app.get("/anime/unsub/{anime_id}")
def unsubscribe_anime(request: Request,anime_id: int):
    user_id = 1
    try:
        unsubscribe(anime_id,user_id)
    except Exception as e:
        logger.error(e)
        return {"status": "error", "msg": str(e)}
    return {"status": "success"}

@app.get("/anime/subscriptions")
def get_anime_follow(request: Request):
    res = get_anime_subscribe(1)
    result = [
        {
            "id": u.id,
            "name": u.name,
            "watch_number": u.watch_number,
            "total_number": u.total_number,
            "update_time": u.update_time,
            "image_url": u.image_url,
            "user_link": u.user_link,
        }
        for u in res
    ]
    return templates.TemplateResponse(
        "subscriptions.html",
        {
            "request": request,
            "subscriptions": result
        }
    )

@app.get("/anime/recommendation/{year}")
def get_anime_recommendation(request: Request,year: int):
    if (year == 1) or (year == 10):
        res = get_ai_anime_recommendation(year)
        result = [
            {
                "id": u.id,
                "name": u.name,
                "status": u.status,
                "info": u.info,
                "total_number": u.total_number,
                "update_time": u.update_time,
                "image_url": u.image_url,
                "link": u.link,
            }
            for u in res
        ]
        return templates.TemplateResponse(
            "recommendation.html",
            {
                "request": request,
                "recommendations": result
            }
        )
    else :
        return {"status": "error", "msg": "时间范围暂时不支持"}

# @app.on_event("startup")
# async def start_scheduler():
#     scheduler.add_job(
#         update_anime(),
#         trigger="cron",
#         hour=0,
#         minute=0
#     )
#     scheduler.start()