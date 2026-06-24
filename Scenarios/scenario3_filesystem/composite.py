from __future__ import annotations
from abc import ABC, abstractmethod


class FileSystemNode(ABC):

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def size(self) -> int:
        pass
    @abstractmethod
    def count_files(self) -> int:
        pass

    @abstractmethod
    def find(self, name: str) -> "FileSystemNode | None":
        pass

    @abstractmethod
    def display(self, indent: int = 0) -> None:
        """Print an indented tree view rooted at this node."""
        pass

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name!r}, {self.size()} B)"


class File(FileSystemNode):

    def __init__(self, name: str, size_bytes: int) -> None:
        super().__init__(name)
        if size_bytes < 0:
            raise ValueError("size cannot be negative")
        self._size = size_bytes

    def size(self) -> int:
        return self._size

    def count_files(self) -> int:
        return 1

    def find(self, name: str) -> FileSystemNode | None:
        return self if self.name == name else None

    def display(self, indent: int = 0) -> None:
        print(" " * indent + f"- {self.name} ({self._size} B)")


class Directory(FileSystemNode):

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._children: list[FileSystemNode] = []

    def add(self, node: FileSystemNode) -> Directory:
        self._children.append(node)
        return self                               # fluent for easy building

    def remove(self, node: FileSystemNode) -> None:
        self._children.remove(node)

    def size(self) -> int:
        return sum(child.size() for child in self._children)       # recursion

    def count_files(self) -> int:
        return sum(child.count_files() for child in self._children)

    def find(self, name: str) -> FileSystemNode | None:
        if self.name == name:
            return self
        for child in self._children:
            hit = child.find(name)
            if hit is not None:
                return hit
        return None

    def display(self, indent: int = 0) -> None:
        print(" " * indent + f"+ {self.name}/ ({self.size()} B)")
        for child in self._children:
            child.display(indent + 2)


def report(node: FileSystemNode) -> None:
    """Client code that treats a leaf and a whole tree identically."""
    print(f"  {node.name}: {node.size()} B, {node.count_files()} file(s)")


def main() -> None:
    root = Directory("project")
    root.add(File("readme.md", 120))

    src = Directory("src")
    src.add(File("main.py", 540)).add(File("utils.py", 310))
    tests = Directory("tests")
    tests.add(File("test_main.py", 410))
    src.add(tests)
    root.add(src)

    print("Tree")
    root.display()

    print("\nUniform treatment of leaf vs composite")
    report(root.find("main.py"))     # a leaf
    report(root)                     # the whole tree

    print("\nRemoving a sub-tree updates totals automatically")
    root.remove(src)
    report(root)


if __name__ == "__main__":
    main()
