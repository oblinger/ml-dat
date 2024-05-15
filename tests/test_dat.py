import os
import sys
import json
import tempfile
from pathlib import Path
from typing import Dict
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dvc_dat.dat import MAIN_CLASS, Dat, DatContainer


TMP_PATH = "/tmp/job_test"
TMP_PATH2 = "/tmp/job_test2"


@pytest.fixture
def do():
    from dvc_dat import do
    return do


@pytest.fixture
def spec1():
    return {
        "main": {"path": "test_dats/{YY}-{MM} Dats{unique}",
                 "my_key1": "my_val1", "my_key2": "my_val2"}
    }


@pytest.fixture
def dat1(spec1):
    return Dat(spec=spec1, path=TMP_PATH, overwrite=True)


@pytest.fixture
def spec2():
    return {"main": {"path": "test_dats/{YY}-{MM} Dats{unique}",
                     "my_key1": "my_val111", "my_key2": "my_val222"},
            "other": "key_value"}


@pytest.fixture
def dat_container_spec():
    return {"main": {"class": "DatContainer"}}


@pytest.fixture
def game_spec():
    return {"main": {"class": "Game"}, "game": {"views": {"view_1": "vid_1.mp4"}}}


@pytest.fixture
def mock_dat_root(monkeypatch: pytest.MonkeyPatch) -> tempfile.TemporaryDirectory:
    import dvc_dat.dat as dat
    temp_dir = tempfile.TemporaryDirectory()
    monkeypatch.setattr(dat, "DAT_ROOT", temp_dir.name)
    return temp_dir


@pytest.fixture
def temp_root_with_gameset(
    mock_dat_root: tempfile.TemporaryDirectory,
        dat_container_spec,
        game_spec: Dict) -> tempfile.TemporaryDirectory:
    gameset_path = Path(mock_dat_root.name, "gamesets/bb/baller10")
    gameset_path.mkdir(parents=True, exist_ok=True)

    with (gameset_path / "_spec_.yaml").open("w") as f:
        json.dump(dat_container_spec, f)

    game_1_path = gameset_path / "1"
    game_1_path.mkdir(exist_ok=True, parents=True)

    with (game_1_path / "_spec_.yaml").open("w") as f:
        json.dump(game_spec, f)

    return mock_dat_root


@pytest.fixture
def temp_root_with_runset(
        temp_root_with_gameset: tempfile.TemporaryDirectory,
        dat_container_spec) -> tempfile.TemporaryDirectory:
    mock_dat_root = temp_root_with_gameset
    runset_path = Path(mock_dat_root.name, "runsets/bb/baller10")
    runset_path.mkdir(parents=True, exist_ok=True)

    with (runset_path / "_spec_.yaml").open("w") as f:
        json.dump(dat_container_spec, f)

    run_1_path = runset_path / "1"
    run_1_path.mkdir(exist_ok=True, parents=True)

    game_1_path = Path(mock_dat_root.name, "gamesets/bb/baller10/1")

    run_spec = {
        "main": {"class": "MCProcRun"},
        "run": {
            "input_game": str(game_1_path),
            "mcproc_output": "my_file.pickle",
        },
    }

    with (run_1_path / "_spec_.yaml").open("w") as f:
        json.dump(run_spec, f)

    return mock_dat_root


# Tests


class TestTemplatedDatCreationAndDeletion:
    def test_empty_creation_and_deletion(self, do):
        assert (dat := do.dat_from_template({})), "Couldn't create Persistable"
        assert dat.delete(), "Couldn't delete Persistable"

    def test_creation_and_deletion_with_spec(self, do, spec1):
        assert (dat := do.dat_from_template(spec1)), "Couldn't create Persistable"
        assert dat.get_path_name().startswith("test_dats/"), "Wrong path"
        assert dat.delete(), "Couldn't delete Persistable"


class TestDatCreationFromStaticFolders:
    def test_create_with_spec(self, spec1):
        assert Dat(path=TMP_PATH, spec=spec1), "Couldn't create Persistable"

    def test_create_with_spec_and_path(self, spec1):
        assert Dat(path=TMP_PATH, spec=spec1), "Couldn't create Persistable"


