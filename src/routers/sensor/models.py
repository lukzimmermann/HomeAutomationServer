from typing_extensions import Unpack
from pydantic import BaseModel, ConfigDict


class Power(BaseModel):
    name: str
    value: float
    unit: str

class ServerPower(BaseModel):
    router: Power
    k3s: Power
    server: Power
    switch: Power