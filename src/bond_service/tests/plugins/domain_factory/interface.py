from typing import Awaitable, Protocol

from app.domains.portfolio import (
    BondEntity,
    BondOperationEntity,
    PortfolioAggregate,
)


class OperationFactoryInterface(Protocol):
    def __call__(self, *args, **kwargs) -> BondOperationEntity:
        """
        Operation data factory interface
        :param args:
        :param kwargs:
        :return:
        """


class BondFactoryInterface(Protocol):
    def __call__(self, *args, **kwargs) -> BondEntity:
        """
        Bond data factory interface
        :param args:
        :param kwargs:
        :return:
        """


class PortfolioFactoryInterface(Protocol):
    def __call__(self, *args, **kwargs) -> PortfolioAggregate:
        """
        Portfolio data factory interface
        :param args:
        :param kwargs:
        :return:
        """


class OperationBuilderInterface(Protocol):
    def __call__(self, *args, **kwargs) -> Awaitable[BondOperationEntity]:
        """
        Operation data builder interface
        :param args:
        :param kwargs:
        :return:
        """


class BondBuilderInterface(Protocol):
    def __call__(self, *args, **kwargs) -> Awaitable[BondEntity]:
        """
        Bond data builder interface
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
