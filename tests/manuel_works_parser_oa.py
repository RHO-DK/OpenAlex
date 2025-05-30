###--- brugt til manuel validering af parsing proces ved særligt udfordrende elementer - filen "problemfil.json"

import os
import sys

# Tilføj src til importsti for config - password til db via venv før  kørsel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from transform.transform_works_oa import parse_and_insert_works

def test_parse_and_insert_valid_file():
    testfile = os.path.join("tests", "problemfil.json")
    failed_files = []
    result = parse_and_insert_works(testfile, failed_files)
    assert result["inserted"] == 6
    assert result["skipped"] == 1
    assert failed_files == []