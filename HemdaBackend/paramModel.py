from dataclasses import dataclass
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional

@dataclass
class SystemModel:
    postgresql: dict

@dataclass
class GeneralModel:
    port: int
    threadSleepTime: float

@dataclass
class ParamsModel:
    general: GeneralModel
    system: SystemModel