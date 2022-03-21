from pathlib import Path
from tempfile import gettempdir

from dynaconf import Dynaconf
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

settings = Dynaconf(settings_file=["settings.toml"], environments=True)


def configure(app: FastAPI) -> None:
    @app.get(f"/{settings.API_VERSION}/templating/{{id}}")
    async def recover_exported_from_link(id: str):
        for file in Path(gettempdir()).glob("*"):
            if id in file.name:
                return FileResponse(file)
        return JSONResponse(
            {"error": "Resource expired or not existant"}, status_code=404
        )
