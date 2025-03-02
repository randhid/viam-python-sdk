from typing_extensions import Self

from grpclib.client import Channel

from viam.rpc.dial import DialOptions, _dial_app, _get_access_token
from viam import logging
from viam.app.data.client import DataClient

LOGGER = logging.getLogger(__name__)


class AppClient:
    """gRPC client for all communication and interaction with app.

    Use create() to instantiate an AppClient::

        AppClient.create(...)
    """

    @classmethod
    async def create(cls, dial_options: DialOptions) -> Self:
        """
        Create an app client that establishes a connection to app.viam.com.

        Args:
            dial_options (DialOptions): Required information for authorization and connection to app, creds and auth_entity are necessary.

        Returns:
            Self: the AppClient.
        """
        self = cls()
        self._channel = await _dial_app(dial_options)
        access_token = await _get_access_token(self._channel, dial_options.auth_entity, dial_options)
        self._metadata = {"authorization": f"Bearer {access_token}"}
        return self

    _channel: Channel
    _metadata: str
    _closed: bool = False

    @property
    def data_client(self) -> DataClient:
        return DataClient(self._channel, self._metadata)

    async def close(self):
        raise NotImplementedError()
