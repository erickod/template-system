from datetime import datetime
from hashlib import md5
from typing import Any, Dict, List
from uuid import uuid4


class TemplateExporter:
    ...


class TemplateData:
    def __init__(
        self,
        input: Any,
        output: Any,
        input_type: Any,
        output_type: Any,
        template_vars: Dict[Any, Any],
    ) -> None:
        self.input = input
        self.input_type = input_type
        self.output = output
        self.output_type = output_type
        self.template_vars = template_vars
        self.exporters: List[str]
        self.unique_identifier = md5(
            f"{uuid4()}{datetime.now()}{template_vars}".encode()
        ).hexdigest()

    def __getitem__(self, key: Any) -> Any:
        return

    def items(self) -> Any:
        return

    def __str__(self) -> str:
        str_repr = f"TemplateData(input={self.input}, output={self.output}, "
        str_repr += f"input_type={self.input_type}, "
        return str_repr + f"output_type={self.output_type}, "
