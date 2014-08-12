# -*- coding: utf-8 -*-

# Copyright 2014 matrix.org
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

from syutil.jsonutil import encode_canonical_json
from syutil.base64util import encode_base64, decode_base64

import twisted.python.log


def sign_json(json_object, signature_name, signing_key):
    """Sign the JSON object. Stores the signature in json_object["signatures"].

    Args:
        json_object (dict): The JSON object to sign.
        signature_name (str): The name of the signing entity.
        signing_key (syutil.crypto.SigningKey): The key to sign the JSON with.

    Returns:
        The modified, signed JSON object."""

    signatures = json_object.get("signatures", {})

    if "signatures" in json_object:
        del json_object["signatures"]

    signed = signing_key.sign(encode_canonical_json(json_object))

    sig_descriptor = "%s:%s" % (signature_name, signing_key.alg)

    signatures[sig_descriptor] = encode_base64(signed.signature)

    json_object["signatures"] = signatures

    return json_object


class SignatureVerifyException(Exception):
    """A signature could not be verified"""
    pass


def verify_signed_json(json_object, signature_name, verify_key):
    """Check a signature on a signed JSON object.

    Args:
        json_object (dict): The signed JSON object to check.
        signature_name (str): The name of the signature to check.
        verify_key (syutil.crypto.VerifyKey): The key to verify the signature.

    Raises:
        InvalidSignature: If the signature isn't valid
    """

    try:
        signatures = json_object['signatures']
    except KeyError:
        raise SignatureVerifyException("No signatures on this object")

    sig_descriptor = "%s:%s" % (signature_name, verify_key.alg)

    try:
        signature_b64 = signatures[sig_descriptor]
    except:
        raise SignatureVerifyException("Missing signature for %s" % sig_descriptor)

    try:
        signature = decode_base64(signature_b64)
    except:
        raise SignatureVerifyException(
            "Invalid signature base64 for %s" % signature_name)

    json_object_copy = {}
    json_object_copy.update(json_object)
    del json_object_copy["signatures"]

    message = encode_canonical_json(json_object_copy)

    try:
        verify_key.verify(message, signature)
    except:
        twisted.python.log.err()
        raise SignatureVerifyException(
            "Unable to verify signature for %s " % signature_name)
