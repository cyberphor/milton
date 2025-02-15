"""Defines an User Proxy Agent."""

# Third party imports.
from autogen import UserProxyAgent


def user_proxy(name: str = "Victor"):
    return UserProxyAgent(
        name=name,
        code_execution_config={"use_docker": False}
    )
