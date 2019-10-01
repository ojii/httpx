import typing
from types import TracebackType

from ..config import CertTypes, TimeoutTypes, VerifyTypes
from ..models import (
    AsyncRequest,
    AsyncRequestData,
    AsyncResponse,
    HeaderTypes,
    QueryParamTypes,
    Request,
    RequestData,
    Response,
    URLTypes,
)


class AsyncDispatcher:
    """
    Base class for async dispatcher classes, that handle sending the request.

    Stubs out the interface, as well as providing a `.request()` convenience
    implementation, to make it easy to use or test stand-alone dispatchers,
    without requiring a complete `Client` instance.
    """

    async def request(
        self,
        method: str,
        url: URLTypes,
        *,
        data: AsyncRequestData = b"",
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        verify: typing.Optional[VerifyTypes] = None,
        cert: typing.Optional[CertTypes] = None,
        timeout: typing.Optional[TimeoutTypes] = None,
    ) -> AsyncResponse:
        request = AsyncRequest(method, url, data=data, params=params, headers=headers)
        return await self.send(request, verify=verify, cert=cert, timeout=timeout)

    async def send(
        self,
        request: AsyncRequest,
        verify: typing.Optional[VerifyTypes] = None,
        cert: typing.Optional[CertTypes] = None,
        timeout: typing.Optional[TimeoutTypes] = None,
    ) -> AsyncResponse:
        raise NotImplementedError()  # pragma: nocover

    async def close(self) -> None:
        pass  # pragma: nocover

    async def __aenter__(self) -> "AsyncDispatcher":
        return self

    async def __aexit__(
        self,
        exc_type: typing.Type[BaseException] = None,
        exc_value: typing.Optional[BaseException] = None,
        traceback: typing.Optional[TracebackType] = None,
    ) -> None:
        await self.close()


class Dispatcher:
    """
    Base class for synchronous dispatcher classes, that handle sending the request.

    Stubs out the interface, as well as providing a `.request()` convenience
    implementation, to make it easy to use or test stand-alone dispatchers,
    without requiring a complete `Client` instance.
    """

    def request(
        self,
        method: str,
        url: URLTypes,
        *,
        data: RequestData = b"",
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        verify: typing.Optional[VerifyTypes] = None,
        cert: typing.Optional[CertTypes] = None,
        timeout: typing.Optional[TimeoutTypes] = None,
    ) -> Response:
        request = Request(method, url, data=data, params=params, headers=headers)
        return self.send(request, verify=verify, cert=cert, timeout=timeout)

    def send(
        self,
        request: Request,
        verify: typing.Optional[VerifyTypes] = None,
        cert: typing.Optional[CertTypes] = None,
        timeout: typing.Optional[TimeoutTypes] = None,
    ) -> Response:
        raise NotImplementedError()  # pragma: nocover

    def close(self) -> None:
        pass  # pragma: nocover

    def __enter__(self) -> "Dispatcher":
        return self

    def __exit__(
        self,
        exc_type: typing.Type[BaseException] = None,
        exc_value: typing.Optional[BaseException] = None,
        traceback: typing.Optional[TracebackType] = None,
    ) -> None:
        self.close()
