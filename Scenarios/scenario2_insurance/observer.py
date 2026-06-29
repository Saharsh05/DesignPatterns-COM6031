"""Scenario 2 - Candidate 1: OBSERVER  (notification mechanism only)

Intent (GoF): define a one-to-many dependency so that when one object changes
state, all its dependents are notified and updated automatically.

Participants:
  * Subject          -> InsurancePolicy (maintains observers, broadcasts change)
  * Observer         -> PremiumObserver  (the update() interface)
  * ConcreteObserver -> Customer, Regulator, Broker, Actuary
  """



from abc import ABC, abstractmethod


class PremiumObserver(ABC):
    """Abstract observer that reacts to premium changes."""

    @abstractmethod
    def update(self, old: float, new: float) -> None: ...

    def label(self) -> str:
        return type(self).__name__


class InsurancePolicy:
    """Subject in the Observer pattern that notifies subscribed observers."""

    def __init__(self, premium: float) -> None:
        self._premium = float(premium)
        self._observers: list[PremiumObserver] = []

    @property
    def premium(self) -> float:
        return self._premium

    def attach(self, observer: PremiumObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: PremiumObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def observers(self) -> list[str]:
        return [o.label() for o in self._observers]

    def set_premium(self, new_premium: float) -> None:
        new_premium = float(new_premium)
        if new_premium < 0:
            raise ValueError("premium cannot be negative")
        old, self._premium = self._premium, new_premium
        self._notify(old, new_premium)

    def _notify(self, old: float, new: float) -> None:
        for observer in self._observers:
            observer.update(old, new)


class Customer(PremiumObserver):
    """Customer observer that decides whether to stay or cancel."""

    def update(self, old: float, new: float) -> None:
        verdict = "cancels" if new > old * 1.10 else "stays"
        print(f"  Customer : {old:.0f}->{new:.0f}, {verdict}")


class Regulator(PremiumObserver):
    """Regulator observer that logs premium changes."""

    def update(self, old: float, new: float) -> None:
        print(f"  Regulator: logged rate change {old:.0f}->{new:.0f}")


class Broker(PremiumObserver):
    """Broker observer that recalculates commission."""

    def update(self, old: float, new: float) -> None:
        commission = (new - old) * 0.05
        print(f"  Broker   : commission adjusted by {commission:+.2f}")


class Actuary(PremiumObserver):
    """Actuary observer that flags large premium swings."""

    def update(self, old: float, new: float) -> None:
        swing = abs(new - old) / old if old else 0.0
        flag = " (REVIEW)" if swing > 0.15 else ""
        print(f"  Actuary  : swing {swing:.0%}{flag}")


def main() -> None:
    policy = InsurancePolicy(1000.0)
    broker = Broker()
    for observer in (Customer(), Regulator(), broker, Actuary()):
        policy.attach(observer)

    print("Attached observers:", policy.observers())
    print("\nPremium rises to 1200:")
    policy.set_premium(1200.0)

    print("\nBroker leaves the deal (detached); premium rises to 1450:")
    policy.detach(broker)
    policy.set_premium(1450.0)

    print("\nValidation rejects a negative premium:")
    try:
        policy.set_premium(-10)
    except ValueError as exc:
        print("  rejected:", exc)


if __name__ == "__main__":
    main()
