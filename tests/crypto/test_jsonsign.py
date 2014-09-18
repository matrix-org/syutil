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
from syutil.crypto.jsonsign import (
    sign_json, verify_signed_json,  SignatureVerifyException
)


class SyutilJsonSignTestCase(unittest.TestCase):
    def setUp(self):
        self.message = {'foo': 'bar'}
        self.sigkey = MockSigningKey()
        print self.sigkey.alg
        self.signed = sign_json(self.message, 'Alice', self.sigkey)
        self.verkey = MockVerifyKey()

    def test_sign_and_verify(self):
        self.assertIn('signatures', self.signed)
        self.assertIn('Alice', self.signed['signatures'])
        self.assertIn('mock:test', self.signed['signatures']['Alice'])
        self.assertEqual(
            self.signed['signatures']['Alice']['mock:test'],
            encode_base64('x_______')
        )
        verify_signed_json(self.signed, 'Alice', self.verkey)

    def test_verify_fail(self):
        self.signed['signatures']['Alice']['mock:test'] = encode_base64(
            'not a signature'
        )
        print self.signed
        verkey = MockVerifyKey()

        with self.assertRaises(SignatureVerifyException):
            verify_signed_json(self.signed, 'Alice', self.verkey)


class MockSigningKey(object):
    alg = "mock"
    version = "test"

    def sign(self, bytes):
        return MockSignature()


class MockVerifyKey(object):
    alg = "mock"
    version = "test"

    def verify(self, message, sig):
        if not sig == "x_______":
            raise Exception()


class MockSignature(object):
    def __init__(self):
        self.signature = "x_______"

