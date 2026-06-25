from __future__ import annotations
from abc import ABC, abstractmethod


class Visitor(ABC):

    @abstractmethod
    def visit_file(self, file: "File") -> None: ...
    @abstractmethod
    def visit_directory(self, directory: "Directory") -> None: ...


class Node(ABC):

    @abstractmethod
    def accept(self, visitor: Visitor) -> None: ...


class File(Node):
    def __init__(self, name: str, size_bytes: int) -> None:
        self.name = name
        self.size_bytes = size_bytes

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_file(self)


class Directory(Node):
    def __init__(self, name: str) -> None:
        self.name = name
        self.children: list[Node] = []

    def add(self, node: Node) -> Directory:
        self.children.append(node)
        return self

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_directory(self)
        for child in self.children:
            child.accept(visitor)


class SizeVisitor(Visitor):

    def __init__(self) -> None:
        self.total = 0

    def visit_file(self, file: File) -> None:
        self.total += file.size_bytes

    def visit_directory(self, directory: Directory) -> None:
        pass


class FileCountVisitor(Visitor):

    def __init__(self) -> None:
        self.files = 0

    def visit_file(self, file: File) -> None:
        self.files += 1

    def visit_directory(self, directory: Directory) -> None:
        pass


class ListingVisitor(Visitor):

    def __init__(self) -> None:
        self.names: list[str] = []

    def visit_file(self, file: File) -> None:
        self.names.append(file.name)

    def visit_directory(self, directory: Directory) -> None:
        pass


class LargestFileVisitor(Visitor):

    def __init__(self) -> None:
        self.name = ""
        self.size = -1

    def visit_file(self, file: File) -> None:
        if file.size_bytes > self.size:
            self.name, self.size = file.name, file.size_bytes

    def visit_directory(self, directory: Directory) -> None:
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
