from typing import Callable

from fastapi import FastAPI
from template_system.api import export_pdf_from_docx, recover_exported_from_link


def endpoints_factory(app: FastAPI) -> None:
    export_pdf_from_docx.configure(app)
    recover_exported_from_link.configure(app)


def app_factory(endpoints_factory: Callable = endpoints_factory) -> FastAPI:
    app = FastAPI()
    endpoints_factory(app)
    return app
