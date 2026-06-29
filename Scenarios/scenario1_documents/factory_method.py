"""Scenario 1 - Candidate 1: FACTORY METHOD  (CHOSEN)

Intent (GoF): define an interface for creating an object, but let subclasses
decide which class to instantiate. Factory Method lets a class defer
instantiation to its subclasses.

Participants:
  * Product          -> Document          (interface common to all documents)
  * ConcreteProduct  -> PdfDocument, WordDocument, MarkdownDocument, HtmlDocument
  * Creator          -> DocumentExporter  (declares the factory method and holds
                        the real export() business logic)
  * ConcreteCreator  -> PdfExporter, WordExporter, MarkdownExporter, HtmlExporter
"""

from abc import ABC, abstractmethod


class Document(ABC):
    """Abstract product for a specific document format."""

    #: File extension associated with this document type.
    extension: str = ""

    @abstractmethod
    def render(self, content: str) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{type(self).__name__}(extension={self.extension!r})"


class PdfDocument(Document):


    extension = ".pdf"

    def render(self, content: str) -> str:
        return f"%PDF-1.7\n{content}\n%%EOF"


class WordDocument(Document):


    extension = ".docx"

    def render(self, content: str) -> str:
        return f"[Word/OOXML] {content}"


class MarkdownDocument(Document):


    extension = ".md"

    def render(self, content: str) -> str:
        return f"# Document\n\n{content}"


class HtmlDocument(Document):


    extension = ".html"

    def render(self, content: str) -> str:
        return f"<!doctype html><html><body><p>{content}</p></body></html>"


class DocumentExporter(ABC):
    """Abstract creator defining a factory method for document creation."""

    @abstractmethod
    def create_document(self) -> Document:
        raise NotImplementedError

    def export(self, content: str) -> str:
        if not content or not content.strip():
            raise ValueError("content must be a non-empty string")

        # Delegate document creation to the concrete subclass.
        document = self.create_document()
        return document.render(content)

    def export_filename(self, stem: str) -> str:
        # The concrete document determines the extension used in the filename.
        return f"{stem}{self.create_document().extension}"


class PdfExporter(DocumentExporter):


    def create_document(self) -> Document:
        return PdfDocument()


class WordExporter(DocumentExporter):


    def create_document(self) -> Document:
        return WordDocument()


class MarkdownExporter(DocumentExporter):


    def create_document(self) -> Document:
        return MarkdownDocument()


class HtmlExporter(DocumentExporter):
    """Concrete creator returning an HtmlDocument."""

    def create_document(self) -> Document:
        return HtmlDocument()


# The client is configured through a registry and only ever refers to the
# abstract DocumentExporter / Document types - never the concrete classes.
EXPORTERS: dict[str, type[DocumentExporter]] = {
    "pdf": PdfExporter,
    "word": WordExporter,
    "markdown": MarkdownExporter,
    "html": HtmlExporter,
}


def export_document(fmt: str, content: str) -> str:
    """Factory client entry point: instantiate the exporter from the registry."""

    try:
        exporter = EXPORTERS[fmt]()
    except KeyError:
        raise ValueError(f"unsupported format: {fmt!r}") from None
    return exporter.export(content)


def main() -> None:
    content = "Quarterly report body"

    print("== Exporting the same content in every registered format ==")
    for fmt in EXPORTERS:
        exporter = EXPORTERS[fmt]()
        print(f"--- {fmt} -> {exporter.export_filename('report')} ---")
        print(export_document(fmt, content))
        print()

    print("== The client only ever sees the abstract types ==")
    print("registered products:", [c().create_document() for c in EXPORTERS.values()])

    print("\n== Error handling for an unknown format ==")
    try:
        export_document("xml", content)
    except ValueError as exc:
        print("rejected:", exc)


if __name__ == "__main__":
    main()