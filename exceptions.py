class ParserError(Exception):
    """Can't find target HTML element"""


class BadRequest(Exception):
    """Somthing wrong with request"""


class HeadersError(Exception):
    """Can't get list of user-agents"""
