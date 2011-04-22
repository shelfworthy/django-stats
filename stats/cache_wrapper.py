from django.core.cache import cache

class Cache(object):
    """
    Simple cache proxy object, provides get/set/delete features for single cached key value pair.
    TODO: Need to create child class with locks implementation for avoid memcache dog pile problem
    """
    
    def __init__(self, key, function=None, *args, **kwargs):
        self.key = str(key)
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.expire = None
    
    def get(self):
        """
        fetch data from cache, and replace it by real data if cache is empty
        """
        
        cached_result = cache.get(self.key)
        
        if cached_result is None and self.function:
            result = self.function(*self.args, **self.kwargs)
            self.set(result, self.expire)
            return result
        
        return cached_result
    
    def delete(self):
        return cache.delete(self.key)
    
    def set(self, *args, **kwargs):
        return cache.set(self.key, *args, **kwargs)
    
    def add(self, *args, **kwargs):
        return cache.add(self.key, *args, **kwargs)
    
    def _incr(self, value=1):
        try:
            current_value = int(self.get())
            current_value += value
            self.set(current_value)
            return self.get()
        except ValueError:
            # TODO handle exception here?
            pass
    
    def _decr(self, value=1):
        try:
            current_value = int(self.get())
            current_value -= value
            self.set(current_value)
            return self.get()
        except ValueError:
            # TODO handle exception here?
            pass
    
    def update_count(self, value):
        if value > 0:
            return self._incr(value)
        elif value < 0:
            return self._decr(abs(value))
        return self