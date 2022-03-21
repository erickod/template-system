from dynaconf import Dynaconf
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from template_system.adapters.web import (
    TemplateApplierController,
    fast_api_domain_request_factory,
)
from template_system.application import TemplateServiceFactory
from template_system.template_exporter.docx_to_pdf import (
    LibreOfficeDocxToPDFTemplateExporter,
)

settings = Dynaconf(settings_file=["settings.toml"], environments=True)


def configure(app: FastAPI) -> None:
    @app.post(f"/{settings.API_VERSION}/templating/")
    async def apply_template(request: Request):
        domain_request = await fast_api_domain_request_factory(request)

        template_service = TemplateServiceFactory.create_with_dict_repository(
            domain_request.data.get("template_vars", {}),
            **getattr(domain_request, "files", {}),
        )

        exporter = LibreOfficeDocxToPDFTemplateExporter()
        template_service.register_exporter(exporter)
        controller = TemplateApplierController(template_service)
        output = await controller.handle(domain_request)
        return JSONResponse(output.data, output.status_code)
