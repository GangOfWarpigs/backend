import json
from abc import ABC
from pydantic import BaseModel, ValidationError

from madissues_backend.core.owners.application.ports.owner_repository import OwnerRepository
from madissues_backend.core.owners.domain.owner import Owner
from madissues_backend.core.shared.application.command import Command, CommandRequest, CommandResponse
from madissues_backend.core.shared.domain.password_hasher import PasswordHasher
from madissues_backend.core.shared.domain.response import Response
from madissues_backend.core.shared.domain.token_generator import TokenGenerator
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class SignUpOwnerCommandRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    verify_password: str
    phone_number: str


class SignUpOwnerCommandResponse(BaseModel):
    token: str
    owner_id: str


class SignUpOwnerCommand(Command[SignUpOwnerCommandRequest, SignUpOwnerCommandResponse]):

    def __init__(self, owner_repository: OwnerRepository, password_hasher: PasswordHasher,
                 token_generator: TokenGenerator):
        self.owner_repository = owner_repository
        self.password_hasher = password_hasher
        self.token_generator = token_generator

    def execute(self, request: SignUpOwnerCommandRequest) -> Response[SignUpOwnerCommandResponse]:
        if self.owner_repository.exists_owner_with_email(request.email):
            return Response.fail(code=2, message="Email is already in use")
        if self.passwords_do_not_match(request.password, request.verify_password):
            return Response.fail(code=3, message="Passwords do not match")

        owner = Owner(
            id=GenericUUID.next_id(),
            first_name=request.first_name,
            last_name=request.last_name,
            phone_number=request.phone_number,
            email=request.email
        )
        owner.set_password(raw_password=request.password, hasher=self.password_hasher)
        owner.generate_auth_token(self.token_generator)
        self.owner_repository.add(owner)
        return Response.ok(
            SignUpOwnerCommandResponse(
                owner_id=str(owner.id),
                token=owner.token
            )
        )

    @staticmethod
    def passwords_do_not_match(password, verify_password):
        return password != verify_password
