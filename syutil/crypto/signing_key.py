from syutil.base64util import encode_base64, decode_base64
import nacl.signing

NACL_ED25519 = "ed25519"

def generate_singing_key(version):
    """Generate a new signing key
    Args:
        version (str): Identifies this key out the keys for this entity.
    Returns:
        A SigningKey object.
    """
    key = nacl.signing.SigningKey.generate()
    key.version = version
    key.alg = NACL_ED25519
    return key


def decode_signing_key_base64(algorithm, version, key_base64):
    """Decode a base64 encoded signing key
    Args:
        algorithm (str): The algorithm the key is for (currently "ed25519").
        version (str): Identifies this key out of the keys for this entity.
        key_base64 (str): Base64 encoded bytes of the key.
    Returns:
        A SigningKey object.
    """
    if algorithm == NACL_ED25519:
        key_bytes = decode_base64(key_base64)
        key = nacl.signing.SigningKey(key_bytes)
        key.version = version
        key.alg = NACL_ED25519
        return key
    else:
        raise ValueError("Unsupported algorithm %s" % (algorithm,))


def encode_signing_key_base64(key):
    """Encode a signing key as base64
    Args:
        key (SigningKey): A signing key to encode.
    Returns:
        base64 encoded string.
    """
    return encode_base64(key.encode())


def read_signing_keys(stream):
    """Reads a list of keys from a stream
    Args:
        stream : A stream to iterate for keys.
    Returns:
        list of SigningKey objects.
    """
    keys = []
    for line in stream:
        algorithm, version, key_base64 = line.split()
        keys.append(decode_signing_key_base64(algorithm, version, key_base64))
    return keys


def write_signing_keys(stream, keys):
    """Writes a list of keys to a stream.
    Args:
        stream: Stream to write keys to.
        keys: List of SigningKey objects.
    """
    for key in keys:
        key_base64 = encode_signing_key_base64(key)
        stream.write("%s %s %s\n" % (key.alg, key.version, key_base64,))

