from abc import ABC, abstractmethod
from turtle import st
from typing import Any, Dict, Generator, Iterable, Protocol

from template_system.domain import TemplateData
from template_system.errors import (
    InvalidTemplateExporterError,
    NoExporterRegisteredError,
)

from .protocols import TemplateExporterABC


class TemplateDataRepository(Protocol):
    @abstractmethod
    def load_template_data(self) -> Iterable[TemplateData]:
        ...


class DictTemplateDataRepositoryABC(TemplateDataRepository):
    def __init__(self, *template_vars: Dict[Any, Any], **extra_args) -> None:
        self._template_vars_iterator = template_vars
        self._extra_args = extra_args


class DocxToPDFDictTemplateDataRepository(
    DictTemplateDataRepositoryABC,
):
    def __init__(self, *template_vars: Dict[Any, Any], **extra_args) -> None:
        super().__init__(*template_vars, **extra_args)

    def load_template_data(self) -> Iterable[TemplateData]:
        template_vars_list = []
        for template_vars in self._template_vars_iterator:
            template_vars_list.append(
                TemplateData(
                    input=self._extra_args["file"],
                    output="",
                    input_type="docx",
                    output_type="pdf",
                    template_vars=template_vars,
                ),
            )
        return template_vars_list


class TemplateServiceABC(ABC):
    def __init__(
        self,
        template_data_repo: TemplateDataRepository,
    ) -> None:
        self.exporters = set()  # type: ignore
        self._repo = template_data_repo

    @abstractmethod
    def apply_templates(
        self, template_vars: Dict[Any, Any], raises=False, **kwargs
    ) -> Generator[TemplateData, None, None]:
        pass

    def supports_templating(
        self,
        *,
        input_type: str,
        output_type: str,
    ) -> bool:
        input_type = input_type.lower()
        output_type = output_type.lower()
        for exporter in self.exporters:
            if (
                input_type in exporter.suported_types
                and output_type == exporter.output_type
            ):
                return True
        return False


class TemplateService(TemplateServiceABC):
    def __init__(
        self,
        template_data_repo: TemplateDataRepository,
    ) -> None:
        super().__init__(template_data_repo)

    def apply_templates(
        self, template_vars: Dict[Any, Any], raises=False, **kwargs
    ) -> Generator[TemplateData, None, None]:

        if raises and not self.exporters:
            raise NoExporterRegisteredError

        for template_data in self._repo.load_template_data():
            for exporter in list(self.exporters):
                exporter.config_template_data(template_data)
                exporter.process(template_data)
                yield template_data

    def register_exporter(self, *exporters) -> Any:
        for exporter in exporters:
            if not isinstance(exporter, TemplateExporterABC):
                raise InvalidTemplateExporterError
            self.exporters.add(exporter)


class TemplateServiceFactory:
    @staticmethod
    def create_with_dict_repository(
        *template_vars: Dict[Any, Any], **extra_args
    ) -> TemplateService:
        repo = DocxToPDFDictTemplateDataRepository(
            *template_vars,
            **extra_args,
        )
        template_service = TemplateService(repo)
        return template_service

    @staticmethod
    def create_with_regular_repository(
        repo: TemplateDataRepository, **extra_args
    ) -> TemplateService:
        template_service = TemplateService(repo, **extra_args)
        return template_service
