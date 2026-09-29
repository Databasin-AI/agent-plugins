#!/usr/bin/env python3
"""Dependency-light repository checks for the Databasin plugin package.

The script validates both host manifests, active prompt surfaces, the OpenAI
listing constraints, the deployment-dependent submission documentation, and
secret/unsafe-instruction patterns. It uses PyYAML when the runner already has
it, but includes a small fallback for environments where installing
dependencies is undesirable.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "databasin"
EXPECTED_PLUGIN_VERSION = "0.9.3"
EXPECTED_MCP_PACKAGE = "@databasin/mcp-client@0.2.2"

REMOTE_TOOL_NAMES = {
    "databasin_get_capabilities",
    "databasin_get_context",
    "databasin_search",
    "databasin_get_schema",
    "databasin_run_agent",
    "databasin_get_agent_run",
    "databasin_cancel_agent_run",
    "databasin_run_query",
    "databasin_get_query_status",
    "databasin_cancel_query",
    "databasin_run_assistant",
    "databasin_get_support_context",
    "databasin_list_support_tickets",
    "databasin_get_support_ticket",
    "databasin_create_support_ticket",
    "databasin_add_support_ticket_message",
    "databasin_update_support_ticket",
    "databasin_list_support_notifications",
    "databasin_mark_support_notification_read",
    "databasin_mark_all_support_notifications_read",
}
LOCAL_TOOL_NAMES = {"databasin_auth_status", "databasin_login"}
ALLOWED_TOOL_NAMES = REMOTE_TOOL_NAMES | LOCAL_TOOL_NAMES


def tracked_paths() -> list[Path]:
    """Return repository files, including untracked files during local review."""

    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return [
            path
            for path in ROOT.rglob("*")
            if path.is_file() and ".git" not in path.parts
        ]

    paths = {
        ROOT / item.decode("utf-8")
        for item in result.stdout.split(b"\0")
        if item and (ROOT / item.decode("utf-8")).is_file()
    }
    paths.update(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and "__pycache__" not in path.parts
    )
    return sorted(paths)


def display(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path, errors: list[str]) -> object | None:
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"{display(path)}: invalid JSON ({exc})")
        return None


def resolve_declared_path(base: Path, value: object, label: str, errors: list[str]) -> Path | None:
    if not isinstance(value, str) or not value:
        errors.append(f"{label}: manifest path must be a non-empty string")
        return None

    candidate = (base / value).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        errors.append(f"{label}: path escapes the repository: {value!r}")
        return None
    return candidate


def validate_json_and_manifests(paths: list[Path], errors: list[str]) -> set[Path]:
    json_paths = [path for path in paths if path.suffix.lower() == ".json"]
    parsed: dict[Path, object] = {}
    for path in json_paths:
        value = load_json(path, errors)
        if value is not None:
            parsed[path] = value

    marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"
    marketplace = parsed.get(marketplace_path)
    if isinstance(marketplace, dict):
        entries = marketplace.get("plugins")
        if not isinstance(entries, list):
            errors.append(".claude-plugin/marketplace.json: 'plugins' must be an array")
        else:
            for index, entry in enumerate(entries):
                if not isinstance(entry, dict):
                    errors.append(f".claude-plugin/marketplace.json: plugins[{index}] must be an object")
                    continue
                source = entry.get("source")
                candidate = resolve_declared_path(
                    ROOT,
                    source,
                    f".claude-plugin/marketplace.json: plugins[{index}].source",
                    errors,
                )
                if candidate is not None and not candidate.exists():
                    errors.append(
                        ".claude-plugin/marketplace.json: missing declared plugin source "
                        f"{source!r}"
                    )

    codex_marketplace_path = ROOT / ".agents" / "plugins" / "marketplace.json"
    codex_marketplace = parsed.get(codex_marketplace_path)
    if not isinstance(codex_marketplace, dict):
        errors.append(f"{display(codex_marketplace_path)}: marketplace must be a JSON object")
    else:
        entries = codex_marketplace.get("plugins")
        if not isinstance(entries, list) or not entries:
            errors.append(f"{display(codex_marketplace_path)}: 'plugins' must be a non-empty array")
        else:
            for index, entry in enumerate(entries):
                if not isinstance(entry, dict):
                    errors.append(f"{display(codex_marketplace_path)}: plugins[{index}] must be an object")
                    continue
                source = entry.get("source")
                source_path = source.get("path") if isinstance(source, dict) else None
                candidate = resolve_declared_path(
                    ROOT,
                    source_path,
                    f"{display(codex_marketplace_path)}: plugins[{index}].source.path",
                    errors,
                )
                if candidate is not None and not candidate.exists():
                    errors.append(
                        f"{display(codex_marketplace_path)}: missing declared plugin source {source_path!r}"
                    )

    plugin_manifest_path = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
    plugin = parsed.get(plugin_manifest_path)
    declared: set[Path] = set()
    if not isinstance(plugin, dict):
        errors.append(f"{display(plugin_manifest_path)}: manifest must be a JSON object")
        return declared

    if plugin.get("version") != EXPECTED_PLUGIN_VERSION:
        errors.append(
            f"{display(plugin_manifest_path)}: version must be {EXPECTED_PLUGIN_VERSION!r}"
        )
    if plugin.get("displayName") != "Databasin":
        errors.append(f"{display(plugin_manifest_path)}: displayName must be 'Databasin'")
    if plugin.get("repository") != "https://github.com/Databasin-AI/agent-plugins":
        errors.append(f"{display(plugin_manifest_path)}: repository metadata is missing or stale")
    if plugin.get("mcpServers") != "./.mcp.json":
        errors.append(f"{display(plugin_manifest_path)}: mcpServers must reference './.mcp.json'")

    for component_type, expected in (("agents", "file"), ("commands", "file"), ("skills", "skill")):
        values = plugin.get(component_type)
        if values is None:
            continue
        if not isinstance(values, list):
            errors.append(f"{display(plugin_manifest_path)}: '{component_type}' must be an array")
            continue
        for index, value in enumerate(values):
            label = f"{display(plugin_manifest_path)}: {component_type}[{index}]"
            candidate = resolve_declared_path(PLUGIN_ROOT, value, label, errors)
            if candidate is None:
                continue
            declared.add(candidate)
            if not candidate.exists():
                errors.append(f"{label}: stale declared path {value!r}")
            elif expected == "file" and candidate.is_dir():
                children = set(candidate.glob("*.md"))
                if not children:
                    errors.append(f"{label}: declared component directory has no Markdown components: {value!r}")
                declared.update(children)
            elif expected == "file" and not candidate.is_file():
                errors.append(f"{label}: expected a file or component directory, found {value!r}")
            elif expected == "skill" and candidate.is_dir():
                if (candidate / "SKILL.md").is_file():
                    declared.add(candidate / "SKILL.md")
                else:
                    children = {
                        skill
                        for skill in candidate.iterdir()
                        if skill.is_dir() and (skill / "SKILL.md").is_file()
                    }
                    if not children:
                        errors.append(
                            f"{label}: declared skill directory has no child SKILL.md files: {value!r}"
                        )
                    declared.update(children)
                    declared.update(skill / "SKILL.md" for skill in children)
            elif expected == "skill":
                errors.append(f"{label}: expected a skill directory, found {value!r}")

    # Catch newly added prompt surfaces that are silently omitted from the manifest.
    actual_components: set[Path] = set()
    for directory in (PLUGIN_ROOT / "agents", PLUGIN_ROOT / "commands"):
        if directory.is_dir():
            actual_components.update(directory.glob("*.md"))
    skills_directory = PLUGIN_ROOT / "skills"
    if skills_directory.is_dir():
        actual_components.update(
            skill / "SKILL.md"
            for skill in skills_directory.iterdir()
            if skill.is_dir() and (skill / "SKILL.md").is_file()
        )
    for path in sorted(actual_components):
        if path not in declared:
            errors.append(f"{display(path)}: active prompt surface is missing from plugin.json")

    codex_manifest_path = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
    codex = parsed.get(codex_manifest_path)
    if not isinstance(codex, dict):
        errors.append(f"{display(codex_manifest_path)}: manifest must be a JSON object")
    else:
        if codex.get("name") != plugin.get("name"):
            errors.append("Claude and Codex plugin names must match")
        if codex.get("version") != plugin.get("version"):
            errors.append("Claude and Codex plugin versions must match")
        if codex.get("repository") != plugin.get("repository"):
            errors.append("Claude and Codex plugin repositories must match")
        if codex.get("mcpServers") != "./.mcp.json":
            errors.append(f"{display(codex_manifest_path)}: mcpServers must reference './.mcp.json'")
        skills_path = resolve_declared_path(
            PLUGIN_ROOT,
            codex.get("skills"),
            f"{display(codex_manifest_path)}: skills",
            errors,
        )
        if skills_path is not None and not skills_path.is_dir():
            errors.append(f"{display(codex_manifest_path)}: skills path must be a directory")

    mcp_path = PLUGIN_ROOT / ".mcp.json"
    mcp = parsed.get(mcp_path)
    expected_server = {
        "command": "npx",
        "args": ["-y", EXPECTED_MCP_PACKAGE, "--environment", "prod"],
        "env_vars": ["DBUS_SESSION_BUS_ADDRESS", "XDG_RUNTIME_DIR"],
    }
    if not isinstance(mcp, dict) or mcp.get("mcpServers") != {"databasin": expected_server}:
        errors.append(
            f"{display(mcp_path)}: must pin the production stdio client to {EXPECTED_MCP_PACKAGE} "
            "and forward only DBUS_SESSION_BUS_ADDRESS and XDG_RUNTIME_DIR for secure Linux storage"
        )

    if isinstance(marketplace, dict) and marketplace.get("version") != EXPECTED_PLUGIN_VERSION:
        errors.append(".claude-plugin/marketplace.json: version must match the plugin release")

    return declared


def validate_openai_metadata(errors: list[str]) -> None:
    """Validate the listing fields that are checked before MCP review."""

    path = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
    value = load_json(path, errors)
    if not isinstance(value, dict):
        return

    interface = value.get("interface")
    if not isinstance(interface, dict):
        errors.append(f"{display(path)}: interface must be an object")
        return

    short_description = interface.get("shortDescription")
    if not isinstance(short_description, str):
        errors.append(f"{display(path)}: shortDescription must be a string")
    elif len(short_description) > 30:
        errors.append(f"{display(path)}: shortDescription exceeds 30 characters")

    long_description = interface.get("longDescription")
    if not isinstance(long_description, str):
        errors.append(f"{display(path)}: longDescription must be a string")
    elif len(long_description) > 4000:
        errors.append(f"{display(path)}: longDescription exceeds 4000 characters")

    display_name = interface.get("displayName")
    if not isinstance(display_name, str):
        errors.append(f"{display(path)}: displayName must be a string")
    elif len(display_name) > 30:
        errors.append(f"{display(path)}: displayName exceeds 30 characters")

    if interface.get("category") != "Data & Analytics":
        errors.append(f"{display(path)}: category must be 'Data & Analytics'")

    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or len(prompts) > 3:
        errors.append(f"{display(path)}: defaultPrompt must contain at most three prompts")
    elif any(
        not isinstance(prompt, str) or len(prompt) > 128 or "@" in prompt
        for prompt in prompts
    ):
        errors.append(
            f"{display(path)}: every default prompt must be a string <=128 characters without '@'"
        )

    marketplace_path = ROOT / ".agents" / "plugins" / "marketplace.json"
    marketplace = load_json(marketplace_path, errors)
    if isinstance(marketplace, dict):
        entries = marketplace.get("plugins")
        databasin = next(
            (
                entry
                for entry in entries
                if isinstance(entry, dict) and entry.get("name") == value.get("name")
            ),
            None,
        ) if isinstance(entries, list) else None
        if not isinstance(databasin, dict):
            errors.append(f"{display(marketplace_path)}: missing Databasin plugin entry")
        elif databasin.get("category") != "Data & Analytics":
            errors.append(f"{display(marketplace_path)}: Databasin category must be 'Data & Analytics'")


def validate_submission_documentation(errors: list[str]) -> None:
    """Keep the documented reviewer matrix aligned with the submission gate."""

    submission_path = PLUGIN_ROOT / "SUBMISSION.md"
    matrix_path = ROOT / "tests" / "AGENT-BEHAVIOR-MATRIX.md"
    try:
        submission = submission_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"{display(submission_path)}: cannot read submission checklist ({exc})")
        return
    try:
        matrix = matrix_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"{display(matrix_path)}: cannot read behavior matrix ({exc})")
        return

    missing_tools = sorted(REMOTE_TOOL_NAMES - set(re.findall(r"`(databasin_[a-z_]+)`", submission)))
    if missing_tools:
        errors.append(f"{display(submission_path)}: missing catalog tools: {', '.join(missing_tools)}")

    case_ids = re.findall(r"^\|\s*([PN]\d+)\s*\|", matrix, flags=re.MULTILINE)
    positive = [case for case in case_ids if case.startswith("P")]
    negative = [case for case in case_ids if case.startswith("N")]
    if len(positive) != 5 or set(positive) != {"P1", "P2", "P3", "P4", "P5"}:
        errors.append(f"{display(matrix_path)}: expected exactly positive cases P1-P5")
    if len(negative) != 3 or set(negative) != {"N1", "N2", "N3"}:
        errors.append(f"{display(matrix_path)}: expected exactly negative cases N1-N3")
    for required in ("tools/list", "deployment", "external gates"):
        if required.lower() not in submission.lower():
            errors.append(f"{display(submission_path)}: missing submission requirement wording {required!r}")


def parse_frontmatter(block: str) -> str | None:
    """Return an error string, or None when a YAML mapping parses successfully."""

    try:
        import yaml  # type: ignore
    except ImportError:
        yaml = None

    if yaml is not None:
        try:
            value = yaml.safe_load(block)
        except Exception as exc:  # PyYAML has several parser exception classes.
            return f"YAML parse error: {exc}"
        if not isinstance(value, dict):
            return "frontmatter must parse to a YAML mapping"
        return None

    # Minimal fallback: all current metadata is a flat mapping. This catches
    # malformed unquoted values without adding a runtime dependency to CI.
    keys: set[str] = set()
    for line_number, line in enumerate(block.splitlines(), start=1):
        if not line.strip():
            continue
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$", line)
        if not match:
            return f"line {line_number}: expected 'key: value' YAML metadata"
        key, value = match.groups()
        keys.add(key)
        if value and not value.startswith(("'", '"', "|", ">")):
            if "\\n" in value or re.search(r":\s", value):
                return f"line {line_number}: unquoted YAML value contains an unsafe escape or colon"
    if not keys:
        return "frontmatter mapping is empty"
    return None


def active_prompt_files() -> list[Path]:
    files: set[Path] = set()
    for directory in (PLUGIN_ROOT / "agents", PLUGIN_ROOT / "commands"):
        if directory.is_dir():
            files.update(directory.glob("*.md"))
    skills = PLUGIN_ROOT / "skills"
    if skills.is_dir():
        files.update(skill / "SKILL.md" for skill in skills.iterdir() if (skill / "SKILL.md").is_file())
    return sorted(files)


def validate_frontmatter(errors: list[str]) -> list[Path]:
    active = active_prompt_files()
    for path in active:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{display(path)}: cannot read prompt surface ({exc})")
            continue

        if not lines or lines[0].strip() != "---":
            errors.append(f"{display(path)}: missing YAML frontmatter block")
            continue
        try:
            end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
        except StopIteration:
            errors.append(f"{display(path)}: YAML frontmatter has no closing --- delimiter")
            continue

        problem = parse_frontmatter("\n".join(lines[1:end]))
        if problem:
            errors.append(f"{display(path)}: {problem}")
    return active


GENERIC_API_COMMAND = re.compile(r"(?i)(?:^|[`$>])\s*(?:[-*]\s*)?databasin\s+api\b")
TOKEN_FILE_INSTRUCTION = re.compile(
    r"(?i)(?:\b(?:cat|type|get-content|head|tail|less|more|sed|awk)\s+"
    r"[^\n]{0,120}\b(?:\.token|token(?:[_ -]?file)?|jwt|secret(?:s)?|credential(?:s)?)\b"
    r"|\b(?:read|open|print|dump)\s+(?:the\s+)?[^\n]{0,100}\b"
    r"(?:\.token|token(?:[_ -]?file)?|jwt|secret(?:s)?|credential(?:s)?)\b)"
)
MANDATORY_SAMPLE_WORDS = re.compile(r"(?i)\b(?:always|must|required|mandatory|default(?:ly)?)\b")
SELECT_STAR = re.compile(r"(?i)\bselect\s+\*\b")
NEGATIVE_SAFETY_WORDS = re.compile(r"(?i)\b(?:do not|don't|never|avoid|not)\b")
TOOL_NAME = re.compile(r"\bdatabasin_[a-z_]+\b")
def validate_unsafe_prompt_patterns(active: Iterable[Path], errors: list[str]) -> None:
    for path in active:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for line_number, line in enumerate(lines, start=1):
            if GENERIC_API_COMMAND.search(line):
                errors.append(f"{display(path)}:{line_number}: unsafe generic 'databasin api' command pattern")
            if TOKEN_FILE_INSTRUCTION.search(line):
                errors.append(f"{display(path)}:{line_number}: instruction to read or print a token/secret file")
            if SELECT_STAR.search(line) and MANDATORY_SAMPLE_WORDS.search(line):
                if not NEGATIVE_SAFETY_WORDS.search(line):
                    errors.append(f"{display(path)}:{line_number}: mandatory SELECT * sampling pattern")
            for tool_name in TOOL_NAME.findall(line):
                if tool_name not in ALLOWED_TOOL_NAMES:
                    errors.append(f"{display(path)}:{line_number}: unknown Databasin MCP tool {tool_name!r}")


def validate_documented_tools(paths: Iterable[Path], errors: list[str]) -> None:
    """Reject retired or invented tool names across shipped user-facing docs."""

    checked = {
        ROOT / "README.md",
        ROOT / "tests" / "AGENT-BEHAVIOR-MATRIX.md",
        PLUGIN_ROOT / "README.md",
        PLUGIN_ROOT / "MCP-SETUP.md",
        PLUGIN_ROOT / "PLUGIN-USAGE.md",
        PLUGIN_ROOT / "SUBMISSION.md",
        *active_prompt_files(),
    }
    for path in sorted(set(paths) & checked):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for line_number, line in enumerate(lines, start=1):
            for tool_name in TOOL_NAME.findall(line):
                if tool_name not in ALLOWED_TOOL_NAMES:
                    errors.append(
                        f"{display(path)}:{line_number}: retired or unknown Databasin MCP tool {tool_name!r}"
                    )


SECRET_FILENAME = re.compile(
    r"(?i)(^|/)(?:\.env(?:\..*)?|.*\.(?:pem|key|p12|pfx)|id_(?:rsa|dsa|ecdsa|ed25519)(?:\..*)?|"
    r"(?:credentials?|secrets?|tokens?)(?:\.[^/]*)?)$"
)
SECRET_CONTENT_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA |PGP )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\b(?:gh[pousr]_|github_pat_|xox[baprs]-)[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
    re.compile(r"\bsk-(?:live|test)-[A-Za-z0-9]{20,}\b"),
    re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|password|secret)"
        r"\b\s*[:=]\s*[\"']?([A-Za-z0-9_./+=-]{20,})[\"']?"
    ),
)
PLACEHOLDER_WORDS = re.compile(r"(?i)(example|sample|dummy|placeholder|changeme|redacted|your[-_ ]|<[^>]+>|\$\{)")


def validate_secret_like_files(paths: list[Path], errors: list[str]) -> None:
    for path in paths:
        relative = display(path)
        if SECRET_FILENAME.search(relative):
            errors.append(f"{relative}: secret-like filename is committed")
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".woff", ".woff2"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for pattern in SECRET_CONTENT_PATTERNS:
            match = pattern.search(text)
            if match and not PLACEHOLDER_WORDS.search(match.group(0)):
                errors.append(f"{relative}: secret-like committed content matches {pattern.pattern!r}")
                break


def main() -> int:
    errors: list[str] = []
    paths = tracked_paths()
    validate_json_and_manifests(paths, errors)
    validate_openai_metadata(errors)
    validate_submission_documentation(errors)
    active = validate_frontmatter(errors)
    validate_unsafe_prompt_patterns(active, errors)
    validate_documented_tools(paths, errors)
    validate_secret_like_files(paths, errors)

    if errors:
        print(f"plugin validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"- {error}")
        return 1

    json_count = sum(path.suffix.lower() == ".json" for path in paths)
    print(f"plugin validation passed: {json_count} JSON file(s), {len(active)} active prompt surface(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
