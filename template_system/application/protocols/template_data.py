from abc import abstractmethod
from typing import Any, Dict, List

from typing_extensions import Protocol, runtime_checkable


class TemplateExporter:
    ...


@runtime_checkable
class TemplateDataProtocol(Protocol):
    input: Any
    input_type: Any
    output: Any
    output_type: Any
    template_vars: Dict[Any, Any]
    unique_identifier: str
    exporters: List[str]

    @abstractmethod
    def __getitem__(self, key: Any) -> Any:
        pass

    @abstractmethod
    def items(self) -> Any:
        pass
