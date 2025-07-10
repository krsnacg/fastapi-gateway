import yaml
import json
from app.models import ConfigRoute
from typing import Any

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

def load_routes_config(path: str = "../configuration/routes.yml") -> list[ConfigRoute]:
    """
    Load the routes configuration from a YAML file.
        
    :param path: Path to the YAML configuration file.
    :return: List of routes as ConfigRoute objects.
    """
    with open(path, "r") as stream:
        config = yaml.safe_load(stream)
        
    config_list = []
            
    for route in config.get("routes", []):
        # Convert each route to a ConfigRoute object
        route["auth_required"] = (route.pop("auth-required", False) if "auth-required" in route else False)
        route["predicate"] = route["predicate"].replace("**", "")
        config_list.append(ConfigRoute(**route))
            
    return config_list

def load_port_config(path: str = "../configuration/routes.yml") -> int:
        """
        Load the port configuration
        """
        with open(path, "r") as stream:
            config = json.load(stream)
        
        return config.get("server.port", 8000)  # Default to 8000 if not specified