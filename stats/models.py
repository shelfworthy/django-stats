from datetime import datetime, timedelta

from django.db import models

class DataPointManager(models.Manager):
    def _filtered(self, key, time_delta=None, **kw):
        to_date = datetime.today().date()
        from_date = to_date-(time_delta or timedelta(days=30))
        
        return self.get_query_set().filter(key=key, date_added__range=(from_date, to_date), **kw)
    
    def total(self, key, time_delta=None, **kw):
        ''' Returns sum of values for given key.
            time_delta - optional datetime.timedelta instance will be substracted from today
            kwargs will be passed to filter function
            '''
        
        return self._filtered(key, time_delta, **kw).aggregate(models.Sum('value'))['value__sum'] or 0
            
    def list(self, key, time_delta=None, **kw):
        ''' Returns list of values, grouped by day
            example output:
                [{'date_added': datetime.date(1989, 2, 2), 'value__sum': 3}, {'date_added': datetime.date(2010, 5, 5), 'value__sum': 11}]
            '''
        
        # Author.objects.values('name').annotate(average_rating=Avg('book__rating'))
        values = self._filtered(key, time_delta, **kw).values('date_added').annotate(models.Sum('value'))
        
        return values

class DataPoint(models.Model):
    key = models.CharField(max_length=140, blank=False, db_index=True)
    value = models.SmallIntegerField(default=0)
    date_added = models.DateField(db_index=True)
    
    objects = DataPointManager()
    
    def save(self, *a, **kw):
        if not self.date_added:
            self.date_added = datetime.today().date()
        
        super(DataPoint, self).save(*a, **kw)
