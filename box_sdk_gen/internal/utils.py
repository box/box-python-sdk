import base64
import datetime
import hashlib
import os
import re
import shutil
import uuid
import time
import hmac
from random import uniform
from enum import Enum
from io import SEEK_CUR, SEEK_END, SEEK_SET, BufferedIOBase, BytesIO
from typing import Any, Callable, Dict, Iterable, Optional, TypeVar, BinaryIO

from abc import abstractmethod
from typing import Any

try:
    import jwt
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
except ImportError:
    jwt, default_backend, serialization = None, None, None

from .base_object import BaseObject
from ..serialization.json import sd_to_json, sanitized_value
from ..serialization.json import serialize
from .null_value import null

ByteStream = BufferedIOBase
OutputStream = BinaryIO
Buffer = bytes


class ResponseByteStream(ByteStream):
    def __init__(self, request_iterator):
        self._iterator = request_iterator
        self._buffer = b''
        self._position = 0
        self._eos = False

    def _read_from_iterator(self, size):
        """
        Read up to `size` bytes from the iterator into the buffer
        :param size: Number of bytes to read. If None, read the entire stream.
        """
        if self._eos:
            return

        while len(self._buffer) < size:
            try:
                chunk = next(self._iterator)
                self._buffer += chunk
            except StopIteration:
                self._eos = True
                break

    def tell(self):
        """
        Returns the current position in the stream
        :return:
        """
        return self._position

    def read(self, size=None):
        """
        Reads up to `size` bytes from the stream
        :param size: Read up to `size` bytes from the stream. If None read the entire stream.
        :return: Bytes read from the stream
        """
        if size is None:
            # Read everything remaining in the stream.
            result = self._buffer + b''.join(self._iterator)
            self._buffer = b''
            self._position += len(result)
            self._eos = True
            return result

        self._read_from_iterator(size)
        result = self._buffer[:size]
        self._buffer = self._buffer[size:]
        self._position += len(result)
        return result

    def seek(self, position, whence=SEEK_SET):
        """
        Move the stream to given position
        :param position: Position to move to
        :param whence: One of SEEK_SET = 0, SEEK_CUR = 1 or SEEK_END = 2
        :return: The new position in the stream
        """
        if whence == SEEK_SET:
            if position < self._position:
                raise ValueError('Cannot seek backwards in a stream')
            self.read(position - self._position)
        elif whence == SEEK_CUR:
            self.read(position)
        elif whence == SEEK_END:
            raise NotImplementedError('SEEK_END is not supported for streams')
        else:
            raise ValueError('Invalid value for `whence`')

        return self._position


def get_env_var(name: str) -> str:
    return os.getenv(name)


def get_uuid() -> str:
    return str(uuid.uuid1())


def decode_base_64(value: str) -> str:
    return base64.b64decode(value).decode()


def generate_byte_buffer(size: int) -> Buffer:
    return Buffer(os.urandom(size))


def generate_byte_stream_from_buffer(buffer: Buffer) -> ByteStream:
    return BytesIO(buffer)


def generate_byte_stream(size: int) -> ByteStream:
    return BytesIO(os.urandom(size))


def buffer_equals(buffer1: Buffer, buffer2: Buffer) -> bool:
    return buffer1 == buffer2


def buffer_length(buffer: Buffer) -> int:
    return len(buffer)


def decode_base_64_byte_stream(value: str) -> ByteStream:
    return BytesIO(base64.b64decode(value))


def string_to_byte_stream(value: str) -> ByteStream:
    return BytesIO(bytes(value, 'utf-8'))


def read_byte_stream(byte_stream: ByteStream) -> Buffer:
    return Buffer(byte_stream.read())


def write_input_stream_to_output_stream(
    input_stream: ByteStream, output_stream: OutputStream
):
    shutil.copyfileobj(input_stream, output_stream)


def get_file_output_stream(file_path: str) -> OutputStream:
    return open(file_path, 'wb')


def close_file_output_stream(file_output_stream: OutputStream):
    file_output_stream.close()


def read_buffer_from_file(path: str) -> bytes:
    with open(path, 'rb') as file:
        return file.read()


def prepare_params(map: Dict[str, Optional[str]]) -> Dict[str, str]:
    return {k: v for k, v in map.items() if v is not None}


