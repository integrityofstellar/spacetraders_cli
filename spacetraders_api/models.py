import os
import datetime
from typing import List, Dict, Optional, Union, TypeVar
from requests.structures import CaseInsensitiveDict
from spacetraders_api.exceptions import SpaceTradersApiException
from pydantic import BaseModel

Model = TypeVar("Model", covariant=True)


class Result:
    def __init__(
        self,
        status_code: int,
        headers: CaseInsensitiveDict,
        message: str = "",
        data: List[Dict] = None,
    ):
        """
        Result returned from low-level RestAdapter
        :param status_code: Standard HTTP Status code
        :param message: Human readable result
        :param data: Python List of Dictionaries (or maybe just a single Dictionary on error)
        """
        self.status_code = int(status_code)
        self.headers = headers
        self.message = str(message)
        self.data = data if data else []


class Reference(BaseModel):
    symbol: str


class MetaPagnaition(BaseModel):
    total: int
    page: int
    limit: int


class SearchResultPaginated(BaseModel):
    data: list
    meta: MetaPagnaition


class Waypoint(BaseModel):
    symbol: str
    type: str
    x: int
    y: int
    orbitals: list[Reference]


class Trait(BaseModel):
    symbol: str
    name: str
    description: str


class System(BaseModel):
    symbol: str
    sectorSymbol: str
    type: str
    x: int
    y: int
    waypoints: list[Waypoint]
    factions: list[Reference]


class WaypointChart(BaseModel):
    submittedBy: str
    submittedOn: datetime.datetime


class SystemWaypoint(BaseModel):
    systemSymbol: str
    symbol: str
    type: str
    x: int
    y: int
    orbitals: list
    traits: list[Trait]
    modifiers: list
    chart: WaypointChart
    faction: Reference
    isUnderConstruction: bool


class Agent(BaseModel):
    accountId: str
    symbol: str
    headquarters: str
    credits: int
    startingFaction: str
    shipCount: int


class Faction(BaseModel):
    symbol: str
    name: str
    description: str
    headquarters: str
    traits: list[Trait]
    isRecruiting: bool


class TermPayment(BaseModel):
    onAccepted: int
    onFulfilled: int


class DeliverTermObject(BaseModel):
    tradeSymbol: str
    destinationSymbol: str
    unitsRequired: int
    unitsFulfilled: int


class Term(BaseModel):
    deadline: str
    payment: TermPayment
    deliver: list[DeliverTermObject]


class Contract(BaseModel):
    id: str
    factionSymbol: str
    type: str
    terms: Term
    accepted: bool
    fulfilled: bool
    expiration: str
    deadlineToAccept: str


class Token(BaseModel):
    token: str


class RoutePoint(BaseModel):
    symbol: str
    type: str
    systemSymbol: str
    x: int
    y: int


class ShipRoute(BaseModel):
    origin: RoutePoint
    destination: RoutePoint
    arrival: datetime.datetime
    departureTime: datetime.datetime


class ShipNav(BaseModel):
    systemSymbol: str
    waypointSymbol: str
    route: ShipRoute
    status: str
    flightMode: str


class ShipCrew(BaseModel):
    current: int
    capacity: int
    required: int
    rotation: str
    morale: int
    wages: int


class ShipFuelConsumed(BaseModel):
    amount: int
    timestamp: datetime.datetime


class ShipFuel(BaseModel):
    current: int
    capacity: int
    consumed: ShipFuelConsumed


class ShipCooldown(BaseModel):
    shipSymbol: str
    totalSeconds: int
    remainingSeconds: int


class PowerAndCrewRequirements(BaseModel):
    power: int
    crew: int


class ShipFrame(BaseModel):
    symbol: str
    name: str
    description: str
    moduleSlots: int
    mountingPoints: int
    fuelCapacity: int
    condition: float
    integrity: int
    requirements: PowerAndCrewRequirements


class ShipReactorRequirements(BaseModel):
    crew: int


class ShipReactor(BaseModel):
    symbol: str
    name: str
    description: str
    condition: int
    integrity: int
    powerOutput: int
    requirements: ShipReactorRequirements


class ShipEngine(BaseModel):
    symbol: str
    name: str
    description: str
    condition: int
    integrity: int
    speed: int
    requirements: PowerAndCrewRequirements


class ShipModuleRequirements(BaseModel):
    crew: int
    power: int
    slots: int


class ShipModule(BaseModel):
    symbol: str
    name: str
    description: str
    capacity: Optional[int]
    requirements: ShipModuleRequirements


class ShipMount(BaseModel):
    symbol: str
    name: str
    description: str
    strength: int
    deposits: List[str] = []
    requirements: PowerAndCrewRequirements


class ShipRegistration(BaseModel):
    name: str
    factionSymbol: str
    role: str


class ShipCargo(BaseModel):
    capacity: int
    units: int
    inventory: List[Dict] = []


class Ship(BaseModel):
    symbol: str
    nav: ShipNav
    crew: ShipCrew
    fuel: ShipFuel
    cooldown: ShipCooldown
    frame: ShipFrame
    reactor: ShipReactor
    engine: ShipEngine
    modules: List[Dict]
    mounts: List[Dict]
    registration: ShipRegistration
    cargo: ShipCargo


class RegistrationResult(BaseModel):
    token: str
    agent: Agent
    contract: Contract
    faction: Faction
    ship: Ship


class ShipTypeReference(BaseModel):
    type: str


class ShipyardShip(BaseModel):
    symbol: str
    shipTypes: list[ShipTypeReference]
    modificationsFee: int


class AcceptContractResult(BaseModel):
    contract: Contract
    agent: Agent


class ChangeShipStatusResponse(BaseModel):
    systemSymbol: str
    waypointSymbol: str
    route: ShipRoute
    status: str
    flightMode: str


class ChangeShipFlightModeResponse(BaseModel):
    systemSymbol: str
    waypointSymbol: str
    route: ShipRoute
    status: str
    flightMode: str


class Event(BaseModel):
    type: str
    symbol: str
    component: str
    name: str
    description: str


class ShipNavigationResponse(BaseModel):
    nav: ShipNav
    fuel: ShipFuel
    events: List[Event]
