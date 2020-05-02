from django.db import models
from django.db.models import Q
from classes.models import News, Nation
import datetime

class NewsManager(models.Manager):
    def getLatestNews(self, limit=False):
        querySet = models.query.QuerySet(model=News, using=self._db)
        conditions = (
            Q(pub_date__lt=datetime.datetime.now())
        )
        result = querySet.filter(conditions).order_by('-pub_date').distinct()
        if limit and len(result) > limit:
            return result[:limit]
        else:
            return result.all()

    def getNewsbyId(self, newsId):
        all_news = self.getLatestNews()

        querySet = models.query.QuerySet(model=News, using=self._db)
        conditions = (
            Q(id__exact=newsId)
        )
        result = querySet.filter(conditions)[0]
        result_index = list(all_news).index(result)
        previous_news, next_news = False, False
        if result_index > 0:
            next_news = all_news[result_index-1]
        if result_index < len(all_news) - 1:
            previous_news = all_news[result_index+1]
        return result, previous_news, next_news

class NationsManager(models.Manager):
    def getAllNations(self):
        querySet = models.query.QuerySet(model=Nation, using=self._db)
        result = querySet.order_by('-abbr')
        return result

    def getNationbyAbbr(self, nationAbbr):
        querySet = models.query.QuerySet(model=Nation, using=self._db)
        conditions = (
            Q(abbr__iexact=nationAbbr)
        )
        result = querySet.filter(conditions).distinct()
        return result[0]