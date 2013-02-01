#-*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings

from website.models import Video, VideoComentario

from pymongo import MongoClient
from datetime import timedelta, datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        conn = MongoClient()

        db = conn[settings.FEEDBACK_DB]

        for v in Video.objects.all():
            the_time = datetime(v.fecha.year, v.fecha.month, v.fecha.day)
            lt = the_time + timedelta(days=1)

            for f in db.feedbacks.find({"comment": {"$ne": ""}, "datetime": {"$gte": the_time, "$lt": lt}}):
                u = db.users.find_one({"_id": f['user']})

                if not VideoComentario.objects.filter(video=v, content=f['comment'], autor=u['username']).exists():
                    comment = VideoComentario(video=v, content=f['comment'], autor=u['username'], autor_url=u['link'], autor_image_url=u['avatar'])
                    comment.save()
