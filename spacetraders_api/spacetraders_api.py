import logging
from spacetraders_api.rest_adapter import RestAdapter
from spacetraders_api.models import *


class SpaceTradersApi:
    def __init__(
        self,
        access_token,
        hostname: str = "api.spacetraders.io",
        ver: str = "v2",
        ssl_verify: bool = False,
        logger: logging.Logger = None,
        page_size: int = 20,
    ):
        self._rest_adapter = RestAdapter(
            hostname, access_token, ver, ssl_verify, logger
        )
        self._page_size = page_size

    def register_agent(
        self, callsign: str, faction="COSMIC", is_private=False
    ) -> RegistrationResult:
        result = self._rest_adapter.post(
            endpoint="/register",
            data={"symbol": callsign, "faction": faction},
            is_private=is_private,
        )

        return RegistrationResult(**result.data["data"])

    def get_my_agent(self) -> Agent:
        result = self._rest_adapter.get(endpoint=f"/my/agent")

        return Agent(**result.data["data"])

    def get_factions(self, page: int = 1, limit: int = 20) -> SearchResultPaginated:
        result = self._rest_adapter.get(
            endpoint="/factions", ep_params={"page": page, "limit": limit}
        )

        _result = SearchResultPaginated(
            data=[Faction(**faction) for faction in result.data["data"]],
            meta=MetaPagnaition(**result.data["meta"]),
        )

        return _result

    def get_contracts(self, page: int = 1, limit: int = 20) -> SearchResultPaginated:
        result = self._rest_adapter.get(
            endpoint="/my/contracts", ep_params={"page": page, "limit": limit}
        )

        _result = SearchResultPaginated(
            data=[Contract(**contract) for contract in result.data["data"]],
            meta=MetaPagnaition(**result.data["meta"]),
        )

        return _result

    def get_systems(self, page: int = 1, limit: int = 20) -> SearchResultPaginated:
        result = self._rest_adapter.get(
            endpoint="/systems", ep_params={"page": page, "limit": limit}
        )

        _result = SearchResultPaginated(
            data=[System(**system) for system in result.data["data"]],
            meta=MetaPagnaition(**result.data["meta"]),
        )

        return _result

    def get_system_waypoints(
        self, system_symbol: str, page: int = 1, limit: int = 20
    ) -> SearchResultPaginated:
        result = self._rest_adapter.get(
            endpoint=f"/systems/{system_symbol}/waypoints",
            ep_params={"page": page, "limit": limit},
        )

        _result = SearchResultPaginated(
            data=[SystemWaypoint(**waypoint) for waypoint in result.data["data"]],
            meta=MetaPagnaition(**result.data["meta"]),
        )

        return _result

    def accept_contract(self, contract_id: str) -> AcceptContractResult:
        result = self._rest_adapter.post(endpoint=f"/my/contracts/{contract_id}/accept")

        # TODO: Workaround for the accepted contract model
        return AcceptContractResult(
            contract=Contract(**result.data["data"]["contract"]),
            agent=Agent(**result.data["data"]["agent"]),
        )

    def find_shipyard(
        self, system_symbol: str, limit: int = 20, page: int = 1
    ) -> SearchResultPaginated:
        result = self._rest_adapter.get(
            endpoint=f"/systems/{system_symbol}/waypoints",
            ep_params={"traits": "SHIPYARD", "limit": limit},
        )

        _result = SearchResultPaginated(
            data=[SystemWaypoint(**waypoint) for waypoint in result.data["data"]],
            meta=MetaPagnaition(**result.data["meta"]),
        )

        return _result

    def get_available_ships_at_shipyard(
        self, system_symbol: str, shipyard_symbol: str
    ) -> ShipyardShip:
        # TODO: For some reason the endpoint is not working as expected and returning only 1 ship, not even in a list.
        result = self._rest_adapter.get(
            endpoint=f"/systems/{system_symbol}/waypoints/{shipyard_symbol}/shipyard",
        )
        return ShipyardShip(**result.data["data"])

    def buy_ship(self, ship_type: str, waypoint_symbol: str):
        result = self._rest_adapter.post(
            endpoint="/my/ships",
            data={"shipType": ship_type, "waypointSymbol": waypoint_symbol},
        )

        return result.data["data"]

    # 'https://api.spacetraders.io/v2/systems/:systemSymbol/waypoints/:waypointSymbol'
    def get_starting_waypoint(self, system_symbol: str, waypoint_symbol: str):
        result = self._rest_adapter.get(
            endpoint=f"/systems/{system_symbol}/waypoints/{waypoint_symbol}"
        )

        return result.data["data"]

    def get_my_ships(self) -> SearchResultPaginated:
        result = self._rest_adapter.get(endpoint="/my/ships")

        _result = SearchResultPaginated(
            data=[Ship(**ship) for ship in result.data["data"]],
            meta=MetaPagnaition(**result.data["meta"]),
        )

        return _result

    def navigate_ship_to(
        self, ship_symbol: str, waypoint_symbol: str
    ) -> ShipNavigationResponse:
        result = self._rest_adapter.post(
            endpoint=f"/my/ships/{ship_symbol}/navigate",
            data={"waypointSymbol": waypoint_symbol},
        )

        return ShipNavigationResponse(**result.data["data"])

    def set_ship_flight_mode(
        self, ship_symbol: str, flight_mode: str
    ) -> ChangeShipFlightModeResponse:
        result = self._rest_adapter.patch(
            endpoint=f"/my/ships/{ship_symbol}/nav",
            data={"flightMode": flight_mode},
        )

        return ChangeShipFlightModeResponse(**result.data["data"])

    def orbit_ship(self, ship_symbol: str) -> ChangeShipStatusResponse:
        result = self._rest_adapter.post(
            endpoint=f"/my/ships/{ship_symbol}/orbit",
        )

        return ChangeShipStatusResponse(**result.data["data"])

    def dock_ship(self, ship_symbol: str) -> ChangeShipStatusResponse:
        result = self._rest_adapter.post(
            endpoint=f"/my/ships/{ship_symbol}/dock",
        )

        return ChangeShipStatusResponse(**result.data["data"])

    def get_agents(self, page: int = 1, limit: int = 20) -> SearchResultPaginated:
        result = self._rest_adapter.get(
            endpoint="/agents", ep_params={"page": page, "limit": limit}
        )

        _result = SearchResultPaginated(
            data=[Agent(**agent) for agent in result.data["data"]],
            meta=MetaPagnaition(**result.data["meta"]),
        )

        return _result

    def get_public_agent(self, agent_symbol: str) -> Agent:
        result = self._rest_adapter.get(endpoint=f"/agents/{agent_symbol}")

        return Agent(**result.data["data"])

    def get_contract(self, contract_id: str) -> Contract:
        result = self._rest_adapter.get(endpoint=f"/my/contracts/{contract_id}")

        return Contract(**result.data["data"])

    def deliver_contract(
        self, contract_id: str, ship_symbol: str, trade_symbol: str, units: int
    ) -> DeliverCargoToContractResponse:
        result = self._rest_adapter.post(
            endpoint=f"/my/contracts/{contract_id}/deliver",
            data={
                "shipSymbol": ship_symbol,
                "tradeSymbol": trade_symbol,
                "units": units,
            },
        )

        return DeliverCargoToContractResponse(**result.data["data"])

    def fulfill_contract(self, contract_id: str) -> AcceptContractResult:
        result = self._rest_adapter.post(
            endpoint=f"/my/contracts/{contract_id}/fulfill",
        )

        return AcceptContractResult(**result.data["data"])

    def get_faction(self, faction_symbol: str) -> Faction:
        result = self._rest_adapter.get(endpoint=f"/factions/{faction_symbol}")

        return Faction(**result.data["data"])
