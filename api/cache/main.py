from datetime import datetime
from enum import Enum

class EvictionStrategies(Enum):
    """A class to represent the list of eviction policies as Enum

    Possible values: OLDEST_FIRST, NEWEST_FIRST, REJECT
    Underlying values: 'OLDEST_FIRST', 'NEWEST_FIRST', 'REJECT'
    """
    OLDEST_FIRST = 'OLDEST_FIRST'
    NEWEST_FIRST = 'NEWEST_FIRST'
    REJECT = 'REJECT'

class CacheEntry:
    """A class used to represent a cache entry

    Attributes:  
        json_str: str
            the string represantion of the json object cached
        ttl: integer
            the time to live in seconds
        creation_time: float
            a timestamp representing the time of creation of the cache entry
        is_expired: bool
            an indicator if the item has expired or not

    Methods:
    """
    def __init__(self, json_str, ttl):
        self._json_str = json_str
        self._ttl = int(ttl)
        self._creation_time = datetime.utcnow().timestamp()

    @property
    def json_str(self):
        return self._json_str

    @property
    def ttl(self):
        return self._ttl

    @property
    def creation_time(self):
        return self._creation_time

    @property
    def is_expired(self):
        if self.ttl == 0:
            return False
        return datetime.utcnow().timestamp() > self.creation_time + self.ttl

class Cache:
    """A class used to represent the cache

    Attributes:
        max_slots: integer
            the max number of entries allowed in the cache
        default_ttl: integer 
            the default time to live in seconds

    Methods:
        get_entry(key):
            returns the value for key in the cache if it exists and not expired.
            Otherwise, it will return None
        set_entry(key, json_str, ttl=None):
            inserts the value for key in the cache if possible. It returns True if successful and False otherwise. It will work according to the eviction policy of the cache
        delete_entry(key):
            removes the entry for key from the cache. It returns True if successful and False otherwise
    """
    def __init__(
        self, 
        max_slots = 10000, 
        default_ttl = 3600, 
        eviction_strategy =  EvictionStrategies.REJECT
    ):
        """
        Parameters:
            max_slots : integer
                The max number of entries allowed in the cache. If a non positive
                number is provided the default value of 10,000 will be used
            default_ttl : integer
                The default time to live in seconds. If a non positive
                number is provided the default value of 3600 will be used
            eviction_strategy : EvictionStrategies
                The Eviction policy when cache is full. It takes values from
                enum EvictionStrategies = (OLDEST_FIRST, NEWEST_FIRST, REJECT) and
                it defaults to EvictionStrategies.REJECT  
        """
        self.max_slots = max_slots
        self.default_ttl = default_ttl
        self._eviction_strategy = self._set_eviction_strategy(eviction_strategy)
        
        # use a dictionary as a container for the cache
        self._container = {}

    @property
    def max_slots(self):
        return self._max_slots

    @max_slots.setter
    def max_slots(self, max_slots):
        self._max_slots = max_slots if max_slots > 0 else 10000

    @property
    def default_ttl(self):
        return self._default_ttl

    @default_ttl.setter
    def default_ttl(self, default_ttl):
        self._default_ttl = default_ttl if default_ttl > 0 else 3600

    def get_entry(self, key):
        """Returns the value for key in the cache if it exists and not expired.
        Otherwise, it will return None

        Parameters:
            key : str
                The cache key

        Returns:
            CacheEntry or None
                The cache entry associated with key or None
        """
        cached_entry = self._container.get(key, None)
        if cached_entry and not cached_entry.is_expired:
            return cached_entry
        return None

    def set_entry(self, key, json_str, ttl=None):
        """Inserts the value for key in the cache if possible. 
        It returns True if successful and False otherwise 
        
        If the key already exists, it will replace the old value.
        Otherwise, it will use a free slot if one exists. If the cache
        is full, the eviction strategy will kick in

        Parameters:
            key: str
                The cache key
            json_str: str
                The string representation of json object to be cached
            ttl: int, optional
                The time to live in seconds. The cache default will be
                use if this is not provided

        Returns:
            bool
                True if the entry is inserted and Flase otherwise 
        """
        
        ttl = ttl or self._default_ttl;
        new_cache_entry = CacheEntry(json_str, ttl)

        # If entry already exists, replace old value
        if key in self._container:
            self._container[key] = new_cache_entry
            return True
        # If a free slot exists, use it
        if len(self._container.keys()) < self._max_slots:
            self._container[key] = new_cache_entry
            return True
        
        # Otherwise, use eviction policy
        key_to_evict = self._eviction_strategy(self._container.items())
        if key_to_evict:
            del self._container[key_to_evict]
            self._container[key] = new_cache_entry
            return True
        return False

    def delete_entry(self, key):
        """Removes the entry for key from the cache. It returns True if successful and False
        the entry does not exist or expired

        Parameters:
            key : str
                The cache key

        Returns:
            bool
                True if the entry is deleted and Flase if the entry
                does not exist or expired
        """
        cached_entry = self._container.get(key, None)
        if not cached_entry:
            return False
        del self._container[key]
        return not cached_entry.is_expired

    # A private method to set eviction strategy
    def _set_eviction_strategy(self, eviction_strategy):
        if eviction_strategy == EvictionStrategies.OLDEST_FIRST:
            return oldest_first
        if eviction_strategy == EvictionStrategies.NEWEST_FIRST:
            return newest_first
        return reject

"""An implementation of reject strategy

It returns the key of the first expired entry it encounters or None
if no expired entry exists
"""
def reject(container):
    for key,entry in container:
        print(key, entry)
        if entry.is_expired:
            return key
    return None

"""An implementation of oldest_first strategy

It returns the key of the first expired entry it encounters or the key
of the oldest entry in the cache
"""
def oldest_first(container):
    oldest_key = None
    oldest_creation_time = datetime.utcnow().timestamp()
    for key,entry in container:
        if entry.is_expired:
            return key
        if entry.creation_time < oldest_creation_time:
            oldest_creation_time = entry.creation_time
            oldest_key = key
    return oldest_key

"""An implementation of newest_first strategy

It returns the key of the first expired entry it encounters or the key
of the newest entry in the cache
"""
def newest_first(container):
    newest_key = None
    newest_creation_time = 0.0
    for key,entry in container:
        if entry.is_expired:
            return key
        if entry.creation_time > newest_creation_time:
            newest_creation_time = entry.creation_time
            newest_key = key
    return newest_key