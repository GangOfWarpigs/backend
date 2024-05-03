from madissues_backend.core.shared.domain.entity import Entity
from madissues_backend.core.shared.domain.value_objects import GenericUUID


class Member(Entity[GenericUUID]):
    task_manager_id: str
    council_id: str