from abc import ABC, abstractmethod


class Colleague(ABC):

    def __init__(self, name: str) -> None:
        self.name = name
        self.mediator: "InsuranceMediator | None" = None


class InsuranceMediator(ABC):
    """Mediator interface: colleagues notify it, it coordinates the rest."""

    @abstractmethod
    def premium_changed(self, sender: Colleague, old: float, new: float) -> None: ...


class Policy(Colleague):

    def __init__(self, mediator: InsuranceMediator, premium: float) -> None:
        super().__init__("Policy")
        self.mediator = mediator
        self._premium = float(premium)

    def set_premium(self, new_premium: float) -> None:
        old, self._premium = self._premium, float(new_premium)
        print(f"Policy: premium {old:.0f} -> {new_premium:.0f}")
        assert self.mediator is not None
        self.mediator.premium_changed(self, old, self._premium)


class Customer(Colleague):
    def react(self, old: float, new: float) -> None:
        print(f"  Customer : {'leaving' if new > old * 1.1 else 'staying'}")


class Reinsurer(Colleague):
    def react(self, old: float, new: float) -> None:
        print(f"  Reinsurer: re-pricing by {new - old:+.0f}")


class Regulator(Colleague):
    def react(self, old: float, new: float) -> None:
        print(f"  Regulator: recorded {old:.0f}->{new:.0f}")


class PremiumMediator(InsuranceMediator):

    def __init__(self) -> None:
        self._customer: Customer | None = None
        self._reinsurer: Reinsurer | None = None
        self._regulator: Regulator | None = None

    def register(self, customer: Customer, reinsurer: Reinsurer,
                 regulator: Regulator) -> None:
        self._customer, self._reinsurer, self._regulator = (
            customer, reinsurer, regulator)
        for c in (customer, reinsurer, regulator):
            c.mediator = self

    def premium_changed(self, sender: Colleague, old: float, new: float) -> None:
        # The mediator decides who reacts and in what order.
        for colleague in (self._customer, self._reinsurer, self._regulator):
            if colleague is not None and colleague is not sender:
                colleague.react(old, new)


def main() -> None:
    mediator = PremiumMediator()
    mediator.register(Customer("Customer"), 
                      Reinsurer("Reinsurer"),
                      Regulator("Regulator"))
    policy = Policy(mediator, 1000.0)

    policy.set_premium(1150.0)
    print()
    policy.set_premium(1400.0)
    print()
    policy.set_premium(1050.0)



if __name__ == "__main__":
    main()
