from abc import ABC, abstractmethod


class OrganizationQueryRepository(ABC):
    @abstractmethod
    def get_all_by_owner(self, owner_id: str):
        ...