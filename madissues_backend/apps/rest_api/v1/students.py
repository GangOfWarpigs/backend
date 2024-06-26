from typing import Annotated

from fastapi import APIRouter, Header

from madissues_backend.apps.rest_api.dependencies import password_hasher, student_repository, authorization_service, \
    event_bus, token_generator, student_query_repository
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.students.application.commands.ban_student_command import BanStudentResponse, \
    BanStudentCommand, BanStudentRequest
from madissues_backend.core.students.application.commands.change_student_email_command import ChangeStudentEmailRequest, \
    ChangeStudentEmailResponse, ChangeStudentEmailCommand
from madissues_backend.core.students.application.commands.delete_student_account_command import DeleteStudentResponse, \
    DeleteStudentRequest, DeleteStudentCommand
from madissues_backend.core.students.application.commands.sign_in_student_command import SignInStudentCommandRequest, \
    SignInStudentCommandResponse, SignInStudentCommand
from madissues_backend.core.students.application.commands.sign_up_student_command import SignUpStudentCommandRequest, \
    SignUpStudentCommandResponse, SignUpStudentCommand
from madissues_backend.core.students.application.commands.update_student_personal_data import \
    ChangeStudentPersonalDataRequest, UpdateStudentPersonalDataCommand, ChangeStudentPersonalDataResponse
from madissues_backend.core.students.application.commands.update_student_preferences_command import \
    ChangeStudentPreferencesRequest, ChangeStudentPreferencesResponse, UpdateStudentPreferencesCommand
from madissues_backend.core.students.application.commands.update_student_profile_command import \
    ChangeStudentProfileRequest, ChangeStudentProfileResponse, UpdateStudentProfileCommand
from madissues_backend.core.students.application.queries.get_user_information_query import GetStudentInformationQuery
from madissues_backend.core.students.domain.read_model.student_read_model import StudentReadModel

router = APIRouter()


@router.post("/students/signup/", tags=["students"])
def student_signup(request: SignUpStudentCommandRequest) -> Response[SignUpStudentCommandResponse]:
    command = SignUpStudentCommand(student_repository, password_hasher, token_generator)
    return command.run(request)


@router.post("/students/signin/", tags=["students"])
def student_signin(request: SignInStudentCommandRequest) -> Response[SignInStudentCommandResponse]:
    command = SignInStudentCommand(student_repository, password_hasher)
    return command.run(request)


@router.put("/students/me/", tags=["students"])
def student_update_personal_data(request: ChangeStudentPersonalDataRequest, token: Annotated[str, Header()]) -> \
        Response[ChangeStudentPersonalDataResponse]:
    authentication = authorization_service(token)
    command = UpdateStudentPersonalDataCommand(authentication, student_repository, event_bus)
    return command.run(request)


@router.put("/students/me/preferences/", tags=["students"])
def student_update_preferences(request: ChangeStudentPreferencesRequest, token: Annotated[str, Header()]) -> Response[
    ChangeStudentPreferencesResponse]:
    authentication = authorization_service(token)
    command = UpdateStudentPreferencesCommand(authentication, student_repository, event_bus)
    return command.run(request)


@router.put("/students/me/profile/", tags=["students"])
def student_update_profile(request: ChangeStudentProfileRequest, token: Annotated[str, Header()]) -> Response[
    ChangeStudentProfileResponse]:
    authentication = authorization_service(token)
    command = UpdateStudentProfileCommand(authentication, student_repository, event_bus)
    return command.run(request)


@router.put("/students/me/change_email/", tags=["students"])
def student_change_email(request: ChangeStudentEmailRequest, token: Annotated[str, Header()]) -> Response[
    ChangeStudentEmailResponse]:
    authentication = authorization_service(token)
    command = ChangeStudentEmailCommand(authentication, student_repository, event_bus)
    return command.run(request)


@router.post("/students/{student_id}/ban/", tags=["students"])
def student_ban(student_id: str, token: Annotated[str, Header()]) -> Response[BanStudentResponse]:
    authentication = authorization_service(token)
    command = BanStudentCommand(authentication, student_repository, event_bus)
    return command.run(
        BanStudentRequest(
            student_id=student_id
        )
    )


@router.delete("/students/{student_id}/", tags=["students"])
def student_delete(student_id: str, token: Annotated[str, Header()]) -> Response[DeleteStudentResponse]:
    authentication = authorization_service(token)
    command = DeleteStudentCommand(authentication, student_repository, event_bus)
    return command.run(
        DeleteStudentRequest(
            student_id=student_id
        )
    )
@router.get("/students/me/", tags=["students"])
def get_owner_profile(token: Annotated[str, Header()]) -> Response[StudentReadModel]:
    authorization = authorization_service(token)
    query = GetStudentInformationQuery(authorization, student_query_repository)
    return query.run()
