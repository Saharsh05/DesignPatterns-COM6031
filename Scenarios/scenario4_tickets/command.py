from __future__ import annotations
from abc import ABC, abstractmethod


class Command(ABC):

    @abstractmethod
    def execute(self) -> None: ...
    @abstractmethod
    def undo(self) -> None: ...

    def label(self) -> str:
        return type(self).__name__


class ResolveTicket(Command):
    def __init__(self, subject: str) -> None:
        self.subject = subject

    def execute(self) -> None:
        print(f"Resolving '{self.subject}'")

    def undo(self) -> None:
        print(f"Re-opening '{self.subject}'")


class EscalateTicket(Command):
    def __init__(self, subject: str) -> None:
        self.subject = subject

    def execute(self) -> None:
        print(f"Escalating '{self.subject}'")

    def undo(self) -> None:
        print(f"De-escalating '{self.subject}'")


class ReassignTicket(Command):
    def __init__(self, subject: str, agent: str) -> None:
        self.subject = subject
        self.agent = agent

    def execute(self) -> None:
        print(f"Reassigning '{self.subject}' to {self.agent}")

    def undo(self) -> None:
        print(f"Reverting assignment of '{self.subject}'")


class TicketQueue:

    def __init__(self) -> None:
        self._pending: list[Command] = []
        self._history: list[Command] = []
        self._undone: list[Command] = []

    def submit(self, command: Command) -> None:
        self._pending.append(command)

    def process_all(self) -> None:
        while self._pending:
            command = self._pending.pop(0)
            command.execute()
            self._history.append(command)
        self._undone.clear()

    def undo_last(self) -> None:
        if self._history:
            command = self._history.pop()
            command.undo()
            self._undone.append(command)

    def redo_last(self) -> None:
        if self._undone:
            command = self._undone.pop()
            command.execute()
            self._history.append(command)

    def log(self) -> list[str]:
        return [c.label() for c in self._history]


def main() -> None:
    queue = TicketQueue()
    queue.submit(ResolveTicket("password reset"))
    queue.submit(ReassignTicket("data breach", "security-team"))
    queue.submit(EscalateTicket("data breach"))

    print("Processing queued commands")
    queue.process_all()
    print("history:", queue.log())

    print("\nUndo the most recent action")
    queue.undo_last()
    print("history:", queue.log())

    print("\nRedo it")
    queue.redo_last()
    print("history:", queue.log())


if __name__ == "__main__":
    main()
