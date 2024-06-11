from .common import pathlib
from ..enums import MIMETYPES


def get_mimetype(filename):
    return MIMETYPES.get(pathlib.Path(filename.lower()).suffix, 'application/octet-stream')
