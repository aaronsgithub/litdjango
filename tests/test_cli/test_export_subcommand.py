import os
import subprocess
import shutil

import pytest


project_name = "testproject"


def test_export_subcommand_exists():
    output = subprocess.run(["litdjango"], capture_output=True, text=True)
    assert "export" in output.stdout, output.stdout


def test_startproject_and_export_return_code(tmp_path):
    """Check these subcommands work then use them to create a fixture"""
    try:
        assert subprocess.check_call(["litdjango", "startproject", project_name], cwd=tmp_path) == 0
        assert subprocess.check_call(["litdjango", "export"], cwd=tmp_path/project_name) == 0
    finally:
        shutil.rmtree(tmp_path)


@pytest.fixture(scope="module")
def exported_project(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("dir")
    old_path = os.getcwd()
    os.chdir(tmp_path)
    subprocess.check_call(["litdjango", "startproject", project_name], cwd=tmp_path) 
    os.chdir(tmp_path / project_name)
    subprocess.check_call(["litdjango", "export"])
    try:
        yield tmp_path / project_name
    finally:
        shutil.rmtree(tmp_path)
        os.chdir(old_path)


@pytest.mark.parametrize("path",[
    f"{project_name}/",
    f"{project_name}/manage.py",
    f"{project_name}/config/",
    f"{project_name}/config/settings.py",
    f"{project_name}/config/wsgi.py",
    f"{project_name}/config/asgi.py",
    f"{project_name}/config/urls.py",
])
def test_new_project_renders_python_modules(exported_project, path):
    output_path = exported_project / path
    assert output_path.exists(), f"{output_path=}"
    if path.endswith("/"):
        assert output_path.is_dir(), f"{output_path=}"


def test_manage_module(exported_project):
    assert subprocess.check_call(["python", f"{project_name}/manage.py", "check"]) == 0