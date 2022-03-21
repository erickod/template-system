from typing import Any, Dict

from template_system.application import protocols
from template_system.application.protocols import TemplateDataProtocol
from template_system.domain import TemplateData


class StubTemplateExporter(protocols.TemplateExporterABC):
    suported_types = ["docx"]
    output_type = "pdf"

    def __init__(self) -> None:
        self.config_template_data_is_called = False
        self.process_is_called = False

    def process(
        self, data: protocols.TemplateDataProtocol
    ) -> protocols.TemplateDataProtocol:
        self.process_is_called = True
        print("process is called")

        return TemplateData(
            input="stub_input_data",
            output="stub_output_data",
            input_type="stub_input_template",
            output_type="stub_output_template",
            template_vars={},
        )

    def config_template_data(
        self, template_data: TemplateDataProtocol
    ) -> TemplateDataProtocol:
        self.config_template_data_is_called = True
        return template_data

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        return self.__str__()
