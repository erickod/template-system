from typing import Any

from typing_extensions import Protocol

from .template_data import TemplateDataProtocol


class TemplateApplier(Protocol):
    def apply_template_vars(self, template_data: TemplateDataProtocol) -> Any:
        return