def to_string(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime.datetime):
        return date_time_to_string(value)
    if isinstance(value, datetime.date):
        return date_to_string(value)
    if (
        isinstance(value, BaseObject)
        or isinstance(value, list)
        and len(value) >= 1
        and isinstance(value[0], BaseObject)
    ):
        return ''.join(sd_to_json(serialize(value)).split())
    if isinstance(value, list):
        return ','.join(map(to_string, value))
    if isinstance(value, Enum):
        return value.value
    return str(value)


class HashName(str, Enum):
    SHA1 = 'sha1'


class Hash:
    def __init__(self, algorithm: HashName):
        self.algorithm = algorithm
        self.hash = hashlib.sha1()

    def update_hash(self, data: Buffer):
        self.hash.update(data)

    def digest_hash(self, encoding):
        return base64.b64encode(self.hash.digest()).decode("utf-8")


def hex_to_base_64(data: hex):
    return base64.b64encode(bytes.fromhex(data)).decode()


T = TypeVar('T')
Iterator = Iterable[T]
Accumulator = TypeVar('Accumulator')


def iterate_chunks(
    stream: ByteStream, chunk_size: int, file_size: int
) -> Iterable[ByteStream]:
    stream_is_finished = False
    while not stream_is_finished:
        copied_length = 0
        chunk = b''
        while copied_length < chunk_size:
            bytes_read = stream.read(chunk_size - copied_length)
            if bytes_read is None:
                # stream returns none when no bytes are ready currently but there are
                # potentially more bytes in the stream to be read.
                continue
            if not bytes_read:
                # stream is exhausted.
                stream_is_finished = True
                break
            chunk += bytes_read
            copied_length += len(bytes_read)
        if chunk:
            yield BytesIO(chunk)


def reduce_iterator(
    iterator: Iterator,
    reducer: Callable[[Accumulator, T], Accumulator],
    initial_value: Accumulator,
) -> Accumulator:
    result = initial_value

    for item in iterator:
        result = reducer(result, item)

    return result


def read_text_from_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()


def is_browser() -> bool:
    return False


def get_epoch_time_in_seconds() -> int:
    return int(time.time())


def get_value_from_object_raw_data(obj: BaseObject, key: str) -> Any:
    keys = key.split('.')
    value: dict = obj.raw_data
    for k in keys:
        value = value.get(k, {})
    return value


class PrivateKeyDecryptor:
    """Class used for private key decryption in JWT auth."""

    @abstractmethod
    def decrypt_private_key(self, encryptedPrivateKey: str, passphrase: str) -> Any:
        """Decrypts private key using a passphrase."""
        pass


class DefaultPrivateKeyDecryptor(PrivateKeyDecryptor):
    def decrypt_private_key(self, encryptedPrivateKey: str, passphrase: str) -> Any:
        if default_backend is None or serialization is None:
            raise ImportError(
                'Missing `cryptography` dependency. `cryptography` library is required to create JWT assertion.'
            )
        encoded_private_key = encode_str_ascii_or_raise(encryptedPrivateKey)
        encoded_passphrase = encode_str_ascii_or_raise(passphrase)

        return serialization.load_pem_private_key(
            encoded_private_key,
            password=encoded_passphrase,
            backend=default_backend(),
        )


class JwtAlgorithm(str, Enum):
    HS256 = 'HS256'
    HS384 = 'HS384'
    HS512 = 'HS512'
    RS256 = 'RS256'
    RS384 = 'RS384'
    RS512 = 'RS512'
    ES256 = 'ES256'
    ES384 = 'ES384'
    ES512 = 'ES512'
    PS256 = 'PS256'
    PS384 = 'PS384'
    PS512 = 'PS512'
    none = 'none'


