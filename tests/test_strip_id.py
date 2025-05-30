import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from utils.helpers import strip_id

def test_strip_id():
    assert strip_id("https://openalex.org/W123") == "W123"
    assert strip_id("https://orcid.org/0000-0002-1234-5678") == "0000-0002-1234-5678"
    assert strip_id("https://doi.org/10.18637/jss.v082.i13") == "10.18637/jss.v082.i13"
    assert strip_id(None) is None
    assert strip_id("JustAnID") == "JustAnID"