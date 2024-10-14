
from .error import InputError

class GenericData:
    """Generic data, including a unique idientifier.
    All main data types in the project inherit from this,
    including Message, AbstractChannel, User,
    Notification, etc
    """
    def __init__(self) -> None:
        """Create a generic data type
        """
        from . import identifier
        self._id = identifier.get_new_identifier()
    
    def __eq__(self, o: object) -> bool:
        """Check equality of generic data types. Compares by ID.

        Args:
            o (object): object to compare, must be GenericData or inherited type

        Returns:
            bool: equality
        """
        if isinstance(o, GenericData): # pragma: no cover
            return self.get_id() == o.get_id()
        else: # pragma: no cover
            # We can't do comparisons for anything else
            return NotImplemented
    
    def get_id(self) -> int:
        """Return the object's unique identifier ID

        Returns:
            int: ID
        """
        return self._id
    
    def remove(self):
        """Remove the data from any required places (called when removed from
        the main database)
        """
        return NotImplemented

class GenericDataContainer:
    """Contains a set of generic data types. Implements functions for adding,
    removing and getting them by ID. Other getters must be implemented in
    derived classes.
    """
    _contained_type_str = "Generic Data"
    def __init__(self, contained_type) -> None:
        """Create a GenericDataContainer

        Args:
            contained_type (type): type of object to accept for container
            
        Raises:
            TypeError: contained_type isn't derived from GenericData
        """
        # Ensure we're creating using a type that is allowed
        if not issubclass(contained_type, GenericData): # pragma: no cover
            raise TypeError(description=f"contained_type ({contained_type}) must be "
                            "derived from type GenericData")
        
        self._contained_type = contained_type
        self._contained = dict()

    def __len__(self) -> int:
        """Return size of container

        Returns:
            int: size
        """
        return len(self._contained)

    def __iter__(self):
        """Generate an iterator for a generic data container

        Returns:
            GenericDataContainerIterator: iterator
        """
        return GenericDataContainerIterator(self)

    def add(self, new_member: GenericData) -> None:
        """Add new_member to the container

        Args:
            new_member (contained_type): member to add
        
        Raises:
            TypeError: object can't be added to container due to incompatible
                       type
        """
        # Ensure the object we're inserting is allowed
        if not isinstance(new_member, self._contained_type): # pragma: no cover
            raise TypeError(description=f"new_object ({type(new_member)}) must be of type "
                            f"{self._contained_type}")

        self._contained[new_member.get_id()] = new_member

    def remove(self, rem_id: int) -> None:
        """Remove a member using its ID. Also calls the member's remove() method

        Args:
            rem_id (int): id to remove
        """
        self._contained.pop(rem_id).remove()

    def get(self, get_id: int) -> GenericData:
        """Get an item using its ID

        Args:
            get_id (int): id of item to get

        Raises:
            InputError: item not found

        Returns:
            GenericData: requested item
        """
        try:
            return self._contained[get_id]
        except KeyError:
            raise InputError(description=f"{self._contained_type_str} with ID {get_id} not found") from None

class GenericDataContainerIterator:
    """Iterator for generic data types
    """
    def __init__(self, container: GenericDataContainer) -> None:
        """Create iterator

        Args:
            container (GenericDataContainer): container to iterate over
        """
        self._index = 0
        self._dict_iter = iter(container._contained.values())

    def __next__(self) -> GenericData:
        """Get next item in iteration
        """
        return self._dict_iter.__next__()
