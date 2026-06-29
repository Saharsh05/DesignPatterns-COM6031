"""Scenario 2 - CHOSEN SOLUTION: OBSERVER + STRATEGY combined

The requirement decomposes into two concerns that map onto two patterns:
  * OBSERVER  governs notification - InsurancePolicy (Subject) broadcasts each
    premium change to every attached Entity (Observer).
  * STRATEGY  governs reaction - each Entity delegates its response to an
    interchangeable ReactionStrategy that can be swapped at runtime.

Separating the two keeps the Subject ignorant of how entities respond, and keeps
each reaction algorithm ignorant of when notifications are dispatched. The GoF
note that Model-View-Controller is itself built principally from Observer,
Composite and Strategy, so combining them here is well precedented.
"""

from abc import ABC, abstractmethod


class ReactionStrategy(ABC):
    """Strategy interface used by observers to decide how to react."""

    @abstractmethod
    def react(self, name: str, old: float, new: float) -> str: ...


class BudgetSensitiveReaction(ReactionStrategy):
    """Budget-sensitive behavior: switch if premium rises too quickly."""

    def react(self, name: str, old: float, new: float) -> str:
        if new > old * 1.10:
            return f"  {name} (budget-sensitive): rose >10%, SWITCHING insurer"
        return f"  {name} (budget-sensitive): rise acceptable, staying"


class ComplianceReaction(ReactionStrategy):
    """Compliance behavior: record the premium change for audit."""

    def react(self, name: str, old: float, new: float) -> str:
        return f"  {name} (compliance): recording {old:.0f}->{new:.0f} for audit"


class ReinsuranceReaction(ReactionStrategy):
    """Reinsurance behavior: reprice exposure based on the premium change."""

    def react(self, name: str, old: float, new: float) -> str:
        return f"  {name} (reinsurance): re-pricing exposure by {new - old:+.0f}"


class BrokerReaction(ReactionStrategy):
    """Broker behavior: calculate commission from the premium change."""

    def react(self, name: str, old: float, new: float) -> str:
        return f"  {name} (broker): commission {(new - old) * 0.05:+.2f}"


class PremiumObserver(ABC):
    """Observer interface for objects watching premium changes."""

    @abstractmethod
    def update(self, old: float, new: float) -> None: ...


class Entity(PremiumObserver):
    """Concrete observer with a runtime-switchable reaction strategy."""

    def __init__(self, name: str, strategy: ReactionStrategy) -> None:
        self.name = name
        self._strategy = strategy

    def set_strategy(self, strategy: ReactionStrategy) -> None:
        # This allows the same observer to change behavior at runtime.
        self._strategy = strategy

    def update(self, old: float, new: float) -> None:
        # Delegate the premium update handling to the current strategy.
        print(self._strategy.react(self.name, old, new))

    def __repr__(self) -> str:
        return f"Entity({self.name!r}, {type(self._strategy).__name__})"


class InsurancePolicy:
    """Subject class that notifies observers whenever the premium changes."""

    def __init__(self, name: str, premium: float) -> None:
        self.name = name
        self._premium = float(premium)
        self._observers: list[PremiumObserver] = []

    def attach(self, observer: PremiumObserver) -> None:
        self._observers.append(observer)

    def detach(self, observer: PremiumObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def set_premium(self, new_premium: float) -> None:
        old, self._premium = self._premium, float(new_premium)
        print(f"Policy '{self.name}': premium {old:.0f} -> {self._premium:.0f}")
        for observer in self._observers:
            observer.update(old, self._premium)


def main() -> None:
    policy = InsurancePolicy("Motor-Fleet", 1000.0)
    saharsh = Entity("Saharsh", BudgetSensitiveReaction())
    policy.attach(saharsh)
    policy.attach(Entity("FCA", ComplianceReaction()))
    policy.attach(Entity("SwissRe", ReinsuranceReaction()))

    print("Premium increase #1:")
    policy.set_premium(1200.0)

    print("\nSaharsh becomes more tolerant (Strategy swapped at runtime):")
    saharsh.set_strategy(ComplianceReaction())
    print("Premium increase #2:")
    policy.set_premium(1450.0)

    print("\nA broker joins mid-simulation (Observer attached at runtime):")
    policy.attach(Entity("Broker", BrokerReaction()))
    print("Premium increase #3:")
    policy.set_premium(1500.0)


if __name__ == "__main__":
    main()
