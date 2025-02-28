from enum import StrEnum


class APIStatus(StrEnum):
    Timeout = "Timeout"
    HTTPError = "HTTPError"
    Forbidden = "Forbidden"
    RateLimited = "Rate Limited"  # CF Workers 达到每分钟上限，服务将暂时不可用
    Limited = "Limited"  # CF Workers 达到当日上限，服务将完全不可用

    UnknowError = "Unknow Error"


class IssueBody:
    OK = "> [!TIP]\n下载服务正常运行。\n"
    Timeout = "> [!WARNING]\n下载服务请求超时。\n>> 这表示最近一次请求超时(10s)，服务仍或许可用。\n\n"
    HttpError = "> [!WARING]\n下载服务请求错误。\n>> 这表示最近一次请求返回 Http 错误，服务仍或许可用。\n\n"
    Forbidden = "> [!CAUTION]\n下载服务请求被拒绝。\n>> 这表示最近一次请求被拒绝，服务仍或许可用。\n\n"
    rateLimited = "> [!CAUTION]\n下载服务请求频率过高。\n>> 这表示最近请求数达到上限，服务将暂时不可用。\n\n"
    Limited = "> [!CAUTION]\n下载服务请求达到当日上限。\n>> 这表示今日请求数达到上限，服务将完全不可用。请次日 8:00(UTC+8:00) 后重试\n\n"

    UnknowError = (
        "> [!WARNING]\n下载服务请求错误。\n>> 发生未知错误，服务可用状态未知。\n\n"
    )
