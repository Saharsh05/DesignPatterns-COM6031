from abc import ABC, abstractmethod


class FileSystemNode(ABC):
    """Base interface for file system nodes.

    Both concrete files and decorator wrappers implement this.
    """

    @abstractmethod
    def size(self) -> int: ...

    @abstractmethod
    def describe(self) -> str: ...


class File(FileSystemNode):
    """A simple file node with a fixed size."""

    def __init__(self, name: str, size_bytes: int) -> None:
        self.name = name
        self._size = size_bytes

    def size(self) -> int:
        return self._size

    def describe(self) -> str:
        return self.name


class NodeDecorator(FileSystemNode):
    """Base decorator that forwards calls to the wrapped node."""

    def __init__(self, wrapped: FileSystemNode) -> None:
        self._wrapped = wrapped

    def size(self) -> int:
        return self._wrapped.size()

    def describe(self) -> str:
        return self._wrapped.describe()


class Compressed(NodeDecorator):
    """Decorator that compresses a node, reducing its reported size."""

    def __init__(self, wrapped: FileSystemNode, ratio: float = 0.4) -> None:
        super().__init__(wrapped)
        self._ratio = ratio

    def size(self) -> int:
        return int(self._wrapped.size() * self._ratio)

    def describe(self) -> str:
        return f"compressed({self._wrapped.describe()})"


class Encrypted(NodeDecorator):
    """Decorator that adds encryption overhead."""

    def size(self) -> int:
        return self._wrapped.size() + 16

    def describe(self) -> str:
        return f"encrypted({self._wrapped.describe()})"


class ReadOnly(NodeDecorator):
    """Decorator that marks a node as read-only."""

    def describe(self) -> str:
        return f"read-only({self._wrapped.describe()})"


class Versioned(NodeDecorator):
    """Decorator that multiplies stored size by version count."""

    def __init__(self, wrapped: FileSystemNode, versions: int = 3) -> None:
        super().__init__(wrapped)
        self._versions = versions

    def size(self) -> int:
        return self._wrapped.size() * self._versions

    def describe(self) -> str:
        return f"versioned x{self._versions}({self._wrapped.describe()})"


def show(node: FileSystemNode) -> None:
    print(f"  {node.describe():<55} -> {node.size():>6} B")


def main() -> None:
    base = File("backup.tar", 1000)
    print("Single component")
    show(base)

    print("\nDecorators stacked dynamically, in different orders")
    show(Compressed(base))
    show(Encrypted(Compressed(base)))
    show(ReadOnly(Encrypted(Compressed(base))))
    show(Versioned(Compressed(base), versions=5))


if __name__ == "__main__":
    main()
