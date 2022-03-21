from collections.abc import Generator

import pytest
from template_system.application import TemplateService
from template_system.application.template_service import (
    DocxToPDFDictTemplateDataRepository,
)
from template_system.domain import TemplateData
from template_system.errors import (
    InvalidTemplateExporterError,
    NoExporterRegisteredError,
)

from tests.helpers import StubTemplateExporter


def test_template_service_instantiation_params() -> None:
    repo = DocxToPDFDictTemplateDataRepository()
    sut = TemplateService(repo)
    assert type(sut.exporters) is set
    assert sut.exporters == set()


def test_ensure_template_service_can_register_an_exporter() -> None:
    stub_exporter = StubTemplateExporter()
    repo = DocxToPDFDictTemplateDataRepository()
    sut = TemplateService(repo)
    sut.register_exporter(stub_exporter)
    assert stub_exporter in list(sut.exporters)


def test_template_service_raises_when_trying_register_an_invalid_exporter() -> None:
    invalid_exporter = {}
    repo = DocxToPDFDictTemplateDataRepository()
    sut = TemplateService(repo)
    with pytest.raises(InvalidTemplateExporterError):
        sut.register_exporter(invalid_exporter)


def test_template_service_apply_templates_returns_a_generator() -> None:
    repo = DocxToPDFDictTemplateDataRepository()
    sut = TemplateService(repo)
    generator = sut.apply_templates(template_vars={}, raises=True)
    assert isinstance(generator, Generator)


def test_template_service_raises_when_trying_apply_templates_with_no_registeredexporters() -> None:
    repo = DocxToPDFDictTemplateDataRepository()
    sut = TemplateService(repo)
    with pytest.raises(NoExporterRegisteredError):
        next(sut.apply_templates(template_vars={}, raises=True))


def test_apply_templates_dont_raises_whit_noexporters_and_a_false_raises_param() -> None:
    repo = DocxToPDFDictTemplateDataRepository()
    sut = TemplateService(repo)
    list(sut.apply_templates(template_vars={}, raises=False))


def test_apply_templates_calls_make_template_data_from_exporter() -> None:
    stub_exporter = StubTemplateExporter()
    assert not stub_exporter.config_template_data_is_called

    repo = DocxToPDFDictTemplateDataRepository(
        {"{{id}}": "any_valid_id"}, file={"file": ""}
    )
    sut = TemplateService(repo)
    sut.register_exporter(stub_exporter)
    list(sut.apply_templates(template_vars={}, raises=False))
    assert stub_exporter.config_template_data_is_called


def test_apply_templates_calls_process_data_from_exporter() -> None:
    stub_exporter = StubTemplateExporter()
    assert not stub_exporter.process_is_called

    repo = DocxToPDFDictTemplateDataRepository({"any": "any"}, file="")
    sut = TemplateService(repo)
    sut.register_exporter(stub_exporter)
    list(sut.apply_templates(template_vars={}, raises=False))
    assert stub_exporter.process_is_called


def test_apply_templates_returns_a_template_data_from_exporter() -> None:
    stub_exporter = StubTemplateExporter()
    repo = DocxToPDFDictTemplateDataRepository({"any": "any"}, file="")
    sut = TemplateService(repo)
    sut.register_exporter(stub_exporter)
    template_data = list(sut.apply_templates(template_vars={}, raises=False))[0]
    assert type(template_data) is TemplateData
