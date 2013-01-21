#-*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings

from website.models import Video

import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        for v in Video.objects.all():
            if os.path.exists(os.path.join(settings.PODCASTS_ROOT, '%s.mp3' % v.slug)):
                v.podcast = True
                v.save()
