# tests/test_main.py

import pytest
from unittest.mock import MagicMock
import sys
import os

# Add the project root to sys.path to allow importing main.py
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import main  # Import the main.py module

@pytest.fixture
def mock_dependencies(mocker):
    """
    Fixture to mock external dependencies used in main.py.
    """
    mock_cleanup_chromadb = mocker.patch('main.cleanup_chromadb', return_value=None)
    mock_begin_benchmark = mocker.patch('main.begin_benchmark', return_value=None)
    mock_VectorDB_Controller = mocker.patch('main.VectorDB_Controller', return_value=MagicMock())
    mock_create_basic_charts = mocker.patch('main.create_basic_charts', return_value=None)
    mock_logger = mocker.patch('main.logger')
    mock_load_dotenv = mocker.patch('main.load_dotenv', return_value=None)

    # Mock datetime.now() to return a fixed date
    mock_datetime = mocker.patch('main.datetime')
    mock_now = MagicMock()
    mock_now.strftime.return_value = "2025-01-15"
    mock_datetime.now.return_value = mock_now

    return {
        'mock_cleanup_chromadb': mock_cleanup_chromadb,
        'mock_begin_benchmark': mock_begin_benchmark,
        'mock_VectorDB_Controller': mock_VectorDB_Controller,
        'mock_create_basic_charts': mock_create_basic_charts,
        'mock_logger': mock_logger,
        'mock_load_dotenv': mock_load_dotenv,
    }

def test_main_execution_without_statistics(mock_dependencies):
    """
    Test the main execution path when 'generate_statistics' is NOT in execution_steps.
    """
    execution_steps = [
        "ollama_to_ollama_evaluate",
        # Additional steps can be added here
    ]

    # Execute the main function with specified execution steps
    main.main(execution_steps=execution_steps)

    # Assertions to verify expected function calls
    mock_dependencies['mock_load_dotenv'].assert_called_once()
    mock_dependencies['mock_cleanup_chromadb'].assert_called_once()
    mock_dependencies['mock_VectorDB_Controller'].assert_called_once_with(keepVectorDB=False)
    mock_dependencies['mock_begin_benchmark'].assert_called_once()
    mock_dependencies['mock_create_basic_charts'].assert_not_called()
    mock_dependencies['mock_logger'].info.assert_any_call("Program started successfully.")
    mock_dependencies['mock_logger'].info.assert_any_call("Starting initialization.")

def test_main_execution_with_statistics(mock_dependencies):
    """
    Test the main execution path when 'generate_statistics' is in execution_steps.
    """
    execution_steps = [
        "generate_statistics",
    ]

    # Execute the main function with specified execution steps
    main.main(execution_steps=execution_steps)

    # Assertions to verify expected function calls
    mock_dependencies['mock_load_dotenv'].assert_called_once()
    mock_dependencies['mock_cleanup_chromadb'].assert_called_once()
    mock_dependencies['mock_VectorDB_Controller'].assert_not_called()  # Should not be called in this scenario
    mock_dependencies['mock_begin_benchmark'].assert_not_called()
    mock_dependencies['mock_create_basic_charts'].assert_called_once()
    mock_dependencies['mock_logger'].bind.return_value.info.assert_called_with("Statistics generated successfully.")

def test_main_execution_full_flow(mock_dependencies):
    """
    Test the main execution path with multiple execution_steps.
    """
    execution_steps = [
        "ollama_to_ollama_evaluate",
        "generate_statistics",
    ]

    # Execute the main function with specified execution steps
    main.main(execution_steps=execution_steps)

    # Assertions to verify expected function calls for both steps
    mock_dependencies['mock_load_dotenv'].assert_called_once()
    mock_dependencies['mock_cleanup_chromadb'].assert_called_once()
    mock_dependencies['mock_VectorDB_Controller'].assert_called_once_with(keepVectorDB=False)
    mock_dependencies['mock_begin_benchmark'].assert_called_once()
    mock_dependencies['mock_create_basic_charts'].assert_called_once()
    mock_dependencies['mock_logger'].info.assert_any_call("Program started successfully.")
    mock_dependencies['mock_logger'].info.assert_any_call("Starting initialization.")
    mock_dependencies['mock_logger'].bind.return_value.info.assert_called_with("Statistics generated successfully.")
