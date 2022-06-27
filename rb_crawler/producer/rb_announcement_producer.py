from bakdata.rb.announcement.v1.announcement_pb2 import Announcement
from common.base_producer import BaseProducer


class RbAnnouncementProducer(BaseProducer):
    TOPIC = "rb-announcements"

    def __init__(self):
        super().__init__(RbAnnouncementProducer.TOPIC, Announcement)

    def get_key(self, announcement: Announcement):
        return announcement.id
