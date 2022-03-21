from typing import Any

from template_system.application.protocols import TemplateDataProtocol


class StubDocxTemplateVarsApplier:
    def __init__(self) -> None:
        self.apply_template_vars_called: bool = False

    def apply_template_vars(self, template_data: TemplateDataProtocol) -> Any:
        self.apply_template_vars_called = True
        template_data.input = "updated_input"
        return template_data
