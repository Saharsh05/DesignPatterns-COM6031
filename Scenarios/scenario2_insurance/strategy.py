"""Scenario 2 - Candidate 2: STRATEGY  (interchangeable reaction only)

Intent (GoF): define a family of algorithms, encapsulate each one, and make them
interchangeable; Strategy lets the algorithm vary independently of the clients
that use it.

Participants:
  * Strategy          -> ReactionStrategy (the react() interface)
  * ConcreteStrategy  -> PriceSensitive, Loyal, CorporateNegotiator, RiskAverse
  * Context           -> Entity (delegates its reaction to a strategy object)
"""
from abc import ABC, abstractmethod


class ReactionStrategy(ABC):
    """Strategy interface for reacting to premium changes."""

    @abstractmethod
    def react(self, name: str, old: float, new: float) -> str: ...


class PriceSensitive(ReactionStrategy):
    """Strategy for entities that compare relative price increases."""

    def react(self, name: str, old: float, new: float) -> str:
        if new > old * 1.10:
            return f"{name}: rise exceeds 10%, switching insurer"
        return f"{name}: rise acceptable, staying"


class Loyal(ReactionStrategy):
    """Strategy for entities that stay loyal regardless of premium changes."""

    def react(self, name: str, old: float, new: float) -> str:
        return f"{name}: remains with current insurer"


class CorporateNegotiator(ReactionStrategy):
    """Strategy for companies that negotiate when premiums rise too much."""

    def react(self, name: str, old: float, new: float) -> str:
        if new - old > 100:
            return f"{name}: triggering contract renegotiation"
        return f"{name}: absorbing the change for now"


class RiskAverse(ReactionStrategy):
    """Strategy for entities that act only when premiums decrease."""

    def react(self, name: str, old: float, new: float) -> str:
        if new < old:
            return f"{name}: premium fell, purchasing additional cover"
        return f"{name}: maintaining current cover"


class Entity:
    """Context object using a strategy to decide how to respond."""

    def __init__(self, name: str, strategy: ReactionStrategy) -> None:
        self.name = name
        self._strategy = strategy

    def set_strategy(self, strategy: ReactionStrategy) -> None:
        """Swap the entity's strategy at runtime."""
        self._strategy = strategy

    def respond(self, old: float, new: float) -> None:
        print("  " + self._strategy.react(self.name, old, new))

    def __repr__(self) -> str:
        return f"Entity({self.name!r}, {type(self._strategy).__name__})"


def broadcast(entities: list[Entity], old: float, new: float) -> None:
    """External helper to notify each entity about a premium change."""
    print(f"Premium {old:.0f} -> {new:.0f}:")
    for entity in entities:
        entity.respond(old, new)


def main() -> None:
    saharsh = Entity("Saharsh", PriceSensitive())
    acme = Entity("Acme Ltd", CorporateNegotiator())
    rita = Entity("Rita", RiskAverse())
    entities = [saharsh, acme, rita]

    print("Entities:", entities)
    print()
    broadcast(entities, 1000, 1200)

    print("\nSaharsh becomes loyal (strategy swapped at runtime):")
    saharsh.set_strategy(Loyal())
    broadcast(entities, 1000, 1200)

    print("\nA premium CUT (1000 -> 900):")
    broadcast(entities, 1000, 900)


if __name__ == "__main__":
    main()