class JwtSignOptions(BaseObject):
    def __init__(
        self,
        algorithm: JwtAlgorithm,
        headers: Dict[str, str] = None,
        audience: Optional[str] = None,
        issuer: Optional[str] = None,
        subject: Optional[str] = None,
        jwtid: Optional[str] = None,
        keyid: Optional[str] = None,
        private_key_decryptor: Optional[PrivateKeyDecryptor] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if headers is None:
            headers = {}
        self.algorithm = algorithm
        self.headers = headers
        self.audience = audience
        self.issuer = issuer
        self.subject = subject
        self.jwtid = jwtid
        self.keyid = keyid
        self.private_key_decryptor = (
            private_key_decryptor
            if private_key_decryptor is not None
            else DefaultPrivateKeyDecryptor()
        )


class JwtKey(BaseObject):
    def __init__(self, key: str, passphrase: str, **kwargs):
        super().__init__(**kwargs)
        self.key = key
        self.passphrase = passphrase


def encode_str_ascii_or_raise(passphrase: str) -> bytes:
    try:
        return passphrase.encode('ascii')
    except UnicodeError as unicode_error:
        raise TypeError(
            "private_key and private_key_passphrase must contain binary data (bytes/str), not a text/unicode string"
        ) from unicode_error


def create_jwt_assertion(claims: dict, key: JwtKey, options: JwtSignOptions) -> str:
    if jwt is None:
        raise ImportError(
            'Missing `PyJWT` dependency. `PyJWT` library is required to create JWT assertion.'
        )
    return jwt.encode(
        {
            'iss': options.issuer,
            'sub': options.subject,
            'box_sub_type': claims['box_sub_type'],
            'aud': options.audience,
            'jti': options.jwtid,
            'exp': claims['exp'],
        },
        options.private_key_decryptor.decrypt_private_key(key.key, key.passphrase),
        algorithm=options.algorithm,
        headers={'kid': options.keyid},
    )


Date = datetime.date
DateTime = datetime.datetime


def date_to_string(date: Date) -> str:
    return date.isoformat()


def date_from_string(date: str) -> Date:
    return Date.fromisoformat(date)


def date_time_to_string(date_time: DateTime) -> str:
    return date_time.isoformat().replace('+00:00', 'Z')


def date_time_from_string(date_time: str) -> DateTime:
    return DateTime.fromisoformat(date_time.replace('Z', '+00:00'))


def date_time_to_epoch_seconds(date_time: DateTime) -> int:
    return int(date_time.timestamp())


def epoch_seconds_to_date_time(epoch_seconds: int) -> DateTime:
    return DateTime.fromtimestamp(epoch_seconds, datetime.timezone.utc)


def delay_in_seconds(seconds: int):
    time.sleep(seconds)


def create_null():
    return null


def escape_unicode(value: str) -> str:
    def replace_char(match):
        char = match.group(0)
        code_point = ord(char)
        if char == '\n':
            return '\\n'
        elif char == '\r':
            return '\\r'
        elif char == '\t':
            return '\\t'
        elif code_point <= 0xFFFF:  # Basic Multilingual Plane (BMP)
            return f"\\u{code_point:04x}"
        else:  # Supplementary Plane (Surrogate Pair)
            code_point -= 0x10000
            high_surrogate = 0xD800 + (code_point >> 10)
            low_surrogate = 0xDC00 + (code_point & 0x3FF)
            return f"\\u{high_surrogate:04x}\\u{low_surrogate:04x}"

    # Replace any backslashes that are NOT part of a \/ with double backslash
    temp = re.sub(r'\\(?!/)', r'\\\\', value)

    # Match special characters, non-ASCII characters
    return re.sub(r'[^\x20-\x7e]|[\n\r\t]', replace_char, temp)


def compute_webhook_signature(
    body: str,
    headers: Dict[str, str],
    signature_key: str,
    escape_body: Optional[bool] = False,
) -> Optional[str]:
    """
    Computes the Hmac for the webhook notification given one signature key.

    :param body:
        The encoded webhook body.
    :param headers:
        The headers for the `Webhook` notification.
    :param signature_key:
        The `Webhook` signature key for this application.
    :param escape_body:
        Indicates if payload should be escaped or left as is.
    :return:
        An Hmac signature.
    """
    if signature_key is None:
        return None
    if headers.get('box-signature-version') != '1':
        return None
    if headers.get('box-signature-algorithm') != 'HmacSHA256':
        return None

    encoded_body = (escape_unicode(body) if escape_body else body).encode('utf-8')
    encoded_signature_key = signature_key.encode('utf-8')
    encoded_delivery_time_stamp = headers.get('box-delivery-timestamp').encode('utf-8')
    new_hmac = hmac.new(encoded_signature_key, digestmod=hashlib.sha256)
    new_hmac.update(encoded_body)
    new_hmac.update(encoded_delivery_time_stamp)
    signature = base64.b64encode(new_hmac.digest()).decode()
    return signature


def compare_signatures(
    expected_signature: Optional[str], received_signature: Optional[str]
) -> bool:
    if not expected_signature or not received_signature:
        return False
    if len(expected_signature) != len(received_signature):
        return False
    return hmac.compare_digest(expected_signature, received_signature)


def random(min: float, max: float) -> float:
    return uniform(min, max)


def sanitize_map(
    dictionary: Dict[str, str], keys_to_sanitize: Dict[str, str]
) -> Dict[str, str]:
    return {
        k: sanitized_value() if k.lower() in keys_to_sanitize else v
        for k, v in dictionary.items()
    }
