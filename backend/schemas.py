from pydantic import BaseModel
from typing import Literal


class Station(BaseModel):
    id: int
    name: str
    neighbourhood: str
    pm25: float
    status: Literal["Online", "Offline"]
    lat: float
    lng: float


class StationsResponse(BaseModel):
    data_type: str
    count: int
    stations: list[Station]

class SummaryResponse(BaseModel):
    data_type: str
    total_stations: int
    online_stations: int
    offline_stations: int
    average_pm25: float

class HistoryReading(BaseModel):
    day: str
    pm25: float


class HistoryResponse(BaseModel):
    data_type: str
    time_range: str
    count: int
    readings: list[HistoryReading]