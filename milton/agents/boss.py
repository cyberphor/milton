"""Defines an agent."""

# Third party imports.
from autogen import ConversableAgent


def boss(llm_config):
    return ConversableAgent(
        name="Bill",
        system_message="You are responsible for ensuring your staff of writers produce memorandums in accordance with Army Regulation 25-50.",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
