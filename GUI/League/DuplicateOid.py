class DuplicateOid(Exception):
    def __init__(self, oid):
        self.oid = oid
