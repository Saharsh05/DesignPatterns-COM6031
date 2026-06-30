# COM6031 — Design Patterns (CW1)

A comparative evaluation and Python implementation of Gang-of-Four design patterns across four scenarios.

The guiding premise of this project is that **no design pattern is a single, context-free "best" answer** to a scenario: appropriateness is relative to the precise requirement. Each scenario therefore weighs several candidate patterns, implements the strongest of them in full, and proposes the one that best fits the requirement as written while showing where the alternatives would be the right choice instead.

---

## Submission details

| | |
|---|---|
| **Student** | _[ Your name ]_ |
| **Student ID** | _[ Your student ID ]_ |
| **Module** | COM6031 Design Patterns |
| **Module leader** | Shaad Kajee |
| **Assignment** | CW1 — Design Patterns Coursework |
| **Language** | Python 3 |

---

## Scenarios and patterns

| # | Scenario | Family focus | Patterns implemented | Proposed design |
|---|----------|--------------|----------------------|-----------------|
| 1 | Document Creation System | Creational | Factory Method, Abstract Factory, Builder | **Factory Method** |
| 2 | Insurance Premium Simulation | Behavioural | Observer, Strategy, Mediator | **Observer + Strategy** (combined) |
| 3 | File System | Structural | Composite, Decorator, Visitor | **Composite** |
| 4 | Support Ticket System | Behavioural | Chain of Responsibility, State | **Chain of Responsibility** |

Each scenario also discusses further patterns that were *considered but not implemented*, with reasons (e.g. Template Method and Singleton for Scenario 1; Iterator and Proxy for Scenario 3). Full reasoning is in the report.

---

## Repository structure

```
.
├── README.md
├── COM6031_Design_Patterns_Report.docx     # the written report
├── COM6031_Design_Patterns.ipynb           # all implementations in one runnable notebook
└── code/
    ├── scenario1_documents/
    │   ├── factory_method.py
    │   ├── abstract_factory.py
    │   └── builder.py
    ├── scenario2_insurance/
    │   ├── observer.py
    │   ├── strategy.py
    │   ├── mediator.py
    │   └── observer_strategy_combined.py    # the proposed design
    ├── scenario3_filesystem/
    │   ├── composite.py
    │   ├── decorator.py
    │   └── visitor.py
    └── scenario4_tickets/
        ├── chain_of_responsibility.py
        └── state.py
        └── command.py
```



---

## Requirements

- **Python 3.10 or newer**
- **No external dependencies** — every script uses only the Python standard library.
- To run the notebook you will also need **Jupyter** (`pip install notebook` or open it in VS Code).

---

## Running the code

Every implementation is a self-contained script with its own `main()` and a `demonstration` you can run directly:

```bash
# from the repository root
python code/scenario1_documents/factory_method.py
python code/scenario2_insurance/observer_strategy_combined.py
python code/scenario3_filesystem/composite.py
python code/scenario4_tickets/chain_of_responsibility.py
```

Each script prints a short demonstration of the pattern in action (the same output shown in the report's *Demonstration and Evaluation* sections).


---

## What each scenario demonstrates

- **Scenario 1 — Document Creation.** A client creates PDF, Word and Markdown documents through one interface while the concrete type is chosen for it. Factory Method decouples the export workflow from the concrete document classes, so a new format is added without touching existing client code (Open/Closed Principle).
- **Scenario 2 — Insurance Premium.** A policy broadcasts premium changes (Observer) and each entity reacts through an interchangeable, runtime-swappable algorithm (Strategy). The two patterns separate *notification* from *business behaviour* so each can evolve independently.
- **Scenario 3 — File System.** Files and directories share one `FileSystemNode` interface, so `size()` and similar operations behave identically on a single file or a whole tree (Composite), with the recursion fully transparent to the client.
- **Scenario 4 — Support Ticket System.** Tickets pass along a chain of escalating handlers; each tier resolves a ticket or forwards it, so the sender never needs to know which tier resolves it (Chain of Responsibility), with an explicit fallback at the end of the chain.

---

## Report and appendices

The written report (`COM6031_Design_Patterns_Report.docx`) contains, for each scenario: a scenario overview, the patterns considered, the selected patterns (with UML class diagrams), and a demonstration and evaluation grounded in real-world systems — followed by a cross-scenario comparative analysis and a conclusion. The full source code is also reproduced in the report appendices.

## References

All sources are cited in Harvard style in the report's reference list (Gamma et al.'s *Design Patterns*, Bloch's *Effective Java*, Freeman and Robson's *Head First Design Patterns*, the official Java documentation, and Refactoring.Guru, among others).

## Academic integrity

This repository is submitted as individual coursework for COM6031. The design and implementations are my own work; external sources that informed the analysis are acknowledged in the report's references.