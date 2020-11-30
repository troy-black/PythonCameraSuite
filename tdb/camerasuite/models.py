from typing import List

from pydantic import BaseModel


class ZipFileRequest(BaseModel):
    files: List[str]
