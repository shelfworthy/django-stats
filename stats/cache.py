import logging

from django.db.models import Sum

from stats.cache_wrapper import Cache
from stats.models import DataPoint

log = logging.getLogger('stats.cache')

def stat_total(key, update=0):
    def function():
        log.debug('getting total stat count for key %s (not cached)...' % key)
        return DataPoint.objects.total(key)
    
    # if there is an update, always update the global total
    cache = Cache('stat_global_total_%s' % key, function)
    cache.update_count(update)
    
    return cache

def stat_list(key, start_date=None, end_date=None):
    if not start_date and not end_date:
        use_range = False
    else:
        use_range = True
    
    # TODO not sure how to update list data in or out of the cache...
    pass