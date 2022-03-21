import asyncio
import base64
import json
from pathlib import Path
from typing import Any, Dict

from dynaconf import Dynaconf
from fastapi.requests import Request
from template_system.application.template_service import TemplateService
from template_system.errors import TemplateProcessError
from template_system.utils.remove_file import remove_file

settings = Dynaconf(settings_file=["settings.toml"], environments=True)


async def fast_api_domain_request_factory(
    request: Request,
) -> "DomainHttpRequest":
    form = await request.form()
    domain_request = DomainHttpRequest()
    domain_request.url = str(request.base_url)
    domain_request.method = request.method
    domain_request.query_params.update(request.query_params.items())
    domain_request.data.update(
        {k: json.loads(v) for k, v in form.items() if type(v) is str}
    )
    domain_request.files = {
        k: await v.read() for k, v in form.items() if type(v) != str
    }
    return domain_request


class DomainHttpResponse:
    # TODO: add Auth
    # TODO: add cookies
    # TODO: add header
    # TODO: add files

    def __init__(
        self,
        status_code: int,
        data: Dict[Any, Any] = {},
        files={},
    ) -> None:
        self.status_code: int = status_code
        self.data: Dict[Any, Any] = data


class DomainHttpRequest:
    # TODO: add Auth
    # TODO: add cookies
    # TODO: add header

    def __init__(self) -> None:

        self.url: str = ""
        self.status_code: int = 200
        self.method: str = ""
        self.files: Dict[Any, Any] = {}
        self._data: Dict[Any, Any] = {}
        self._query_params: Dict[Any, Any] = {}

    @property
    def data(self) -> Dict[Any, Any]:
        return self._data

    @data.setter
    def data(self, data: Any) -> None:
        self._data = data

    @property
    def query_params(self) -> Dict[Any, Any]:
        return self._query_params

    @query_params.setter
    def query_params(self, query_params: Any) -> None:
        self._query_params = query_params


class TemplateApplierController:
    def __init__(self, template_service: TemplateService) -> None:
        self._template_service = template_service

    async def handle(self, request: Any) -> Any:
        try:
            input_type = request.query_params["input"]
            output_type = request.query_params["output"]
        except KeyError as err:
            return DomainHttpResponse(
                400,
                {"error": f"missing query param {err}"},
            )

        if not self._template_service.supports_templating(
            input_type=input_type,
            output_type=output_type,
        ):
            return DomainHttpResponse(
                500,
                {
                    "message": "No exporter registered",
                    "input_type": input_type,
                    "output_type": output_type,
                },
            )
        try:
            template_data_generator = self._template_service.apply_templates(
                template_vars=request.data["template_vars"],
                input_file=request.files["file"],
            )

            template_data = next(template_data_generator)
            file_path = Path(template_data.output)
            asyncio.create_task(remove_file(template_data.input, 1))
        except TemplateProcessError as err:
            return DomainHttpResponse(
                500,
                {
                    "error": str(err),
                    "message": f"received file is not a valid {input_type}",
                    "informed_input_type": input_type,
                    "received_output_type": output_type,
                },
            )

        except KeyError as err:
            return DomainHttpResponse(
                400,
                {"error": f"missing field {err}"},
            )

        asyncio.create_task(remove_file(file_path))
        link = f"{request.url}{settings.API_VERSION}"
        link += f"/templating/{template_data.unique_identifier}"

        with open(template_data.output, "rb") as file:
            base64_encoded_file = base64.encodebytes(file.read()).decode()
            return DomainHttpResponse(
                200,
                {
                    "id": template_data.unique_identifier,
                    "extension": "pdf",
                    "link": link,
                    "link_expiration": {
                        "time": 300,
                        "time_unit": "seconds",
                    },
                    "base64_encoded_bytes": base64_encoded_file,
                },
            )
