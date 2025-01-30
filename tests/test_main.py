# tests/test_main.py

import pytest
from unittest.mock import MagicMock, call
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

@pytest.fixture
def mock_config(mocker):
    """
    Fixture to mock configparser.ConfigParser and provide controlled configuration data.
    """
    # Define the required sections and options with default valid values
    config_data = {
        "rounds": {"answer_rounds": "3"},
        "BENCHMARK_NAME": {"benchmark_name": "test_benchmark"},
        "evaluator_models": {
            "GROQ_EVALUATOR_MODEL": "groq_model",
            "OLLAMA_EVALUATOR_MODEL": "ollama_model",
        },
        "execution_steps": {"EXECUTION_STEPS": ""},
        "student_models": {
            "STUDENT_OPENROUTER_MODELS": "openrouter_model1, openrouter_model2",
            "STUDENT_GROQ_MODELS": "groq_model1, groq_model2",
            "STUDENT_OLLAMA_MODELS": "ollama_model1, ollama_model2",
        },
        "vision": {"VISION_DB": "false"},
        "parquet": {"PARQUET": "false"},
        "keep_vector_db": {"KEEP_VECTOR_DB": "false"},
    }
    
    mock_config = MagicMock()
    
    # Mock has_section
    mock_config.has_section.side_effect = lambda section: section in config_data
    
    # Mock has_option
    mock_config.has_option.side_effect = lambda section, option: option in config_data.get(section, {})
    
    # Mock __getitem__ to return a dict-like object for each section
    def get_section(section):
        return config_data.get(section, {})
    
    mock_config.__getitem__.side_effect = get_section
    
    # Mock getboolean
    def mock_getboolean(section, option):
        value = config_data[section][option].lower()
        return value in ['1', 'yes', 'true', 'on']
    
    mock_config.getboolean.side_effect = mock_getboolean
    
    # Mock getint
    def mock_getint(section, option):
        return int(config_data[section][option])
    
    mock_config.getint.side_effect = mock_getint
    
    # Patch configparser.ConfigParser to return this mock_config
    mocker.patch('main.configparser.ConfigParser', return_value=mock_config)
    
    return config_data

def test_main_execution_without_statistics(mock_dependencies, mock_config):
    """
    Test the main execution path when 'generate_statistics' is NOT in execution_steps.
    Expect VectorDB_Controller to be called once.
    """
    # Set EXECUTION_STEPS to exclude 'generate_statistics' with only one benchmarking step
    mock_config['execution_steps']['EXECUTION_STEPS'] = "ollama_to_ollama_evaluate"
    
    # Execute the main function
    main.main()
    
    # Assertions to verify expected function calls
    mock_dependencies['mock_load_dotenv'].assert_called_once()
    mock_dependencies['mock_cleanup_chromadb'].assert_called_once()
    mock_dependencies['mock_VectorDB_Controller'].assert_called_once_with(keepVectorDB=False, VISION=False)
    mock_dependencies['mock_begin_benchmark'].assert_called_once()
    mock_dependencies['mock_create_basic_charts'].assert_not_called()
    mock_dependencies['mock_logger'].info.assert_any_call("Program started successfully.")
    mock_dependencies['mock_logger'].info.assert_any_call("Starting initialization.")

def test_main_execution_with_statistics(mock_dependencies, mock_config):
    """
    Test the main execution path when 'generate_statistics' is in execution_steps.
    Expect VectorDB_Controller not to be called and create_basic_charts to be called once.
    """
    # Set EXECUTION_STEPS to include only 'generate_statistics'
    mock_config['execution_steps']['EXECUTION_STEPS'] = "generate_statistics"
    
    # Execute the main function
    main.main()
    
    # Assertions to verify expected function calls
    mock_dependencies['mock_load_dotenv'].assert_called_once()
    mock_dependencies['mock_cleanup_chromadb'].assert_called_once()
    mock_dependencies['mock_VectorDB_Controller'].assert_not_called()  # Should not be called in this scenario
    mock_dependencies['mock_begin_benchmark'].assert_not_called()
    mock_dependencies['mock_create_basic_charts'].assert_called_once()
    mock_dependencies['mock_logger'].bind.return_value.info.assert_called_with("Statistics generated successfully.")

def test_main_execution_full_flow(mock_dependencies, mock_config):
    """
    Test the main execution path with multiple execution_steps.
    Expect VectorDB_Controller to be called once and create_basic_charts to be called once.
    """
    # Set EXECUTION_STEPS to include both benchmarking and statistics generation
    mock_config['execution_steps']['EXECUTION_STEPS'] = "ollama_to_ollama_evaluate, generate_statistics"
    
    # Execute the main function
    main.main()
    
    # Assertions to verify expected function calls for both steps
    mock_dependencies['mock_load_dotenv'].assert_called_once()
    mock_dependencies['mock_cleanup_chromadb'].assert_called_once()
    mock_dependencies['mock_VectorDB_Controller'].assert_called_once_with(keepVectorDB=False, VISION=False)
    mock_dependencies['mock_begin_benchmark'].assert_called_once()
    mock_dependencies['mock_create_basic_charts'].assert_called_once()
    mock_dependencies['mock_logger'].info.assert_any_call("Program started successfully.")
    mock_dependencies['mock_logger'].info.assert_any_call("Starting initialization.")
    mock_dependencies['mock_logger'].bind.return_value.info.assert_called_with("Statistics generated successfully.")
