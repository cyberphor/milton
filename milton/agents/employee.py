"""Defines an agent."""

# Third party imports.
from autogen import ConversableAgent


def employee(llm_config):
    return ConversableAgent(
        name="Milton",
        system_message="You create memorandums.",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )   
