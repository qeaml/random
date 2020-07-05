import json
import os

__all__ = ['load', 'DBError']

def load(filename, auto_commit=True):
    """
        Loads and returns a database.
        
        Parameters:
            filename: `str` - The filename of the database to load.
            auto_commit: `bool` - Whether to enable auto-commiting. (def.: True)
    """
    return Database(filename, auto_commit)

class DBError(Exception):
    pass

class DBObject:
    """
        A JSON object stored witin the database. Supports subscription.
    """
    def __init__(self, db, key, value):
        self._db = db
        self._key = key
        self.value = value
        
    def _update(self):
        self._db._update(self._key, self.value)

    def get(self, key):
        v = self.value[key]
        if isinstance(v, dict):
            return DBObject(self._db, f'{self._key}.{key}', v)
        else:
            return v

    def set(self, key, value):
        self.value[key] = value
        self._update()
        
    def delete(self, key):
        del self.value[key]
        self._update()

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)
        
    def __delitem__(self, key):
        self.delete(key)

    def __str__(self):
        return f'<object "{self.key}" in {self._db}>'
        
    def __dict__(self):
        return self.value
        
    def __len__(self):
        return len(self.value)

class Database:
    """
        A loaded database. Supports subscription. `dict`s contained within the
        database are returned as `DBObject` to allow for synchronised reading
        and writing through subscription.
    """
    def __init__(self, filename, auto_commit):
        self.filename = filename
        self.auto_commit = auto_commit
        
        self._raw = None
        self._dict = None
        
        self._load()

    def _load(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'wb') as f:
                f.write(b'{}')
        with open(self.filename, 'rb') as f:
            self._raw = f.read()
        try:
            self._dict = json.loads(self._raw)
        except json.decoder.JSONDecodeError as e:
            raise DBError(
                'Could not load database file!'
            ) from e

    def _update(self, key, value):
        keys = key.split('.')
        keys.reverse()
        d = self._dict.copy()
        f = d
        while len(keys) > 1:
            f = f[keys.pop()]
        f[keys[-1]] = value
        self._dict = d
        if self.auto_commit:
            self.commit()

    def commit(self):
        try:
            self._raw = bytes(json.dumps(self._dict), 'utf-8')
        except json.encoder.JSONEncodeError:
            return 
        with open(self.filename, 'wb') as f:
            f.write(self._raw)

    def get(self, key):
        try:
            v = self._dict[key]
        except KeyError:
            raise DBError(f'Could not find root key "{key}".')
        if isinstance(v, dict):
            return DBObject(self, key, v)
        else:
            return v

    def set(self, key, value):
        self._dict.update({key: value})
        if self.auto_commit:
            self.commit()

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        return self.set(key, value)
    
    def __str__(self):
        return f'<database in "{self.filename}">'