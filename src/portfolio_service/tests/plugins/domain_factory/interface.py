from typing import Awaitable, Protocol

from app.domains.portfolio import PortfolioAggregate


class PortfolioFactoryInterface(Protocol):
    def __call__(self, *args, **kwargs) -> PortfolioAggregate:
        """
        Portfolio data factory interface
        :param args:
        :param kwargs:
        :return:
        """


class PortfolioBuilderInterface(Protocol):
    def __call__(self, *args, **kwargs) -> Awaitable[PortfolioAggregate]:
        """
        Portfolio data builder interface
        :param args:
        :param kwargs:
        :return:
        """
