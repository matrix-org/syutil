# Copyright 2014 OpenMarket Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read_file(path_segments):
    """Read a file from the package. Takes a list of strings to join to
    make the path"""
    file_path = os.path.join(here, *path_segments)
    with open(file_path) as f:
        return f.read()


def exec_file(path_segments):
    """Execute a single python file to get the variables defined in it"""
    result = {}
    code = read_file(path_segments)
    exec(code, result)
    return result

version = exec_file(("syutil", "__init__.py"))["__version__"]
long_description = read_file(("README",))


setup(
    name="syutil",
    version=version,
    packages=find_packages(exclude=["tests"]),
    description="Synapse Matrix Server Utilities",
    install_requires=[
        "service_identity>=1.0.0",
        "pyasn1",
        "pynacl",
        "simplejson>=3.6.5",
        "frozendict>=0.4",
        "ujson>=1.33",
    ],
    setup_requires=[
        "setuptools_trial",
        "mock"
    ],
    include_package_data=True,
    long_description=long_description,
    test_suite='tests'
)
