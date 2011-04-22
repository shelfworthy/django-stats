from celery.task import Task
from celery.registry import tasks

from stats.models import DataPoint

class DataPointUpdate(Task):
    def run(self, key, value, date, **kwargs):
        point, created = DataPoint.objects.get_or_create(key=key, date_added=date)
        if value > 0:
            point.value += value
        elif value < 0:
            point.value -= abs(value)
        point.save()
tasks.register(DataPointUpdate)