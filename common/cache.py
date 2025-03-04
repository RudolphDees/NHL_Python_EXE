import pickle
import os

class Cache:
    def __init__(self, filename: str):
        self.filename = "cache/" + filename
        self.cache = self.load_cache()

    def load_cache(self):
        """Loads the cache from the file if it exists."""
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as file:
                return pickle.load(file)
        else:
            return {}

    def save_cache(self):
        """Saves the cache to a file."""
        with open(self.filename, 'wb') as file:
            pickle.dump(self.cache, file)

    def get(self, key):
        """Gets a value from the cache."""
        return self.cache.get(key)

    def set(self, key, value):
        """Sets a value in the cache."""
        self.cache[key] = value
        self.save_cache()

    def delete(self, key):
        """Deletes a key-value pair from the cache."""
        if key in self.cache:
            del self.cache[key]
            self.save_cache()

    def clear(self):
        """Clears the entire cache."""
        self.cache.clear()
        self.save_cache()
