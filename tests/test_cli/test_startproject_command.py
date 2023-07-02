import subprocess
import pytest
import json

from litdjango.utils import print_notebook_contents


project_name = "testproject"


def test_startproject_return_code(tmp_path):
    assert subprocess.check_call(["litdjango", "startproject", project_name], cwd=str(tmp_path)) == 0


@pytest.fixture(scope="module")
def created_project(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("dir", numbered=False)
    subprocess.check_call(["litdjango", "startproject", project_name], cwd=str(tmp_path))
    return tmp_path / project_name


@pytest.mark.parametrize("path", [
    "nbs/",
    "nbs/manage.ipynb",
    "nbs/config/",
    "nbs/config/settings.ipynb",
    "nbs/config/wsgi.ipynb",
    "nbs/config/asgi.ipynb",
    "nbs/config/urls.ipynb",
    # f"{project_name}/"
])
def test_startproject_structure(created_project, path):
    output_path = created_project / path
    assert output_path.exists(), f"{output_path=}"
    if path[-1] == "/":
        assert output_path.is_dir(), f"{output_path=}"


def test_manage_module(created_project):
    with open(created_project / "nbs/manage.ipynb") as f:
        contents = f.read()
        assert project_name in contents, print_notebook_contents(contents)


def test_config_wsgi_module(created_project):
    with open(created_project / "nbs/config/wsgi.ipynb") as f:
        contents = f.read()
        assert "config.wsgi" in contents, print_notebook_contents(contents)


def test_config_asgi_module(created_project):
    with open(created_project / "nbs/config/asgi.ipynb") as f:
        contents = f.read()
        assert "config.asgi" in contents, print_notebook_contents(contents)


def test_config_urls_module(created_project):
    with open(created_project / "nbs/config/urls.ipynb") as f:
        contents = f.read()
        assert project_name in contents, print_notebook_contents(contents)
        assert "config.urls" in contents, print_notebook_contents(contents)


def test_config_settings_module(created_project):
    with open(created_project / "nbs/config/settings.ipynb") as f:
        contents = f.read()
        assert "litdjango" in contents, print_notebook_contents(contents)
        assert "SECRET_KEY" in contents, print_notebook_contents(contents)