class TestCreateSaveAndLoad:
    def test_create(self, spec1):  # Creation needed to work for these tests
        assert Dat(path=TMP_PATH, spec=spec1), "Couldn't create Persistable"

    def test_get(self, spec1):
        assert Dat.get(spec1, ["main", "my_key1"]) == "my_val1"
        assert Dat.get(spec1, "main.my_key1") == "my_val1"
        assert Dat.get(spec1, ["main"]) == spec1["main"]
        assert Dat.get(spec1, "main") == spec1["main"]

    def test_set(self, spec1):
        Dat.set(spec1, ["main", "foo"], "bar")
        assert Dat.get(spec1, ["main", "foo"]) == "bar"
        Dat.set(spec1, "main.foo", "baz")
        assert Dat.get(spec1, ["main", "foo"]) == "baz"

        Dat.set(spec1, ["key1"], "value1")
        assert Dat.get(spec1, ["key1"]) == "value1"
        Dat.set(spec1, "key1", "value2")
        assert Dat.get(spec1, ["key1"]) == "value2"

    def test_deep_set(self, spec1):
        Dat.set(spec1, ["level1", "level2", "level3", "lev4"], "val")
        assert Dat.get(spec1, ["level1", "level2", "level3", "lev4"]) == "val"

    def test_persistable_get_set(self, spec1):
        dat = Dat(spec=spec1, path=TMP_PATH)
        assert Dat.get(dat, ["main", "my_key1"]) == "my_val1"
        assert Dat.get(dat, ["main"]) == spec1["main"]

    def test_gets(self, spec1):
        dat = Dat(spec=spec1, path=TMP_PATH)
        assert Dat.gets(dat, "main.my_key1", "main") == [
            "my_val1",
            spec1["main"],
        ]

    def test_sets(self, spec1):
        Dat.sets(spec1, "main.foo = bar", "bip.bop.boop=3.14", "bip.zip=7")
        assert Dat.gets(spec1, "main.foo", "bip.bop.boop", "bip.zip") == [
            "bar",
            3.14,
            7,
        ]


class TestDatLoadingAndSaving:
    def test_create(self):
        assert Dat(spec={}, path=TMP_PATH), "Couldn't create Persistable"

    def test_path_accessor(self, dat1):
        assert dat1._path == TMP_PATH

    def test_spec_accessors(self, spec1, dat1):
        assert dat1._spec == spec1

    def test_save(self, dat1):
        dat1.save()
        assert True

    def test_load(self, spec1):
        original = Dat(spec=spec1, path=TMP_PATH)
        original.save()

        dat = Dat.load(TMP_PATH)
        assert isinstance(dat, Dat), "Did not load the Persistable"
        assert dat._spec == spec1


class TestDatContainers:
    def test_create(self):
        os.system(f"rm -r '{TMP_PATH}'")
        container = DatContainer(path=TMP_PATH, spec={})
        assert isinstance(container, DatContainer)
        assert container.get_dat_paths() == []
        assert container.get_dats() == []

    def test_save_empty_container(self):
        container = DatContainer(path=TMP_PATH, spec={})
        container.save()
        assert Dat.get(container._spec, MAIN_CLASS) == "DatContainer"

    def test_composite_dat_container(self):
        container = DatContainer(path=TMP_PATH, spec={}, overwrite=True)
        container.save()
        for i in range(10):
            name = f"sub_{i}"
            spec = {}
            Dat.set(spec, "main.my_nifty_name", name)
            sub = Dat(path=os.path.join(container._path, name), spec=spec)
            sub.save()

        reload: DatContainer[Dat] = DatContainer.load(TMP_PATH)
        assert isinstance(reload, DatContainer)
        assert Dat.get(reload._spec, MAIN_CLASS) == "DatContainer"

        paths = reload.get_dat_paths()
        assert isinstance(paths, list)
        assert isinstance(paths[3], str)

        sub_dats = reload.get_dats()
        assert isinstance(sub_dats, list)
        assert isinstance(sub_dats[3], Dat)
        assert Dat.get(sub_dats[8], "main.my_nifty_name") == "sub_8"

        os.system(f"rm -r '{TMP_PATH}'")
