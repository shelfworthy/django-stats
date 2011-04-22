from datetime import date

from stats.tasks import DataPointUpdate
from stats import cache

import keys as stat_keys

def get_stats(key, set='total', update=0, start_date=None, end_date=None):
    ''' This cache will store and return stats for a given key in multiple ways.
        Currently supported:
            total: the total count for this key for all time
        Needs support:
            a way to get a list for given time periods (maybe give two dates?)
            a way to get totals for a given time peroid
    '''
    if set == 'total':
        return cache.stat_total(key, update).get()

def update_stat(key, value, date=date.today()):
    key = key.lower()
    try:
        if int(value) != 0:
            DataPointUpdate.delay(key, value, date)
            return get_stats(key, update=value)
    except ValueError:
        # TODO Do we need an exception here?
        pass