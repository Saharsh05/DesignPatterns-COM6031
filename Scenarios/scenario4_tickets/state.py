from __future__ import annotations
from abc import ABC, abstractmethod


class TicketState(ABC):

    name: str = "state"

    def assign(self, ticket: "Ticket") -> None:
        self._invalid("assign")

    def start(self, ticket: "Ticket") -> None:
        self._invalid("start")

    def resolve(self, ticket: "Ticket") -> None:
        self._invalid("resolve")

    def reopen(self, ticket: "Ticket") -> None:
        self._invalid("reopen")

    def _invalid(self, action: str) -> None:
        print(f"   ! cannot '{action}' while {self.name}")


class New(TicketState):
    name = "New"

    def assign(self, ticket: Ticket) -> None:
        ticket.transition(Assigned())


class Assigned(TicketState):
    name = "Assigned"

    def start(self, ticket: Ticket) -> None:
        ticket.transition(InProgress())


class InProgress(TicketState):
    name = "InProgress"

    def resolve(self, ticket: Ticket) -> None:
        ticket.transition(Resolved())


class Resolved(TicketState):
    name = "Resolved"

    def reopen(self, ticket: Ticket) -> None:
        ticket.transition(Reopened())


class Reopened(TicketState):
    name = "Reopened"

    def start(self, ticket: Ticket) -> None:
        ticket.transition(InProgress())


class Ticket:

    def __init__(self, subject: str) -> None:
        self.subject = subject
        self.state: TicketState = New()

    def transition(self, new_state: TicketState) -> None:
        print(f"'{self.subject}': {self.state.name} -> {new_state.name}")
        self.state = new_state

    def assign(self) -> None: self.state.assign(self)
    def start(self) -> None: self.state.start(self)
    def resolve(self) -> None: self.state.resolve(self)
    def reopen(self) -> None: self.state.reopen(self)


def main() -> None:
    ticket = Ticket("printer offline")
    print(" Happy path ")
    ticket.assign()
    ticket.start()
    ticket.resolve()

    print("\n Illegal action is rejected by the current state ")
    ticket.assign()       

    print("\n Reopen then resolve again ")
    ticket.reopen()
    ticket.start()
    ticket.resolve()


if __name__ == "__main__":
    main()
