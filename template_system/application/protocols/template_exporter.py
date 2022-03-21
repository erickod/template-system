from abc import abstractmethod
from typing import Any, Dict, Tuple

from template_system.application.protocols import TemplateDataProtocol
from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class TemplateExporter(Protocol):
    suported_types: Tuple[str]
    output_type: str

    @abstractmethod
    def process(self, data: TemplateDataProtocol) -> TemplateDataProtocol:
        raise NotImplementedError

    @abstractmethod
    def config_template_data(
        self, template_data: TemplateDataProtocol
    ) -> TemplateDataProtocol:
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError


# @runtime_checkable
class TemplateExporterABC(TemplateExporter):
    def supports_template(self, template: TemplateDataProtocol) -> bool:
        return (
            template.input_type in self.suported_types
            and template.output_type == self.output_type
        )
