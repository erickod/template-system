import io
from pathlib import Path
from tempfile import gettempdir
from unittest import mock

from template_system.domain import TemplateData
from template_system.template_exporter.docx_to_pdf import DocxTemplateVarsApplier


def test_DocxTemplateVarsApplier_instantiation_parms() -> None:
    sut = DocxTemplateVarsApplier()
    assert sut._DocxTemplateVarsApplier__template_items == []
    assert sut._DocxTemplateVarsApplier__temp_dir == gettempdir()


def test_apply_template_vars_calls_template_factory() -> None:
    template_data = TemplateData(b"input", "output", "docx", "pdf", {})
    template_factory = mock.MagicMock()
    sut = DocxTemplateVarsApplier(template_factory=template_factory)
    sut.apply_template_vars(template_data)
    template_factory.assert_called()


def test_apply_template_vars_calls___process_section_with_right_params() -> None:
    template_data = TemplateData(b"input", "output", "docx", "pdf", {})
    template_factory = mock.MagicMock()
    sut = DocxTemplateVarsApplier(template_factory=template_factory)
    sut._DocxTemplateVarsApplier__process_paragraphs = mock.Mock()
    sut.apply_template_vars(template_data)
    sut._DocxTemplateVarsApplier__process_paragraphs.assert_called()


def test_apply_template_vars_calls___process_tables_with_right_params() -> None:
    template_data = TemplateData(b"input", "output", "docx", "pdf", {})
    template_factory = mock.MagicMock()
    sut = DocxTemplateVarsApplier(template_factory=template_factory)
    sut._DocxTemplateVarsApplier__process_tables = mock.Mock()
    sut.apply_template_vars(template_data)
    sut._DocxTemplateVarsApplier__process_tables.assert_called()


def test_apply_template_vars_calls__process_section_with_right_params() -> None:
    template_data = TemplateData(b"input", "output", "docx", "pdf", {})
    template_factory = mock.MagicMock()
    sut = DocxTemplateVarsApplier(template_factory=template_factory)
    sut._DocxTemplateVarsApplier__process_section = mock.Mock()
    sut.apply_template_vars(template_data)
    sut._DocxTemplateVarsApplier__process_section.assert_called()
