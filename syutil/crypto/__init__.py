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


class Key:
    """
    Interface only
    """
    def __init__(self):
        self.alg = None

class SigningKey(Key):
    """
    Interface only

    Returns: syutil.crypto.Signature

    """
    def sign(self, bytes):
        pass

class VerifyKey(Key):
    """
    Interface only
    """
    def verify(self, bytes):
        pass

class Signature:
    def __init__(self):
        self.signature = None