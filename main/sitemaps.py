from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "daily"

    def items(self):
        return [
            'main',
            'shop:shop'
        ]
    
    def location(self, item):
        return reverse(item)
