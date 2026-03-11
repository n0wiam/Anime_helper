import pymysql
from anime import Anime
from pymysql.cursors import DictCursor

def insert_anime_information(anime: Anime):
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='anime_helper', charset='utf8')
    cursor = conn.cursor()
    sql = """
          INSERT INTO anime(id, name, status, info, total_number, update_time, image_url, link)
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY
          UPDATE
              name =
          VALUES (name), status =
          VALUES (status), info =
          VALUES (info), total_number =
          VALUES (total_number), update_time =
          VALUES (update_time), image_url =
          VALUES (image_url), link =
          VALUES (link)
          """

    params = (
        anime.id,
        anime.name,
        anime.status,
        anime.info,
        anime.total_number,
        anime.update_time,
        anime.image_url,
        anime.link
    )

    cursor.execute(sql, params)
    conn.commit()
    conn.close()


def insert_weekly_anime_list(anime_list: list):
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='anime_helper', charset='utf8')
    cursor = conn.cursor()

    sql = """
          INSERT INTO weekly (date, value)
          VALUES (%s, %s) ON DUPLICATE KEY
          UPDATE value =
          VALUES (value) 
          """

    values = [(idx, val) for idx, val in enumerate(anime_list, start=1)]
    cursor.executemany(sql, values)

    conn.commit()
    cursor.close()
    conn.close()

def show_anime_by_name(anime_name: str, offset: int, limit: int):
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='anime_helper', charset='utf8',cursorclass=DictCursor)
    sql = """
          SELECT id, name, status, info, total_number, update_time, image_url, link FROM anime WHERE name LIKE %s LIMIT %s OFFSET %s
          """
    with conn.cursor() as cursor:
        cursor.execute(sql,(f"%{anime_name}%",limit,offset))
        rows = cursor.fetchall()
    animes = [Anime(**row) for row in rows]
    conn.close()
    return animes

def show_anime_by_page(offset: int, limit: int):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='1234',
        db='anime_helper',
        charset='utf8',
        cursorclass=DictCursor
    )

    try:
        sql = """
            SELECT id, name, status, info, total_number, update_time, image_url, link
            FROM anime
            LIMIT %s OFFSET %s
        """
        with conn.cursor() as cursor:
            cursor.execute(sql, (limit, offset))
            rows = cursor.fetchall()

        animes = [Anime(**row) for row in rows]
        return animes
    finally:
        conn.close()
def insert_subscribe_anime(anime_id: int, watcher_number: int, user_id: int, user_link: str):
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='anime_helper', charset='utf8')
    cursor = conn.cursor()
    sql = """
          INSERT INTO subscribe(user_id, anime_id, watch_number, user_link)
          VALUES (%s, %s, %s, %s) ON DUPLICATE KEY
          UPDATE
              user_id =
          VALUES (user_id), anime_id =
          VALUES (anime_id), watch_number =
          VALUES (watch_number), user_link =
          VALUES (user_link)
          """

    params = (
        user_id,
        anime_id,
        watcher_number,
        user_link
    )

    cursor.execute(sql, params)
    conn.commit()
    conn.close()
def delete_subscribe_anime(anime_id: int, user_id: int):
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='anime_helper', charset='utf8')
    cursor = conn.cursor()
    sql = """
              DELETE FROM subscribe WHERE user_id = %s AND anime_id = %s
              """
    params = (user_id, anime_id)
    cursor.execute(sql, params)
    conn.commit()
    conn.close()

class AnimeSub:
    def __init__(self, anime_id: int, watch_number: int, user_id: int, user_link: str):
        self.anime_id = anime_id
        self.watch_number = watch_number
        self.user_id = user_id
        self.user_link = user_link

def get_anime_follow(user_id:int):
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='anime_helper', charset='utf8',
                           cursorclass=DictCursor)
    sql = """
              SELECT anime_id, watch_number, user_id, user_link FROM subscribe WHERE user_id = %s
              """
    with conn.cursor() as cursor:
        cursor.execute(sql, user_id)
        rows = cursor.fetchall()
    anime_sub_info = [AnimeSub(**row) for row in rows]
    conn.close()
    return anime_sub_info
def get_anime_by_ids(ids: list):
    if not ids:
        return []
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='anime_helper', charset='utf8',
                           cursorclass=DictCursor)
    placeholders = ','.join(['%s'] * len(ids))
    sql = f"""
        SELECT id, name, status, info, total_number, update_time, image_url, link 
        FROM anime
        WHERE id IN ({placeholders})
        """

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, tuple(ids))
            rows = cursor.fetchall()
        animes = [Anime(**row) for row in rows]
        return animes
    finally:
        conn.close()



if __name__ == "__main__":
    # res  = show_anime_by_name("异世界")
    # for anime in res:
    #     print(anime.name)
    # insert_subscribe_anime(123,1,1,"https")
    print("test sql")