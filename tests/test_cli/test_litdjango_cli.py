import subprocess 


def test_litdjango_command_exists():
    result = subprocess.run(["litdjango"], capture_output=True, text=True)
    assert 'litdjango' in result.stdout