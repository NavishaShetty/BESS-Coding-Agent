import pytest
from unittest.mock import patch, MagicMock
from energy_agent.energy_agent import EnergyAgent
from energy_agent.config import config

@pytest.fixture
def energy_agent():
    return EnergyAgent()

@patch('energy_agent.OpenAIServerModel')
def test_init(mock_openai, energy_agent):
    """Test initialization of EnergyAgent"""
    assert energy_agent.api_key == config.OPENROUTER_API_KEY
    assert energy_agent.model_id == config.MODEL
    assert energy_agent.api_base == config.OPENROUTER_API_BASE

@patch('energy_agent.OpenAIServerModel')
def test_energy_agent_creation(mock_openai, energy_agent):
    """Test energy_agent method creates proper agent"""
    mock_model = MagicMock()
    mock_openai.return_value = mock_model
    
    agent = energy_agent.energy_agent()
    
    # Verify OpenAIServerModel was called with correct parameters
    mock_openai.assert_called_once_with(
        model_id=energy_agent.model_id,
        api_base=energy_agent.api_base,
        api_key=energy_agent.api_key
    )

@patch('energy_agent.CodeAgent')
@patch('energy_agent.OpenAIServerModel')
def test_run_method(mock_openai, mock_code_agent, energy_agent):
    """Test run method executes properly"""
    mock_agent = MagicMock()
    mock_code_agent.return_value = mock_agent
    mock_agent.run.return_value = "Test response"
    
    response = energy_agent.run("test task")
    assert response == "Test response"
    mock_agent.run.assert_called_once_with(task="test task")

@patch('energy_agent.GradioUI')
@patch('energy_agent.CodeAgent')
@patch('energy_agent.OpenAIServerModel')
def test_start_ui(mock_openai, mock_code_agent, mock_gradio, energy_agent):
    """Test UI launch"""
    mock_ui = MagicMock()
    mock_gradio.return_value = mock_ui
    
    energy_agent.start_ui()
    mock_gradio.assert_called_once()
    mock_ui.launch.assert_called_once()