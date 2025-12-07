"""Test that the application can run locally without MINITAP_API_KEY."""

import os
import pytest
from unittest.mock import patch
from pydantic import SecretStr

from minitap.mobile_use.config import (
    Settings,
    parse_llm_config,
    initialize_llm_config,
    get_default_llm_config,
)
from minitap.mobile_use.context import ExecutionSetup, MobileUseContext, DeviceContext, DevicePlatform
from minitap.mobile_use.sdk.types.task import TaskRequest


def test_execution_setup_defaults_to_no_remote_tracing():
    """Test that ExecutionSetup defaults to no remote tracing."""
    setup = ExecutionSetup()
    assert setup.enable_remote_tracing is False, "Remote tracing should be disabled by default"


def test_task_request_defaults_to_no_remote_tracing():
    """Test that TaskRequest defaults to no remote tracing."""
    task = TaskRequest(goal="Test goal")
    assert task.enable_remote_tracing is False, "Remote tracing should be disabled by default"


def test_default_llm_config_does_not_require_minitap():
    """Test that the default LLM config doesn't use minitap provider."""
    config = get_default_llm_config()
    
    # Check that no agent uses minitap provider
    assert config.planner.provider != "minitap", "Default planner should not use minitap"
    assert config.orchestrator.provider != "minitap", "Default orchestrator should not use minitap"
    assert config.contextor.provider != "minitap", "Default contextor should not use minitap"
    assert config.cortex.provider != "minitap", "Default cortex should not use minitap"
    assert config.executor.provider != "minitap", "Default executor should not use minitap"
    assert config.utils.hopper.provider != "minitap", "Default hopper should not use minitap"
    assert config.utils.outputter.provider != "minitap", "Default outputter should not use minitap"


def test_settings_minitap_api_key_optional():
    """Test that Settings can be created without MINITAP_API_KEY."""
    with patch.dict(os.environ, {}, clear=True):
        # Remove all environment variables
        settings = Settings()
        assert settings.MINITAP_API_KEY is None, "MINITAP_API_KEY should be optional"


def test_initialize_llm_config_without_minitap():
    """Test that LLM config can be initialized without MINITAP_API_KEY."""
    # Mock environment with only OPENAI_API_KEY
    with patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-key",
        "MINITAP_API_KEY": "",  # Explicitly empty
    }, clear=True):
        # This should not raise an error
        config = parse_llm_config()
        
        # Verify the config uses openai provider
        assert config.planner.provider == "openai", "Default config should use openai"
        

def test_context_without_minitap_api_key():
    """Test that MobileUseContext can be created without minitap_api_key."""
    device = DeviceContext(
        host_platform="LINUX",
        mobile_platform=DevicePlatform.ANDROID,
        device_id="test-device",
        device_width=1080,
        device_height=2340,
    )
    
    config = get_default_llm_config()
    
    # Create context without minitap_api_key
    context = MobileUseContext(
        trace_id="test-trace",
        device=device,
        llm_config=config,
        minitap_api_key=None,  # Should be optional
    )
    
    assert context.minitap_api_key is None, "minitap_api_key should be optional"
    assert context.execution_setup is None or context.execution_setup.enable_remote_tracing is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
