"""Defines a tool."""

# Standard library imports.
from io import BytesIO
from typing import Annotated

# Third party imports.
import streamlit
from docx import Document


def memo_maker(
        file_name: Annotated[str, "The file name of the memo."],
        body: Annotated[str, "The body of the memo."]
    ):
    """Used to make memorandums."""
    bytes = BytesIO()
    document = Document()
    document.add_paragraph(body)
    document.save(bytes)
    streamlit.success("Done!")
    return streamlit.download_button(
        label="Download",
        data=bytes.getvalue(),
        file_name=f"{file_name}.docx",
        mime="docx"
    )
