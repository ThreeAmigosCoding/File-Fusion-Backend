class Album:
    def __init__(self, id, name, owner, deleted, parent):
        self.id = id
        self.name = name
        self.owner = owner
        self.deleted = deleted
        self.parent = parent

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "owner": self.owner,
            "deleted": self.deleted,
            "parent": self.parent
        }