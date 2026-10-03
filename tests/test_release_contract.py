"""Regression checks for the Linux session forwarding release contract."""

import unittest
from unittest.mock import patch

import validate_plugin as validator


class ReleaseContractTests(unittest.TestCase):
    def validate_with_env(self, names):
        original = validator.load_json

        def load(path, errors):
            value = original(path, errors)
            if path == validator.PLUGIN_ROOT / ".mcp.codex.json":
                server = value["mcpServers"]["databasin"]
                if names is None:
                    server.pop("env_vars", None)
                else:
                    server["env_vars"] = names
            return value

        errors = []
        with patch.object(validator, "load_json", side_effect=load):
            validator.validate_json_and_manifests(validator.tracked_paths(), errors)
        return errors

    def test_shipped_release_contract(self):
        self.assertEqual(self.validate_with_env(
            validator.EXPECTED_CODEX_ENV
        ), [])

    def test_old_config_and_partial_forwarding_are_rejected(self):
        for names in (None, [], ["DBUS_SESSION_BUS_ADDRESS"], ["XDG_RUNTIME_DIR"]):
            with self.subTest(names=names):
                errors = self.validate_with_env(names)
                self.assertTrue(any("secure Linux storage" in error for error in errors))

    def test_extra_environment_forwarding_is_rejected(self):
        errors = self.validate_with_env(
            ["DBUS_SESSION_BUS_ADDRESS", "XDG_RUNTIME_DIR", "UNRELATED_SESSION_VARIABLE"]
        )
        self.assertTrue(any("secure Linux storage" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
