import re

import adraitools


def test_adraitools_has_version_and_matches_pattern() -> None:
    assert adraitools.__version__ is not None
    assert re.match(r"^\d+\.\d+\.\d+$", adraitools.__version__) is not None
