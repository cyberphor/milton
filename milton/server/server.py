"""Defines a server."""

# Standard library imports.
import asyncio
from httpx import Client
from os import environ
from pathlib import Path
from typing import Any, Dict, List
from warnings import filterwarnings

# Supress warnings about flaml.automl not being installed.
filterwarnings("ignore", category=UserWarning, module="flaml")

# Third party imports.
from autogen import filter_config, register_function
import streamlit

# Local imports.
from milton.agents import boss, employee, user_proxy
from milton.core import get_logger
from milton.tools import memo_maker


class CustomHttpClient(Client):
    def __init__(
        self,
        cert_file: Path,
        key_file: Path,
        verify: bool
    ):
        super().__init__(
            cert=(cert_file, key_file),
            verify=verify
        )

    def __deepcopy__(self, memo):
        return self


class Server:
    """Responds to requests.
        
    Args:
        llm_tag. str.
        tools. A list of functions.
        message_client.

    """
    def __init__(
        self,
        name: str,
        llm_tag: str,
        cert_file_path: Path = None,
        key_file_path: Path = None,
    ):
        # Init a logger.
        self.logger = get_logger(name)

        # Init a proxy agent for the user. 
        self.user_proxy = user_proxy()

        # Set the certificate file paths needed for an HTTP client.
        self.__cert_file_path = cert_file_path
        self.__key_file_path = key_file_path

        # Parse the LLM config provided. 
        self.llm_config = self.__get_llm_config(llm_tag)[0]

        # Init a boss agent. 
        self.boss = boss(self.llm_config)

        # Init an employee agent.
        self.employee = employee(self.llm_config)

        # Register tools for the agents to use.
        self.__register_tools([memo_maker])

    def __get_http_client(self):
        """
        Returns an custom HTTP client.
        """
        return CustomHttpClient(
            cert_file=self.__cert_file_path,
            key_file=self.__key_file_path,
            verify=False,
        )

    def __get_llm_config(self, llm_tag: str) -> Dict[str, Any]:
        """
        Returns an LLM config.
        """
        match llm_tag:
            case "camogpt":
                if "CAMOGPT_API_KEY" not in environ:
                    raise RuntimeError("the 'CAMOGPT_API_KEY' environment variable is not set")
                self.logger.debug("the 'CAMOGPT_API_KEY' environment variable is set")
                base_url = "https://omni.army.mil/camogptapi/v2"
                http_client = self.__get_http_client()
                api_key = environ["CAMOGPT_API_KEY"]
            case _:
                if "OPENAI_API_KEY" not in environ:
                    raise RuntimeError("the 'OPENAI_API_KEY' environment variable is not set")
                self.logger.debug("the 'OPENAI_API_KEY' environment variable is set")
                base_url = None
                http_client = None
                api_key = environ["OPENAI_API_KEY"]
        
        return filter_config(
            filter_dict={"tags": [llm_tag]},
            config_list=[
                {
                    "tags": ["camogpt"],
                    "api_key": api_key,
                    "model": "",
                    "cache_seed": None,
                    "base_url": base_url,
                    "http_client": http_client,
                    "api_rate_limit": 1.0
                },
                {
                    "tags": ["openai", "gpt-4o"],
                    "api_key": api_key,
                    "model": "gpt-4o",
                    "cache_seed": None,
                },
            ],
        )

    def __register_tools(self, tools) -> None:
        """Registers tools for Milton to use.
        
        Returns:
            bool: True if all tool registrations were successful. False if all tool registrations were not successful.
        
        """
        try:
            for tool in tools:
                self.logger.debug(f"registering '{tool.__name__}' as a tool for Milton to use")
                register_function(
                    tool,
                    caller=self.boss,
                    executor=self.employee,
                    description=tool.__doc__,
                )
        except Exception as e:
            self.logger.error(e)
            raise RuntimeError(e)

    def on_click(self):
        with streamlit.spinner("Standby..."):
            self.user_proxy.initiate_chats(
                [
                    {
                        "chat_id": 1,
                        "sender": self.boss,
                        "recipient": self.employee,
                        "message": f"Write a short memo about {streamlit.session_state.subject}.",
                        "max_turns": 2,
                    }
                ]
            )

    def Start(self):
        """
        Starts the Milton server.
        """
        streamlit.set_page_config(page_title="Milton", page_icon=":shark:")
        with streamlit.container():
            with streamlit.form(key="form"):
                streamlit.text_input(label="Subject", key="subject")
                streamlit.form_submit_button(label="Submit", on_click=self.on_click)
            streamlit.stop()
