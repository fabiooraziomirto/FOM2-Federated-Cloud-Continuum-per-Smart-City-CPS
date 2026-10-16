import json
from orchestrator.contract import check_run_dir, REQUIRED_PROVENANCE


def test_empty_dir_fails(tmp_path):
    assert check_run_dir(tmp_path)


def test_valid_dir_passes(tmp_path):
    (tmp_path / "metrics.csv").write_text("t_s,metric,value,tier\n")
    (tmp_path / "run.log").write_text("")
    (tmp_path / "provenance.json").write_text(json.dumps({k: "x" for k in REQUIRED_PROVENANCE}))
    assert check_run_dir(tmp_path) == []
