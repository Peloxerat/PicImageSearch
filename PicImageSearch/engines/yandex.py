from pathlib import Path
from typing import Any, Optional, Union

from ..model import YandexResponse
from ..utils import read_file
from .base import BaseSearchEngine


class Yandex(BaseSearchEngine):
    """API client for the Yandex reverse image search engine.

    This class provides an interface to perform reverse image searches using Yandex's service.
    It supports searching by both image URL and local image file upload.

    Attributes:
        base_url: The base URL for Yandex image search service.

    Note:
        - The service might be affected by regional restrictions.
        - Search results may vary based on the user's location and Yandex's algorithms.
    """

    def __init__(
        self,
        base_url: str = "https://yandex.com",
        **request_kwargs: Any,
    ):
        """Initializes a Yandex API client with specified configurations.

        Args:
            base_url: The base URL for Yandex searches.
            **request_kwargs: Additional arguments for network requests.
        """
        base_url = f"{base_url}/images/search"
        super().__init__(base_url, **request_kwargs)

    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        **kwargs: Any,
    ) -> YandexResponse:
        """Performs a reverse image search on Yandex.

        This method supports two ways of searching:
        1. Search by image URL
        2. Search by uploading a local image file

        Args:
            url: URL of the image to search.
            file: Local image file, can be a path string, bytes data, or Path object.
            **kwargs: Additional arguments passed to the parent class.

        Returns:
            YandexResponse: An object containing:
                - Search results and metadata
                - The final search URL used by Yandex

        Raises:
            ValueError: If neither 'url' nor 'file' is provided.

        Note:
            - Only one of 'url' or 'file' should be provided.
            - When using file upload, the image will be sent to Yandex's servers.
            - The search process involves standard Yandex parameters like 'rpt' and 'cbir_page'.
        """
        await super().search(url, file, **kwargs)

        params = {"rpt": "imageview", "cbir_page": "sites"}

        if url:
            params["url"] = url
            resp = await self._make_request(method="get", params=params)
        else:
            files = {"upfile": read_file(file)}
            resp = await self._make_request(
                method="post",
                params=params,
                data={"prg": 1},
                files=files,
            )

        return YandexResponse(resp.text, resp.url)
