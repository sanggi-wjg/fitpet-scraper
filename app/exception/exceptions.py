from app.enum.channel_enum import ChannelEnum
from app.enum.error_code_enum import ErrorCodeEnum


class FitpetScraperException(Exception):

    def __init__(self, message: str, error_code: ErrorCodeEnum):
        self.message = message
        self.error_code = error_code
        super().__init__(message)


class KeywordAlreadyExistsException(FitpetScraperException):

    def __init__(self, word: str):
        super().__init__(
            f"{word} 은(는) 이미 존재하는 단어 입니다.",
            ErrorCodeEnum.KEYWORD_ALREADY_EXISTS,
        )


class UnsupportedChannelException(FitpetScraperException):

    def __init__(self, channel: ChannelEnum):
        super().__init__(
            message=f"{channel.value} 은(는) 지원하지 않는 채널입니다.",
            error_code=ErrorCodeEnum.UNSUPPORTED_CHANNEL,
        )
