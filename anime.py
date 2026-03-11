class Anime(object):
    def __init__(self, id, name, status, info, total_number, update_time, image_url, link):
        self.id = id
        self.name = name
        self.status = status
        self.info = info
        self.total_number = total_number
        self.update_time = update_time
        self.image_url = image_url
        self.link = link
class AnimeSubInfo(object):
    def __init__(self, id, name,watch_number,total_number,update_time,image_url,user_link):
        self.id = id
        self.name = name
        self.watch_number = watch_number
        self.total_number = total_number
        self.update_time = update_time
        self.image_url = image_url
        self.user_link = user_link