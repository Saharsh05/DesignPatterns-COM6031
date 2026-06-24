
from abc import ABC, abstractmethod


class ReactionStrategy(ABC):

    @abstractmethod
    def react(self, name: str, old: float, new: float) -> str: ...


class PriceSensitive(ReactionStrategy):

    def react(self, name: str, old: float, new: float) -> str:
        if new > old * 1.10:
            return f"{name}: rise exceeds 10%, switching insurer"
        return f"{name}: rise acceptable, staying"


class Loyal(ReactionStrategy):

    def react(self, name: str, old: float, new: float) -> str:
        return f"{name}: remains with current insurer"


class CorporateNegotiator(ReactionStrategy):

    def react(self, name: str, old: float, new: float) -> str:
        if new - old > 100:
            return f"{name}: triggering contract renegotiation"
        return f"{name}: absorbing the change for now"


class RiskAverse(ReactionStrategy):

    def react(self, name: str, old: float, new: float) -> str:
        if new < old:
            return f"{name}: premium fell, purchasing additional cover"
        return f"{name}: maintaining current cover"


class Entity:

    def __init__(self, name: str, strategy: ReactionStrategy) -> None:
        self.name = name
        self._strategy = strategy

    def set_strategy(self, strategy: ReactionStrategy) -> None:
        self._strategy = strategy

    def respond(self, old: float, new: float) -> None:
        print("  " + self._strategy.react(self.name, old, new))

    def __repr__(self) -> str:
        return f"Entity({self.name!r}, {type(self._strategy).__name__})"


def broadcast(entities: list[Entity], old: float, new: float) -> None:
    """A manual broadcast helper - note the caller must drive this itself."""
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

    print("\nAlice becomes loyal (strategy swapped at runtime):")
    saharsh.set_strategy(Loyal())
    broadcast(entities, 1000, 1200)

    print("\nA premium CUT (1000 -> 900):")
    broadcast(entities, 1000, 900)


if __name__ == "__main__":
    main()
