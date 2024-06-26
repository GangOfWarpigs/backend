import unittest
from unittest.mock import Mock, MagicMock
from madissues_backend.core.shared.domain.value_objects import GenericUUID
from madissues_backend.core.task_manager.domain.task_manager_config import TaskManagerConfig
from madissues_backend.core.task_manager.domain.task_manager_service import TaskManagerFactory, TaskManagerService
from madissues_backend.core.task_manager.domain.task_manager import TaskManager
from madissues_backend.core.task_manager.domain.board import Board


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.task_manager_factory = Mock(spec=TaskManagerFactory)
        self.task_manager_service = Mock(spec=TaskManagerService)
        self.task_manager_factory.of.return_value = self.task_manager_service

        # Estableciendo valores de retorno de los métodos mockeados
        self.task_manager_service.create_empty_board.return_value = "123e4567-e89b-12d3-a456-426614174000"
        self.task_manager_service.create_empty_list.return_value = "list_id"

        # Configuración inicial del TaskManager
        self.task_manager = TaskManager(
            id=GenericUUID.next_id(),
            organization_id=GenericUUID.next_id(),
            config=TaskManagerConfig(service="trello", api_key="test_key", api_token="test_token"),
            task_manager_project_id="123e4567-e89b-12d3-a456-426614174000"
        )

    def test_generate_infrastructure(self):
        self.task_manager.generate_infrastructure(self.task_manager_factory)
        self.task_manager_factory.of.assert_called_once_with(self.task_manager.config)
        self.task_manager_service.create_empty_board.assert_any_call(self.task_manager.task_manager_project_id, "Faqs")
        self.task_manager_service.create_empty_board.assert_any_call(self.task_manager.task_manager_project_id, "Issues")
        self.assertEqual(self.task_manager_service.create_empty_list.call_count, 8)
        self.assertIsNotNone(self.task_manager.faqs_board)
        self.assertIsNotNone(self.task_manager.issue_board)

    def test_generate_idle_board(self):
        board = self.task_manager.generate_idle_board("test", self.task_manager_service)
        self.task_manager_service.create_empty_board.assert_called_once_with(self.task_manager.task_manager_project_id, "test")
        self.assertEqual(self.task_manager_service.create_empty_list.call_count, 4)
        self.assertIsNotNone(board)

    def test_generate_idle_board_with_different_name(self):
        board = self.task_manager.generate_idle_board("different_test", self.task_manager_service)
        self.task_manager_service.create_empty_board.assert_called_once_with(self.task_manager.task_manager_project_id, "different_test")
        self.assertEqual(self.task_manager_service.create_empty_list.call_count, 4)
        self.assertIsNotNone(board)

    def test_generate_infrastructure_with_different_config(self):
        self.task_manager.config = TaskManagerConfig(service="trello", api_key="different_test_key", api_token="different_test_token")
        self.task_manager.generate_infrastructure(self.task_manager_factory)
        self.task_manager_factory.of.assert_called_once_with(self.task_manager.config)
        self.task_manager_service.create_empty_board.assert_any_call(self.task_manager.task_manager_project_id, "Faqs")
        self.task_manager_service.create_empty_board.assert_any_call(self.task_manager.task_manager_project_id, "Issues")
        self.assertEqual(self.task_manager_service.create_empty_list.call_count, 8)
        self.assertIsNotNone(self.task_manager.faqs_board)
        self.assertIsNotNone(self.task_manager.issue_board)

    def test_generate_infrastructure_with_same_config(self):
        # Se llama dos veces a generate_infrastructure para probar con la misma configuración
        self.task_manager.generate_infrastructure(self.task_manager_factory)
        self.task_manager.generate_infrastructure(self.task_manager_factory)
        self.task_manager_factory.of.assert_called_with(self.task_manager.config)
        self.task_manager_service.create_empty_board.assert_any_call(self.task_manager.task_manager_project_id, "Faqs")
        self.task_manager_service.create_empty_board.assert_any_call(self.task_manager.task_manager_project_id, "Issues")
        self.assertEqual(self.task_manager_service.create_empty_list.call_count, 16)  # 8 llamadas por cada generate_infrastructure
        self.assertIsNotNone(self.task_manager.faqs_board)
        self.assertIsNotNone(self.task_manager.issue_board)

    def test_generate_infrastructure_with_same_service(self):
        # Se llama dos veces a generate_infrastructure para probar con la misma configuración
        self.task_manager.generate_infrastructure(self.task_manager_factory)
        self.task_manager.generate_infrastructure(self.task_manager_factory)
        self.task_manager_factory.of.assert_called_with(self.task_manager.config)
        self.task_manager_service.create_empty_board.assert_any_call(self.task_manager.task_manager_project_id, "Faqs")
        self.task_manager_service.create_empty_board.assert_any_call(self.task_manager.task_manager_project_id, "Issues")
        self.assertEqual(self.task_manager_service.create_empty_list.call_count, 16)  # 8 llamadas por cada generate_infrastructure
        self.assertIsNotNone(self.task_manager.faqs_board)
        self.assertIsNotNone(self.task_manager.issue_board)


if __name__ == '__main__':
    unittest.main()
