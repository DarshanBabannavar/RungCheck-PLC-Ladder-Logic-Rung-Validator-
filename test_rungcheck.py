from rungcheck import check_rung, check_lines


def test_valid_rung():
    assert check_rung("XIC I0.0 XIO I0.1 OTE O0.0") is None


def test_missing_output():
    assert check_rung("XIC I0.0 XIO I0.1") == "missing output"


def test_bad_address():
    assert check_rung("XIC X0.0 OTE O0.0") == "bad address"


def test_too_many_outputs():
    assert check_rung("XIC I0.0 OTE O0.0 OTU O0.1") == "too many outputs"


def test_output_not_last():
    assert check_rung("OTE O0.0 XIC I0.0") == "output not last"


def test_unknown_instruction():
    assert check_rung("ABC I0.0 OTE O0.0") == "unknown instruction"


def test_check_lines():
    lines = [
        "XIC I0.0 OTE O0.0",
        "XIC I0.1 XIO I0.2 OTE O0.1",
    ]

    assert check_lines(lines) == (2, [])