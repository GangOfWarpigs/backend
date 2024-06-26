import json
from abc import abstractmethod, ABC
from functools import wraps
from typing import Generic, TypeVar, Any, Callable
from pydantic import BaseModel, ValidationError
from madissues_backend.core.shared.domain.response import Response

CommandRequest = TypeVar("CommandRequest")
CommandResponse = TypeVar("CommandResponse")


class Command(Generic[CommandRequest, CommandResponse]):
    @abstractmethod
    def execute(self, request: CommandRequest) -> Response[CommandResponse]:
        pass

    def run(self, request: CommandRequest) -> Response[CommandResponse]:
        try:
            return self.execute(request)
        except ValidationError as e:
            field: list[str] = json.loads(e.json())[0]["loc"]
            return Response.field_fail(message='{} must be valid'.format(", ".join(field)), field=field)
        except ValueError as e:
            return Response.fail(message=str(e))
        except Exception as e:
            return Response.fail(code=-1, message=str(e))


def authenticated_only(cls):
    original_execute: Callable[[Any, CommandRequest], Response[CommandResponse]] = cls.execute  # type: ignore

    @wraps(original_execute)
    def new_execute(self, request: CommandRequest) -> 'Response[CommandResponse]':
        if not self.authentication_service.is_authenticated():
            return Response.fail(code=403, message="User must be authenticated")
        return original_execute(self, request)

    cls.execute = new_execute
    return cls


def students_only(cls):
    original_execute: Callable[[Any, CommandRequest], Response[CommandResponse]] = cls.execute  # type: ignore

    @wraps(original_execute)
    def new_execute(self, request: CommandRequest) -> 'Response[CommandResponse]':
        if not self.authentication_service.is_student():
            return Response.fail(code=403, message="User must be a student")
        return original_execute(self, request)

    cls.execute = new_execute
    return cls


def owners_only(cls):
    original_execute: Callable[[Any, CommandRequest], Response[CommandResponse]] = cls.execute  # type: ignore

    @wraps(original_execute)
    def new_execute(self, request: CommandRequest) -> 'Response[CommandResponse]':
        if not self.authentication_service.is_owner():
            return Response.fail(code=403, message="User must be a owner")
        return original_execute(self, request)

    cls.execute = new_execute
    return cls


def site_admins_only(cls):
    original_execute: Callable[[Any, CommandRequest], Response[CommandResponse]] = cls.execute  # type: ignore

    @wraps(original_execute)
    def new_execute(self, request: CommandRequest) -> 'Response[CommandResponse]':
        if not self.authentication_service.is_site_admin():
            return Response.fail(code=403, message="User must be a site admin")
        return original_execute(self, request)

    cls.execute = new_execute
    return cls


def council_members_only(cls):
    original_execute: Callable[[Any, CommandRequest], Response[CommandResponse]] = cls.execute  # type: ignore

    @wraps(original_execute)
    def new_execute(self, request: CommandRequest) -> 'Response[CommandResponse]':
        if not self.authentication_service.is_council_member():
            return Response.fail(code=403, message="User must be a council member")
        return original_execute(self, request)

    cls.execute = new_execute
    return cls


def council_members_or_site_admins_only(cls):
    original_execute: Callable[[Any, CommandRequest], Response[CommandResponse]] = cls.execute  # type: ignore

    @wraps(original_execute)
    def new_execute(self, request: CommandRequest) -> 'Response[CommandResponse]':
        if not self.authentication_service.is_council_member() and not self.authentication_service.is_site_admin():
            return Response.fail(code=403, message="User must be a council member or site admin")
        return original_execute(self, request)

    cls.execute = new_execute
    return cls