from tempfile import gettempdir
from unittest import mock

from template_system.domain import TemplateData
from template_system.template_exporter.docx_to_pdf import (
    LibreOfficeDocxToPDFTemplateExporter,
)
from tests.helpers import StubDocxTemplateVarsApplier

template_data = TemplateData(b"filename.docx", "output", "docx", "pdf", {})


def test_LibreOfficeDocxToPDFTemplateExporter_instantiation_params() -> None:
    vars_applier = StubDocxTemplateVarsApplier()
    sut = LibreOfficeDocxToPDFTemplateExporter(vars_applier)

    assert sut.suported_types == ("docx",)
    assert sut.output_type == "pdf"
    assert sut._template_vars_applier == vars_applier


def test_config_template_data_returns_a_right_template_data() -> None:
    template_data = TemplateData("input.docx", "output", "docx", "pdf", {})
    vars_applier = StubDocxTemplateVarsApplier()
    sut = LibreOfficeDocxToPDFTemplateExporter(vars_applier)
    data = sut.config_template_data(template_data)
    assert type(data) is TemplateData
    assert data.input == template_data.input
    assert data.input_type == "docx"
    assert data.output_type == "pdf"


def test_LibreOfficeDocxToPDFTemplateExporter_process_returns_a_template_data() -> None:
    vars_applier = StubDocxTemplateVarsApplier()
    sut = LibreOfficeDocxToPDFTemplateExporter(
        vars_applier, subprocess_executor=mock.Mock()
    )

    data = sut.process(sut.config_template_data(template_data))
    assert type(data) is TemplateData


def test_LibreOfficeDocxToPDFTemplateExporter_process_calls_apply_template_vars_from_var_applier() -> None:
    vars_applier = StubDocxTemplateVarsApplier()
    sut = LibreOfficeDocxToPDFTemplateExporter(
        vars_applier, subprocess_executor=mock.Mock()
    )
    sut.process(sut.config_template_data(template_data))
    assert vars_applier.apply_template_vars_called


def test_LibreOfficeDocxToPDFTemplateExporter_subprecess_executor_is_called_with_right_parms() -> None:
    subprocess_executor = mock.Mock()
    vars_applier = StubDocxTemplateVarsApplier()
    sut = LibreOfficeDocxToPDFTemplateExporter(
        vars_applier, subprocess_executor=subprocess_executor
    )
    sut.process(sut.config_template_data(template_data))
    subprocess_executor.assert_called_with(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "updated_input",
            "--outdir",
            gettempdir(),
        ]
    )
