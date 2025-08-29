from collections.abc import Callable
from functools import wraps
from typing import TypeVar, Any, Self, Generic

T = TypeVar("T")


class Result(Generic[T]):

    def __init__(self, value: T | None = None, exception: Exception | None = None):
        self.value = value
        self.exception = exception
        self.is_success = exception is None

    @property
    def is_failure(self) -> bool:
        return not self.is_success

    def get_or_none(self) -> T | None:
        return self.value if self.is_success else None

    def get_or_raise(self) -> T:
        if self.is_success:
            return self.value
        raise self.exception

    def exception_or_none(self) -> Exception | None:
        return self.exception if self.is_failure else None

    def on_success(self, action: Callable[[T], None]) -> Self:
        if self.is_success:
            action(self.value)
        return self

    def on_failure(self, action: Callable[[Exception], None]) -> Self:
        if self.is_failure and self.exception is not None:
            action(self.exception)
        return self

    def fold(self, on_success: Callable[[T], Any], on_failure: Callable[[Exception], Any]) -> Any:
        if self.is_success:
            return on_success(self.value)
        else:
            return on_failure(self.exception)

    def __str__(self) -> str:
        if self.is_success:
            return f"Success({self.value})"
        else:
            return f"Failure({self.exception})"


def run_catching(func: Callable[..., T]) -> Callable[..., Result[T]]:

    @wraps(func)
    def wrapper(*args, **kwargs) -> Result[T]:
        try:
            return Result(value=func(*args, **kwargs))
        except Exception as e:
            return Result(exception=e)

    return wrapper
