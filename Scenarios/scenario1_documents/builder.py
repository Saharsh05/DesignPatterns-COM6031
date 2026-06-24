from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Section:
    

    heading: str
    body: str

    def __repr__(self) -> str:
        return f"Section({self.heading!r})"


@dataclass
class Document:


    title: str = ""
    author: str = ""
    show_toc: bool = False
    sections: list[Section] = field(default_factory=list)
    footer: str = ""

    def render(self) -> str:
        lines = [self.title, f"by {self.author}", ""]
        if self.show_toc:
            lines.append("Contents:")
            lines.extend(f"  {i}. {s.heading}" for i, s in enumerate(self.sections, 1))
            lines.append("")
        for section in self.sections:
            lines.append(f"## {section.heading}")
            lines.append(f"   {section.body}")
        lines.append("")
        lines.append(f"[{self.footer}]")
        return "\n".join(lines)


class DocumentBuilder:


    def __init__(self) -> None:
        self._doc = Document()

    def set_title(self, title: str) -> DocumentBuilder:
        self._doc.title = title
        return self

    def set_author(self, author: str) -> DocumentBuilder:
        self._doc.author = author
        return self

    def with_table_of_contents(self) -> DocumentBuilder:
        self._doc.show_toc = True
        return self

    def add_section(self, heading: str, body: str) -> DocumentBuilder:
        self._doc.sections.append(Section(heading, body))
        return self

    def set_footer(self, footer: str) -> DocumentBuilder:
        self._doc.footer = footer
        return self

    def build(self) -> Document:
        if not self._doc.title:
            raise ValueError("a document requires a title")
        if not self._doc.sections:
            raise ValueError("a document requires at least one section")
        return self._doc


class ReportDirector:


    @staticmethod
    def standard_report(builder: DocumentBuilder) -> Document:
        return (builder
                .set_title("Project Report")
                .set_author("Engineering")
                .with_table_of_contents()
                .add_section("Introduction", "Background and aims.")
                .add_section("Findings", "What the analysis showed.")
                .add_section("Conclusion", "Recommended next steps.")
                .set_footer("Confidential")
                .build())

    @staticmethod
    def memo(builder: DocumentBuilder) -> Document:
        return (builder
                .set_title("One-page Memo")
                .set_author("Ops")
                .add_section("Summary", "A single short section only.")
                .set_footer("Internal")
                .build())


def main() -> None:
    print("== Full report built via the director's recipe ==")
    print(ReportDirector.standard_report(DocumentBuilder()).render())

    print("\n== Bespoke document assembled step by step ==")
    custom = (DocumentBuilder()
              .set_title("Release Notes")
              .set_author("QA")
              .add_section("Fixed", "Three defects resolved.")
              .add_section("Known issues", "One minor display glitch.")
              .set_footer("v2.1")
              .build())
    print(custom.render())

    print("\n== Validation rejects an incomplete product ==")
    try:
        DocumentBuilder().set_author("nobody").build()
    except ValueError as exc:
        print("rejected:", exc)


if __name__ == "__main__":
    main()
