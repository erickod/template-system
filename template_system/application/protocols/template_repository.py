from abc import abstractmethod
from typing import Generator

from typing_extensions import Protocol, runtime_checkable

from .template_data import TemplateDataProtocol


@runtime_checkable
class TemplateRepository(Protocol):

    @abstractmethod
    def get_template_data(self, **kwargs) -> Generator[
        TemplateDataProtocol, None, None
    ]:
        pass

    @abstractmethod
    def save(self, template_data: TemplateDataProtocol) -> None:
        pass
