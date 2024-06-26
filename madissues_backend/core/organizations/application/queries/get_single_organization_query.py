from typing import Any

from pydantic import BaseModel

from madissues_backend.core.organizations.application.ports.organization_query_repository import \
    OrganizationQueryRepository
from madissues_backend.core.organizations.domain.read_models.organization_read_model import OrganizationReadModel
from madissues_backend.core.shared.application.authentication_service import AuthenticationService
from madissues_backend.core.shared.application.query import Query
from madissues_backend.core.shared.domain.response import Response


class Params(BaseModel):
    id: str


class GetSingleOrganizationQuery(Query[Params, OrganizationReadModel]):
    def execute(self, params: Params | None = None) -> Response[OrganizationReadModel]:
        if params is not None:
            return Response.ok(self.query_repository.get_by_id(params.id))
        return Response.fail(message="you must send an id")

    def __init__(self, query_repository: OrganizationQueryRepository):
        self.query_repository = query_repository
