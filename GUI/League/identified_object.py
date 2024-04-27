
class IdentifiedObject:
    """
    IdentifiedObject -- an abstract class...no instances of it will be created (file name: identified_object.py)

        oid [r/o prop] -- the object id for this object
        __init__(oid) -- initialization method that sets the oid property as specified by the argument
        __eq__(other) -- two   are equal if they have the same type and the same oid
        __hash__() -- return hash code based on object's oid

     """

    def __init__(self, oid) -> None:
        self._oid = oid

    @property
    def oid(self):
        return self._oid

    def __eq__(self, other):
        if self.__hash__() == other.__hash__() and type(self) is type(other):
            return True
        else:
            return False

    def __hash__(self):
        return hash(self._oid)
