import modal
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from yamlp.server.webapp import web_app

app = modal.App(name="yamlp")
volume = modal.Volume.from_name("YAMLP", create_if_missing=True)


modal_image = (
    modal.Image.debian_slim()
    .apt_install(["libgl1-mesa-glx", "libglib2.0-0"])
    .pip_install_from_pyproject("pyproject.toml")
    .add_local_python_source("yamlp")  # I'm getting an "automounting" warning without this. Not sure why.
    .add_local_dir("src/yamlp", remote_path="/src/yamlp")
    .add_local_dir("static", remote_path="/static")
)


@app.function(image=modal_image, container_idle_timeout=60, volumes={"/data": volume})
@modal.asgi_app()
def index() -> FastAPI:
    web_app.mount("/images", StaticFiles(directory="/data/images"), name="images")
    return web_app
