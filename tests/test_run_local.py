# Copyright 2018 Iguazio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import getpass
from os import path, environ

from mlrun import new_task, run_local, code_to_function
from tests.conftest import (
    examples_path,
    out_path,
    tag_test,
    verify_state,
)

base_spec = new_task(params={"p1": 8}, out_path=out_path)
base_spec.spec.inputs = {"infile.txt": "infile.txt"}


def test_run_local():
    spec = tag_test(base_spec, "test_run_local")
    result = run_local(
        spec, command=f"{examples_path}/training.py", workdir=examples_path
    )
    verify_state(result)


def test_run_local_with_uid_does_not_exist(monkeypatch):
    """
    Mocking a scenario that happened in field in which getuser raised the same error as the mock
    The problem was basically that the code was
    environ.get("V3IO_USERNAME", getpass.getuser())
    instead of
    environ.get("V3IO_USERNAME") or getpass.getuser()
    """

    def mock_getpwuid_raise(*args, **kwargs):
        raise KeyError("getpwuid(): uid not found: 400")

    environ["V3IO_USERNAME"] = "some_user"
    monkeypatch.setattr(getpass, "getuser", mock_getpwuid_raise)
    spec = tag_test(base_spec, "test_run_local")
    result = run_local(
        spec, command=f"{examples_path}/training.py", workdir=examples_path
    )
    verify_state(result)


def test_run_local_handler():
    spec = tag_test(base_spec, "test_run_local_handler")
    spec.spec.handler = "my_func"
    result = run_local(
        spec, command=f"{examples_path}/handler.py", workdir=examples_path
    )
    verify_state(result)


def test_run_local_nb():
    spec = tag_test(base_spec, "test_run_local_nb")
    spec.spec.handler = "training"
    result = run_local(
        spec, command=f"{examples_path}/mlrun_jobs.ipynb", workdir=examples_path
    )
    verify_state(result)


def test_run_local_yaml():
    spec = tag_test(base_spec, "test_run_local_yaml")
    spec.spec.handler = "training"
    nbpath = f"{examples_path}/mlrun_jobs.ipynb"
    ymlpath = path.join(out_path, "nbyaml.yaml")
    print("out path:", out_path, ymlpath)
    code_to_function(filename=nbpath, kind="job").export(ymlpath)
    result = run_local(spec, command=ymlpath, workdir=out_path)
    verify_state(result)


def test_run_local_obj():
    spec = tag_test(base_spec, "test_run_local_obj")
    spec.spec.handler = "training"
    nbpath = f"{examples_path}/mlrun_jobs.ipynb"
    ymlpath = path.join(out_path, "nbyaml.yaml")
    print("out path:", out_path, ymlpath)
    fn = code_to_function(filename=nbpath, kind="job").export(ymlpath)
    result = run_local(spec, command=fn, workdir=out_path)
    verify_state(result)


def test_run_local_from_func():
    spec = tag_test(base_spec, "test_run_local_from_func")
    spec.spec.handler = "training"
    nb_path = f"{examples_path}/mlrun_jobs.ipynb"
    nbyml_path = path.join(out_path, "nbyaml.yaml")
    print("out path:", out_path, nbyml_path)
    fn = code_to_function(filename=nb_path, kind="job").export(nbyml_path)
    result = fn.run(spec, workdir=out_path, local=True)
    verify_state(result)
