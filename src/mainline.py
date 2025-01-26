from __future__ import annotations

import operator
from collections.abc import Sequence
from pathlib import Path
from typing import Annotated
from typing import TypedDict

from langchain.prompts import PromptTemplate
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph
from PIL import Image

from src.base.layout import Layout
from src.tools.models.layout_extractor import global_layout_extractor
from src.tools.pdf_reader import PDFReader


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.setitem]


class ChatChainModel:
    def __init__(
        self,
        document_path: Path,
        crop: tuple[int, int, int, int, int] | None = None,
        image_mode: bool = False,
    ):
        """
        A chat chain model that uses a layout to generate a conversation.

        :param document_path: The path to the document.
        :param crop: The crop for the document (for specific regions).
        :param image_mode: Select the mode of the document.
        """

        self.chain = self._build_chain()
        self.layout = self._build_document(document_path, crop, image_mode)

    def _build_document(
        self,
        document_path: Path,
        crop: tuple[int, int, int, int, int] | None = None,
        image_mode: bool = False,
    ) -> Layout:
        """
        Make layout of the image.

        :param document_path: The input image.
        :param crop: The crop for the document (for specific regions).
        :param image_mode: Select the mode of the document.
        :return: None
        """

        self.images: list[Image.Image] | None = None
        if not image_mode:
            self.images = self._read_document(document_path)
        else:
            self.images = [self._read_image(document_path)]

        if crop is not None and self.images is not None:
            self.images = [self.images[crop[0]].crop(crop[1:])]

        layout = Layout.from_dict(
            {
                "blocks": [
                    box.update({"page_number": page_number}) or box
                    for page_number, image in enumerate(self.images)
                    for box in global_layout_extractor.make_layout(image)
                ],
            },
        )
        return layout

    def _read_document(
        self,
        document_path: Path,
    ) -> list[Image.Image]:
        """
        Read the document.

        :param document_path: The path to the document.
        :return: None
        """

        self.pdf_reader = PDFReader(document_path)
        return self.pdf_reader.images

    def _read_image(
        self,
        document_path: Path,
    ) -> Image.Image:
        """
        Read the image.

        :param document_path: The path to the document.
        :return: None
        """

        return Image.open(document_path)

    def _build_chain(self) -> StateGraph:
        """
        Build the chain for the chat model.

        :return: The chain for the chat model.
        """

        chain = StateGraph(AgentState)

        chain.add_state("start")
        chain.add_state("end")

        chain.add_edge(
            "start",
            "end",
            PromptTemplate("Ask for information about document", layout=self.layout),
        )

        return chain

    def get_layout(self) -> Layout:
        """
        Get the layout of the document.

        :return: The layout of the document.
        """

        return self.layout

    def handle_prompt(self, prompt: str) -> str:
        """
        Handle the prompt and return the response.

        :param prompt: The prompt to handle.
        :return: The response.
        """

        result = self.chain.generate_conversation()

        assert isinstance(
            result,
            str,
        ), "Something went wrong with the conversation: chain returned a non-string result."

        return result


class ExtractionChainModel:
    def __init__(
        self,
        layout: Layout,
    ):
        """
        An extraction chain model that uses a layout to extract information from the document.

        :param layout: The layout of the document.
        """

        self.chain = self._build_chain()
        self.layout = layout

    def _build_chain(self) -> StateGraph:
        """
        Build the chain for the extraction model.

        :return: The chain for the extraction model.
        """

        chain = StateGraph()

        chain.add_state("start")
        chain.add_state("end")

        chain.add_edge(
            "start",
            "end",
            PromptTemplate("Ask for information about document", layout=self.layout),
        )

        return chain

    def extract_information(self) -> str:
        """
        Extract information based on the layout.

        :return: The extracted information.
        """

        result = self.chain.generate_conversation()

        assert isinstance(
            result,
            str,
        ), "Something went wrong with the conversation: chain returned a non-string result."

        return result
