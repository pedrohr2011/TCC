# -*- coding: utf-8 -*-
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from app import gee_config


class GeeConfigTest(unittest.TestCase):
    def test_reads_project_from_local_env_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text("GEE_PROJECT_ID=meu-projeto\n", encoding="utf-8")

            with mock.patch.object(gee_config, "BASE_DIR", Path(temp_dir)):
                with mock.patch.dict(os.environ, {}, clear=True):
                    self.assertEqual(gee_config.get_gee_project_id(), "meu-projeto")

    def test_real_environment_has_priority_over_local_env_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text("GEE_PROJECT_ID=projeto-do-env-file\n", encoding="utf-8")

            with mock.patch.object(gee_config, "BASE_DIR", Path(temp_dir)):
                with mock.patch.dict(os.environ, {"GEE_PROJECT_ID": "projeto-do-terminal"}, clear=True):
                    self.assertEqual(gee_config.get_gee_project_id(), "projeto-do-terminal")

    def test_initialize_fails_clearly_without_project(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with mock.patch.object(gee_config, "BASE_DIR", Path(temp_dir)):
                with mock.patch.dict(os.environ, {}, clear=True):
                    with self.assertRaisesRegex(RuntimeError, "GEE_PROJECT_ID"):
                        gee_config.initialize_gee()


if __name__ == "__main__":
    unittest.main()
