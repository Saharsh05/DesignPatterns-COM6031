from abc import ABC, abstractmethod


class Document(ABC):
    @abstractmethod
    def render(self, content: str) -> str: ...


class Stylesheet(ABC):
    @abstractmethod
    def describe(self) -> str: ...


class Metadata(ABC):
    @abstractmethod
    def mime_type(self) -> str: ...



class PdfDocument(Document):
    def render(self, content: str) -> str:
        return f"%PDF {content}"


class PdfStylesheet(Stylesheet):
    def describe(self) -> str:
        return "print-optimised CMYK styles"


class PdfMetadata(Metadata):
    def mime_type(self) -> str:
        return "application/pdf"



class WebDocument(Document):
    def render(self, content: str) -> str:
        return f"<html><body>{content}</body></html>"


class WebStylesheet(Stylesheet):
    def describe(self) -> str:
        return "responsive RGB CSS styles"


class WebMetadata(Metadata):
    def mime_type(self) -> str:
        return "text/html"



class MobileDocument(Document):
    def render(self, content: str) -> str:
        return f"{{\"screen\": \"{content}\"}}"


class MobileStylesheet(Stylesheet):
    def describe(self) -> str:
        return "compact high-contrast mobile styles"


class MobileMetadata(Metadata):
    def mime_type(self) -> str:
        return "application/vnd.app+json"


class DocumentSuiteFactory(ABC):
    """Abstract Factory: creates a whole matched family of products."""

    @abstractmethod
    def create_document(self) -> Document: ...
    @abstractmethod
    def create_stylesheet(self) -> Stylesheet: ...
    @abstractmethod
    def create_metadata(self) -> Metadata: ...


class PdfSuiteFactory(DocumentSuiteFactory):
    """Concrete Factory producing the consistent PDF family."""

    def create_document(self) -> Document:
        return PdfDocument()

    def create_stylesheet(self) -> Stylesheet:
        return PdfStylesheet()

    def create_metadata(self) -> Metadata:
        return PdfMetadata()


class WebSuiteFactory(DocumentSuiteFactory):
    """Concrete Factory producing the consistent Web family."""

    def create_document(self) -> Document:
        return WebDocument()

    def create_stylesheet(self) -> Stylesheet:
        return WebStylesheet()

    def create_metadata(self) -> Metadata:
        return WebMetadata()


class MobileSuiteFactory(DocumentSuiteFactory):
    """Concrete Factory producing the consistent Mobile family."""

    def create_document(self) -> Document:
        return MobileDocument()

    def create_stylesheet(self) -> Stylesheet:
        return MobileStylesheet()

    def create_metadata(self) -> Metadata:
        return MobileMetadata()


def build_suite(factory: DocumentSuiteFactory, content: str) -> str:
    """Use a factory to build a complete, internally consistent document set."""
    document = factory.create_document()
    stylesheet = factory.create_stylesheet()
    metadata = factory.create_metadata()
    return (f"{document.render(content)}\n"
            f"      styles: {stylesheet.describe()}\n"
            f"      type  : {metadata.mime_type()}")


FACTORIES: dict[str, DocumentSuiteFactory] = {
    "pdf": PdfSuiteFactory(),
    "web": WebSuiteFactory(),
    "mobile": MobileSuiteFactory(),
}


def main() -> None:
    print("== Each factory yields a self-consistent family ==")
    for name, factory in FACTORIES.items():
        print(f"[{name}] {type(factory).__name__}")
        print("  " + build_suite(factory, "Annual review"))
        print()

    print("== Products from one family are guaranteed compatible ==")
    web = FACTORIES["web"]
    print("document + metadata agree on type:",
          isinstance(web.create_document(), WebDocument),
          "/", web.create_metadata().mime_type())


if __name__ == "__main__":
    main()