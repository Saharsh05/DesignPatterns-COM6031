from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Ticket:

    subject: str
    difficulty: int          
    vip: bool = False

    def __str__(self) -> str:
        tag = " [VIP]" if self.vip else ""
        return f"'{self.subject}' (difficulty {self.difficulty}){tag}"


class SupportHandler(ABC):

    def __init__(self) -> None:
        self._next: SupportHandler | None = None

    def set_next(self, handler: SupportHandler) -> SupportHandler:
        self._next = handler
        return handler

    def handle(self, ticket: Ticket) -> None:
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

    def _can_handle(self, ticket: Ticket) -> bool:
        return ticket.difficulty == 0 and not ticket.vip

    def _resolve(self, ticket: Ticket) -> None:
        print(f"Bot auto-closed {ticket}")


class Level1Support(SupportHandler):
    def _can_handle(self, ticket: Ticket) -> bool:
        return ticket.difficulty <= 1 and not ticket.vip

    def _resolve(self, ticket: Ticket) -> None:
        print(f"L1 resolved {ticket}")


class Level2Support(SupportHandler):
    def _can_handle(self, ticket: Ticket) -> bool:
        return ticket.difficulty == 2 and not ticket.vip

    def _resolve(self, ticket: Ticket) -> None:
        print(f"L2 resolved {ticket}")


class Level3Support(SupportHandler):

    def _can_handle(self, ticket: Ticket) -> bool:
        return ticket.difficulty >= 3 or ticket.vip

    def _resolve(self, ticket: Ticket) -> None:
        print(f"L3 resolved {ticket}")


def build_chain() -> SupportHandler:
    first = BotTriage()
    first.set_next(Level1Support()).set_next(Level2Support()).set_next(Level3Support())
    return first


def main() -> None:
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
