from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.conf import settings

from models import Video
from datetime import datetime, time


class iTunesFeed(Rss201rev2Feed):
    mime_type = 'application/xml'

    def rss_attributes(self):
        attrs = super(iTunesFeed, self).rss_attributes()

        attrs['xmlns:itunes'] = 'http://www.itunes.com/dtds/podcast-1.0.dtd'

        return attrs

    def add_root_elements(self, handler):
        super(iTunesFeed, self).add_root_elements(handler)

        handler.addQuickElement('itunes:category', 'Technology')
        handler.addQuickElement('itunes:category', 'Gadgets')
        handler.addQuickElement('itunes:category', 'Tech News')


class VideoFeed(Feed):
    feed_type = iTunesFeed
    title = 'Mejorando.la'
    link = 'http://mejorando.la'
    author_name = 'Mejorando.la INC'
    description = 'Un show en vivo de gente que crea Internet, todos los jueves a las 4pm GMT-5'
    description_template = 'feeds/video_description.html'

    def items(self):
        return Video.objects.filter(podcast=True, activado=True).order_by('-fecha')

    def item_enclosure_url(self, item):
        return 'https://mejorando.la%s%s.mp3' % (settings.PODCASTS_URL, item.slug)

    def item_enclosure_mime_type(self, item):
        return 'audio/mpeg'

    def item_pubdate(self, item):
        return datetime.combine(item.fecha, time())

    def item_title(self, item):
        return item.titulo
