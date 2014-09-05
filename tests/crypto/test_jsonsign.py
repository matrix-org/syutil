# -*- coding: utf-8 -*-

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

import unittest

from syutil.base64util import encode_base64
import syutil.crypto
import syutil.crypto.jsonsign


class SyutilJsonSignTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sign_and_verify(self):
        message = {'foo': 'bar'}
        sigkey = MockSigningKey()
        signed = syutil.crypto.jsonsign.sign_json(message, 'Alice', sigkey)

        self.assertIn('signatures', signed)
        self.assertIn('Alice:mock', signed['signatures'])
        self.assertEqual(signed['signatures']['Alice:mock'], encode_base64('x_______'))

        verkey = MockVerifyKey()
        syutil.crypto.jsonsign.verify_signed_json(signed, 'Alice', verkey)

    def test_verify_fail(self):
        message = {'foo': 'bar'}
        sigkey = MockSigningKey()
        signed = syutil.crypto.jsonsign.sign_json(message, 'Alice', sigkey)

        signed['signatures']['Alice:mock'] = encode_base64('not a signature')

        verkey = MockVerifyKey()

        with self.assertRaises(syutil.crypto.jsonsign.SignatureVerifyException):
            syutil.crypto.jsonsign.verify_signed_json(signed, 'Alice', verkey)


class MockSigningKey(syutil.crypto.SigningKey):
    def __init__(self):
        self.alg = "mock"

    def sign(self, bytes):
        return MockSignature()

class MockVerifyKey(syutil.crypto.VerifyKey):
    def __init__(self):
        self.alg = "mock"

    def verify(self, message, sig):
        if not sig == "x_______":
            raise Exception()

class MockSignature(syutil.crypto.Signature):
    def __init__(self):
        self.signature = "x_______"

