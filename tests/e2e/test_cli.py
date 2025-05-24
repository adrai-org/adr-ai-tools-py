from subprocess import run

import adraitools


def test_cli_print_version():
    result = run(["adr-ai-tools", "--version"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "adr-ai-tools" in result.stdout
    assert adraitools.__version__ in result.stdout
