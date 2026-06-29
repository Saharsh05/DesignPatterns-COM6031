"""Scenario 4 - Candidate 3: COMMAND  (considered, not chosen)

Intent (GoF): encapsulate a request as an object, thereby letting you
parameterise clients with different requests, queue or log requests, and support
undoable operations.

Participants:
  * Command          -> Command (execute()/undo() interface)
  * ConcreteCommand  -> ResolveTicket, EscalateTicket, ReassignTicket
  * Invoker          -> TicketQueue (stores, runs, logs, and can undo/redo)
  * Receiver         -> the printed ticket actions
"""

from __future__ import annotations
from abc import ABC, abstractmethod


class Command(ABC):
    """Abstract command interface for ticket actions."""

    @abstractmethod
    def execute(self) -> None: ...

    @abstractmethod
    def undo(self) -> None: ...

    def label(self) -> str:
        """Return a human-friendly name for the command."""
        return type(self).__name__


class ResolveTicket(Command):
    """Concrete command to resolve a ticket."""

    def __init__(self, subject: str) -> None:
        self.subject = subject

    def execute(self) -> None:
        print(f"Resolving '{self.subject}'")

    def undo(self) -> None:
        print(f"Re-opening '{self.subject}'")


class EscalateTicket(Command):
    """Concrete command to escalate a ticket."""

    def __init__(self, subject: str) -> None:
        self.subject = subject

    def execute(self) -> None:
        print(f"Escalating '{self.subject}'")

    def undo(self) -> None:
        print(f"De-escalating '{self.subject}'")


class ReassignTicket(Command):
    """Concrete command to reassign a ticket to a different agent."""

    def __init__(self, subject: str, agent: str) -> None:
        self.subject = subject
        self.agent = agent

    def execute(self) -> None:
        print(f"Reassigning '{self.subject}' to {self.agent}")

    def undo(self) -> None:
        print(f"Reverting assignment of '{self.subject}'")


class TicketQueue:
    """Invoker-like class that queues commands and supports undo/redo."""

    def __init__(self) -> None:
        self._pending: list[Command] = []
        self._history: list[Command] = []
        self._undone: list[Command] = []

    def submit(self, command: Command) -> None:
        """Add a command to the pending queue."""
        self._pending.append(command)

    def process_all(self) -> None:
        """Execute every pending command and move it to history."""
        while self._pending:
            command = self._pending.pop(0)
            command.execute()
            self._history.append(command)

        # Clear redo history after new commands are processed.
        self._undone.clear()

    def undo_last(self) -> None:
        """Undo the most recently executed command."""
        if self._history:
            command = self._history.pop()
            command.undo()
            self._undone.append(command)

    def redo_last(self) -> None:
        """Redo the most recently undone command."""
        if self._undone:
            command = self._undone.pop()
            command.execute()
            self._history.append(command)

    def log(self) -> list[str]:
        """Return a list of executed commands for inspection."""
        return [c.label() for c in self._history]


def main() -> None:
    """Demonstrate queuing, processing, undo, and redo of ticket commands."""
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
