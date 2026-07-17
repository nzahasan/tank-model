import json
from pathlib import Path

import pytest

from tank_core import project_helpers as ph
from tank_core import io_helpers as ioh

TEST_DATA_DIR = Path(__file__).absolute().parent / 'test_data'


def test_hms_basin_to_tank_basin_rejects_duplicate_node_name():

    hms_basin_def = '''
Subbasin: W1
     Downstream: J1
     Area: 100
End:

Subbasin: W1
     Downstream: J1
     Area: 200
End:

Junction: J1
End:
'''

    with pytest.raises(ValueError):
        ph.hms_basin_to_tank_basin(hms_basin_def)


def test_hms_basin_to_tank_basin_accepts_valid_sample():

    hms_basin_file = TEST_DATA_DIR / 'hms_basin_sample.basin'

    basin = ph.hms_basin_to_tank_basin(hms_basin_file.read_text())

    assert 'BAHADURABAD' in basin['basin_def']
    assert basin['root_node'] == ['BAHADURABAD']


def test_read_basin_file_rejects_duplicate_node_name(tmp_path):

    basin_file = tmp_path / 'duplicate_basin.json'

    basin_file.write_text('''
    {
        "basin_def": {
            "W1": {"type": "Subbasin", "area": 100, "downstream": "J1"},
            "W1": {"type": "Subbasin", "area": 200, "downstream": "J1"},
            "J1": {"type": "Junction"}
        },
        "root_node": ["J1"]
    }
    ''')

    with pytest.raises(ValueError):
        ioh.read_basin_file(str(basin_file))


def test_read_basin_file_accepts_valid_basin(tmp_path):

    basin_file = tmp_path / 'valid_basin.json'

    basin = {
        "basin_def": {
            "W1": {"type": "Subbasin", "area": 100, "downstream": "J1"},
            "J1": {"type": "Junction"}
        },
        "root_node": ["J1"]
    }

    basin_file.write_text(json.dumps(basin))

    loaded = ioh.read_basin_file(str(basin_file))

    assert loaded == basin
