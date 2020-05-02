''' 
Managers retrieve model objects by conditions. All Manager files are written following the same layout.

    CONDITIONS LOOKUPS:
    -   exact: strict match. None = null. Case sensitive
    -   iexact: case insensitive exact match.
    -   contains: case sensitive contained content
    -   icontains: case insensive contained content
    -   in: in list match. Strings are allowed.
    -   gt: >; gte: >=; lt: <; lte: <=
    -   startswith: case sensitive
    -   istartswith: case insensive
    -   endswith: case sensitive contained content
    -   iendswith: case insensive contained content
    -   (see more lookups at https://docs.djangoproject.com/en/3.0/ref/models/querysets/)

'''
from django.db import models
from django.db.models import Q # formatting query conditions to DB-readible syntax. concatenate with | (or) and & (and)

class IManager(models.Manager):
    def IbyConditions(self, parameter1, parameter2):
        querySet = models.query.QuerySet(model=self.model, using=self._db)
        conditions = (
            Q(modelattr1__icontains=parameter1) | 
            Q(modelattr2__icontains=parameter2) &
            Q(modelattr3__icontains=parameter2)
        )
        return querySet.filter(conditions).distinct()