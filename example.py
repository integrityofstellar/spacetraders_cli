from spacetraders_api.spacetraders_api import SpaceTradersApi
from rich.console import Console

console = Console()

with open("secrets", "r") as file:
    token = file.read()

api = SpaceTradersApi(
    access_token=token,
)

register_result = api.register_agent("test")
console.print(register_result.token)

my_agent = api.get_my_agent()
console.print(my_agent)

factions = api.get_factions()
console.print(factions)

contracts = api.get_contracts()
console.print(contracts)

systems = api.get_systems(page=50)
console.print(systems)

system_waypoints = api.get_system_waypoints("X1-RR47")
console.print(system_waypoints)
