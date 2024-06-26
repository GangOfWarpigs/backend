import unittest

from madissues_backend.core.shared.application.mock_repository import EntityTable
from madissues_backend.core.shared.infrastructure.mocks.mock_authentication_service import \
    create_mock_authentication_service
from madissues_backend.core.shared.infrastructure.mocks.mock_event_bus import MockEventBus
from madissues_backend.core.students.application.commands.ban_student_command import BanStudentCommand, \
    BanStudentRequest
from madissues_backend.core.students.domain.student_mother import StudentMother
from madissues_backend.core.students.infrastructure.mocks.mock_student_repository import MockStudentRepository


class TestBanStudentCommand(unittest.TestCase):
    def setUp(self):
        self.db = EntityTable()
        self.student_repository = MockStudentRepository(self.db)
        self.event_bus = MockEventBus()
        self.student_getting_banned = StudentMother.random_student()
        self.student_getting_banned.is_council_member = False
        self.student_getting_banned.is_site_admin = False

        self.council_member = StudentMother.random_student()
        self.council_member.is_council_member = True

        self.site_admin = StudentMother.random_student()
        self.site_admin.is_site_admin = True

        self.unauthorized_student = StudentMother.random_student()
        self.unauthorized_student.is_council_member = False
        self.unauthorized_student.is_site_admin = False

        # Add student to repository
        self.student_repository.add(self.student_getting_banned)
        self.student_repository.add(self.council_member)
        self.student_repository.add(self.site_admin)
        self.student_repository.add(self.unauthorized_student)

    def test_ban_student_successful_as_council_member(self):
        # Reset the event bus (important)
        self.event_bus.events.clear()

        # Initialize authentication service with a valid council member token (get class and instantiate)
        authentication_service = create_mock_authentication_service(self.db)(self.council_member.token)
        command = BanStudentCommand(authentication_service, self.student_repository, self.event_bus)
        request = BanStudentRequest(
            student_id=str(self.student_getting_banned.id)
        )

        # Execute the command with the request
        response = command.execute(request)

        # Assert success and check response data
        self.assertTrue(response.is_success(), "Student should be banned")
        self.assertTrue(response.success.banned, "Student should be banned")
        self.assertTrue(self.student_repository.get_by_id(self.student_getting_banned.id).is_banned,
                        "Student should be banned in repository")
        self.assertEqual(len(self.event_bus.events), 1, "Should be triggered an event")

    def test_ban_student_successful_as_site_admin(self):
        # Reset the event bus (important)
        self.event_bus.events.clear()

        # Initialize authentication service with a valid site admin token (get class and instantiate)
        authentication_service = create_mock_authentication_service(self.db)(self.site_admin.token)
        command = BanStudentCommand(authentication_service, self.student_repository, self.event_bus)
        request = BanStudentRequest(
            student_id=str(self.student_getting_banned.id)
        )

        # Execute the command with the request
        response = command.execute(request)

        # Assert success and check response data
        self.assertTrue(response.is_success(), "Student should be banned")
        self.assertTrue(response.success.banned, "Student should be banned")
        self.assertTrue(self.student_repository.get_by_id(self.student_getting_banned.id).is_banned,
                        "Student should be banned in repository")
        self.assertEqual(len(self.event_bus.events), 1, "Should be triggered an event")

    def test_ban_student_unauthenticated(self):
        # Reset the event bus (important)
        self.event_bus.events.clear()

        # Initialize authentication service with a valid site admin token (get class and instantiate)
        authentication_service = create_mock_authentication_service(self.db)(self.unauthorized_student.token)
        command = BanStudentCommand(authentication_service, self.student_repository, self.event_bus)
        request = BanStudentRequest(
            student_id=str(self.student_getting_banned.id)
        )

        # Execute the command with the request
        response = command.execute(request)

        # Assert error and check response data
        self.assertTrue(response.is_error(), "Should not be able to ban student without authentication")

        # Check error code 403 and error message "User must be a student"
        self.assertEqual(response.error.error_code, 403, "Should return a 403 error")
        self.assertEqual(response.error.error_message, "User must be a council member or site admin",
                         "Should return 'User must be a council member or site admin'")

        self.assertEqual(len(self.event_bus.events), 0, "Should not be triggered an event")


if __name__ == '__main__':
    unittest.main()
