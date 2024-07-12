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

    def accept_contract(self, contract_id: str) -> Contract:
        result = self._rest_adapter.post(endpoint=f"/my/contracts/{contract_id}/accept")

        # TODO: Workaround for the accepted contract model
        return result.data
