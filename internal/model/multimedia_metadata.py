import json


class MultimediaMetadata:
    def __init__(self, id, name, type, size_in_kb, created_at, last_changed, username, description):
        self.id = id
        self.name = name
        self.type = type
        self.size_in_kb = size_in_kb
        self.created_at = created_at
        self.last_changed = last_changed
        self.username = username
        self.description = description

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return MultimediaMetadata(**data)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "size_in_kb": self.size_in_kb,
            "created_at": self.created_at,
            "last_changed": self.last_changed,
            "username": self.username,
            "description": self.description
        }
