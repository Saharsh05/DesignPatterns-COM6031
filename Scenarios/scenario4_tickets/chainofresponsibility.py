"""Scenario 4 - Candidate 1: CHAIN OF RESPONSIBILITY  (CHOSEN)

Intent (GoF): avoid coupling the sender of a request to its receiver by giving
more than one object a chance to handle the request. Chain the receivers and pass
the request along the chain until an object handles it.

Participants:
  * Handler         -> SupportHandler (holds the successor link + shared flow)
  * ConcreteHandler -> BotTriage, Level1Support, Level2Support, Level3Support
  * Client          -> submits every ticket to the first handler only
"""



from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Ticket:
    """A support ticket that flows through the handler chain."""

    subject: str
    difficulty: int
    vip: bool = False

    def __str__(self) -> str:
        tag = " [VIP]" if self.vip else ""
        return f"'{self.subject}' (difficulty {self.difficulty}){tag}"


class SupportHandler(ABC):
    """Abstract base for a chain of responsibility support handler."""

    def __init__(self) -> None:
        # Reference to the next handler in the chain.
        self._next: SupportHandler | None = None

    def set_next(self, handler: SupportHandler) -> SupportHandler:
        """Link this handler to the next handler and return the next handler."""
        self._next = handler
        return handler

    def handle(self, ticket: Ticket) -> None:
        """Attempt to handle the ticket or pass it to the next handler."""
        if self._can_handle(ticket):
            self._resolve(ticket)
        elif self._next is not None:
            print(f"   {type(self).__name__} escalates {ticket}")
            self._next.handle(ticket)
        else:
            print(f"   [unresolved] {ticket} exceeded every tier")

    @abstractmethod
    def _can_handle(self, ticket: Ticket) -> bool: ...

    @abstractmethod
    def _resolve(self, ticket: Ticket) -> None: ...


class BotTriage(SupportHandler):
    """First tier handler that auto-closes trivial non-VIP tickets."""

    def _can_handle(self, ticket: Ticket) -> bool:
        return ticket.difficulty == 0 and not ticket.vip

    def _resolve(self, ticket: Ticket) -> None:
        print(f"Bot auto-closed {ticket}")


class Level1Support(SupportHandler):
    """First human support tier for very easy, non-VIP tickets."""

    def _can_handle(self, ticket: Ticket) -> bool:
        return ticket.difficulty <= 1 and not ticket.vip

    def _resolve(self, ticket: Ticket) -> None:
        print(f"L1 resolved {ticket}")


class Level2Support(SupportHandler):
    """Second support tier for medium difficulty, non-VIP tickets."""

    def _can_handle(self, ticket: Ticket) -> bool:
        return ticket.difficulty == 2 and not ticket.vip

    def _resolve(self, ticket: Ticket) -> None:
        print(f"L2 resolved {ticket}")


class Level3Support(SupportHandler):
    """Highest support tier for hard issues or any VIP ticket."""

    def _can_handle(self, ticket: Ticket) -> bool:
        return ticket.difficulty >= 3 or ticket.vip

    def _resolve(self, ticket: Ticket) -> None:
        print(f"L3 resolved {ticket}")


def build_chain() -> SupportHandler:
    """Build the chain of responsibility and return the first handler."""
    first = BotTriage()
    first.set_next(Level1Support()).set_next(Level2Support()).set_next(Level3Support())
    return first


def main() -> None:
    """Create sample tickets and submit them to the chain."""
    chain = build_chain()
    tickets = [
        Ticket("FAQ lookup", 0),
        Ticket("password reset", 1),
        Ticket("billing discrepancy", 2),
        Ticket("data breach", 3),
        Ticket("minor query", 1, vip=True),
    ]

    for ticket in tickets:
        print(f"Submitting {ticket}:")
        chain.handle(ticket)
        print()


if __name__ == "__main__":
    main()
