from datetime import timedelta, datetime

from django.test import TestCase
from django.db import models

from stats.models import DataPoint

class Test(TestCase):
    def setUp(self):
        for x in xrange(1, 10):
            DataPoint.objects.create(key='ctu', value=1)
        
        DataPoint.objects.create(key='ctu', value=2)
        
    def _tearDown(self):
        DataPoint.objects.delete()

    def test_total(self):
        self.assertEquals(DataPoint.objects.total(key='asd'), 0)
        self.assertEquals(DataPoint.objects.total(key='ctu'), 11)
        
        #kwargs
        self.assertEquals(DataPoint.objects.total(key='ctu', value=2), 2)
        
        #custom timedelta
        self.assertEquals(DataPoint.objects.total('ctu', time_delta=timedelta(days=100)), 11)
        
    def test_list(self):
        DataPoint.objects.create(key='ctu', value=3, date_added=datetime(1989, 2, 2))
        
        l = DataPoint.objects.list('ctu', time_delta=timedelta(days=10000))