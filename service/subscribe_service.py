from sql import *
from log import logger
from anime import *

def subscribe_anime(anime_id: int, watcher_number: int, user_id: int, user_link: str):
    try:
        insert_subscribe_anime(anime_id, watcher_number, user_id, user_link)
    except Exception as e:
        logger.error(e)


def unsubscribe_anime(anime_id: int, user_id: int):
    try:
        delete_subscribe_anime(anime_id,user_id)
    except Exception as e:
        logger.error(e)
def get_anime_subscribe(user_id: int):
    anime_subs = get_anime_follow(user_id)
    ids = []
    for item in anime_subs:
        ids.append(item.anime_id)
    animes = get_anime_by_ids(ids)
    # print(ids)
    # print(animes)
    anime_map ={anime.id :anime for anime in animes}
    anime_sub_infos = []
    for item in anime_subs:
        anime = anime_map[item.anime_id]
        anime_sub = AnimeSubInfo(item.anime_id,anime.name,item.watch_number,anime.total_number,anime.update_time,anime.image_url,item.user_link)
        anime_sub_infos.append(anime_sub)
    return anime_sub_infos

