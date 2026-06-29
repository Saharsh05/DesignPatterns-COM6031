"""Scenario 3 - Candidate 3: VISITOR  (considered, not chosen)

Intent (GoF): represent an operation to be performed on the elements of an object
structure. Visitor lets you define a new operation without changing the classes
of the elements on which it operates.

Participants:
  * Visitor          -> Visitor (visit_file / visit_directory)
  * ConcreteVisitor  -> SizeVisitor, FileCountVisitor, ListingVisitor, LargestFileVisitor
  * Element          -> Node (accept())
  * ConcreteElement  -> File, Directory
"""

from __future__ import annotations
from abc import ABC, abstractmethod


class Visitor(ABC):
    """Visitor interface for operations over file system nodes."""

    @abstractmethod
    def visit_file(self, file: "File") -> None: ...

    @abstractmethod
    def visit_directory(self, directory: "Directory") -> None: ...


class Node(ABC):
    """Abstract element in the object structure."""

    @abstractmethod
    def accept(self, visitor: Visitor) -> None: ...


class File(Node):
    """Leaf element representing a file."""

    def __init__(self, name: str, size_bytes: int) -> None:
        self.name = name
        self.size_bytes = size_bytes

    def accept(self, visitor: Visitor) -> None:
        # A file accepts a visitor and delegates to visit_file.
        visitor.visit_file(self)


class Directory(Node):
    """Composite element holding child nodes."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.children: list[Node] = []

    def add(self, node: Node) -> Directory:
        self.children.append(node)
        return self

    def accept(self, visitor: Visitor) -> None:
        # Visit the directory itself, then recursively visit children.
        visitor.visit_directory(self)
        for child in self.children:
            child.accept(visitor)


class SizeVisitor(Visitor):
    """Visitor that sums the total size of all files."""

    def __init__(self) -> None:
        self.total = 0

    def visit_file(self, file: File) -> None:
        self.total += file.size_bytes

    def visit_directory(self, directory: Directory) -> None:
        # No size contribution from directories themselves.
        pass


class FileCountVisitor(Visitor):
    """Visitor that counts file nodes."""

    def __init__(self) -> None:
        self.files = 0

    def visit_file(self, file: File) -> None:
        self.files += 1

    def visit_directory(self, directory: Directory) -> None:
        # Directories are not counted as files.
        pass


class ListingVisitor(Visitor):
    """Visitor that collects file names."""

    def __init__(self) -> None:
        self.names: list[str] = []

    def visit_file(self, file: File) -> None:
        self.names.append(file.name)

    def visit_directory(self, directory: Directory) -> None:
        # Only visit files for listing.
        pass


class LargestFileVisitor(Visitor):
    """Visitor that finds the largest file."""

    def __init__(self) -> None:
        self.name = ""
        self.size = -1

    def visit_file(self, file: File) -> None:
        if file.size_bytes > self.size:
            self.name, self.size = file.name, file.size_bytes

    def visit_directory(self, directory: Directory) -> None:
        # Directory nodes do not affect the largest file calculation.
        pass


def main() -> None:
    root = Directory("project")
    root.add(File("a.txt", 200))
    sub = Directory("sub").add(File("b.txt", 350)).add(File("c.bin", 1200))
    root.add(sub)

    size, count = SizeVisitor(), FileCountVisitor()
    listing, largest = ListingVisitor(), LargestFileVisitor()
    for visitor in (size, count, listing, largest):
        root.accept(visitor)

    print(f"Total size  : {size.total} B")
    print(f"File count  : {count.files}")
    print(f"File names  : {listing.names}")
    print(f"Largest file: {largest.name} ({largest.size} B)")


if __name__ == "__main__":
    main()
