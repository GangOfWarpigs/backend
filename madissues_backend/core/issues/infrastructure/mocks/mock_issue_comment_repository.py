from datetime import datetime
from typing import Dict
from uuid import UUID

from madissues_backend.core.issues.application.ports.issue_comment_repository import IssueCommentRepository
from madissues_backend.core.issues.domain.issue_comment import IssueComment
from madissues_backend.core.shared.application.mock_repository import GenericMockRepository, EntityTable
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class MockIssueCommentRepository(IssueCommentRepository, GenericMockRepository[UUID, IssueComment]):
    def __init__(self, entity_table: EntityTable):
        super().__init__(entity_table)
        self._issues: Dict[UUID, IssueComment] = self.entity_table.tables["issue_comments"]

    def add(self, issue: IssueComment):
        # Check if the issue already exists
        if issue.id in self._issues:
            raise ValueError(f"Issue with id {issue.id} already exists")
        self._issues[issue.id] = issue

    def remove(self, issue_id: GenericUUID):
        if issue_id not in self._issues:
            raise ValueError(f"Issue with id {issue_id} does not exist")
        del self._issues[issue_id]

    def get_by_id(self, issue_id: GenericUUID) -> IssueComment | None:
        return self._issues.get(issue_id)

    def save(self, issue_comment: IssueComment):
        if issue_comment.id not in self._issues:
            raise ValueError(f"Issue with id {issue_comment.id} does not exist")
        self._issues[issue_comment.id] = issue_comment
