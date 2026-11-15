"""Run one test scenario of the b6 plugin with a simulated user.

Usage (macOS):   python3 -I testy/spust.py S1 [--model opus] [--projekt DIR] [--max-kol N] [--timeout MIN] [--sucho]
Usage (Windows): py -3 -I testy/spust.py S1 ...

The main chat runs `claude -p` with the plugin loaded; a second `claude -p` (sonnet, no plugin)
plays the user. The project copy lives in a temporary folder outside any git repository (so the
chat sees no git and no client CLAUDE.md). The transcript and a copy of the final project are written
to testy/vysledky/<ID>-<time>/. These runs spend the usage limit of the account, so `--sucho` only
prints the commands.
"""
import argparse
import hashlib
import json
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

TESTY = Path(__file__).resolve().parent
PLUGIN_DIR = TESTY.parent / "b6"
SCENARE = TESTY / "scenare.md"
VYSLEDKY = TESTY / "vysledky"

DEFAULT_MODEL = "opus"
SIMULATOR_MODEL = "sonnet"
DEFAULT_TIMEOUT_MINUTES = 45
DEFAULT_MAX_ROUNDS = 10
# Isolation: no MCP servers and no user-level plugins or settings, so the test sees only the b6 plugin.
IZOLACIA = ["--strict-mcp-config", "--setting-sources", "project,local"]
# The runner must run outside a sandbox (claude saves sessions under ~/.claude for --resume), so the
# test chat's own Bash commands are kept in a sandbox without network access.
# Automatic memory is off, so a run cannot store state outside the project or carry it over to the next run.
# Claude Code on Windows has no sandbox, so there the test chat runs without it (owner's decision 2026-11-15):
# it still has only the allowed tools below, a temporary folder, a made-up project, no MCP and no memory.
SANDBOX_SETTINGS = {"autoMemoryEnabled": False}
if sys.platform != "win32":
    SANDBOX_SETTINGS["sandbox"] = {"enabled": True, "failIfUnavailable": True, "allowUnsandboxedCommands": False,
                                   "network": {"strictAllowlist": True}}
SANDBOX = ["--settings", json.dumps(SANDBOX_SETTINGS)]
ALLOWED_TOOLS = "Read,Write,Edit,Glob,Grep,Task,Agent,Skill,Bash(python3:*),Bash(ls:*),Bash(rm:*),Bash(git:*)"
if sys.platform == "win32":  # on Windows Python is usually started as `python` or `py`
    ALLOWED_TOOLS += ",Bash(python:*),Bash(py:*)"
SHOWN_DIRS = ("ctx", "docs")
SHOWN_FILES = ("CLAUDE.md",)
IGNORED_NAMES = {"__pycache__"}


class ScenarioError(Exception):
    """Raised when a scenario is missing or cannot be read."""


# ---------------------------------------------------------------- scenario file

def split_sections(text, level):
    """Split text on headings of the given level; return (intro, [(title, body), ...])."""
    pattern = re.compile(r"^{} (.+?)\s*$".format("#" * level), re.MULTILINE)
    matches = list(pattern.finditer(text))
    if not matches:
        return text, []
    sections = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((match.group(1), text[match.end():end].strip()))
    return text[:matches[0].start()], sections


def phase_from_fields(fields):
    return {
        "persona": fields.get("Persona", ""),
        "first": fields.get("Prvá správa", ""),
        "max_rounds": int(fields.get("Max kôl", DEFAULT_MAX_ROUNDS)),
    }


def load_scenario(scenario_id):
    """Return {'project': str, 'phases': [{'persona', 'first', 'max_rounds'}]}."""
    text = SCENARE.read_text(encoding="utf-8")
    _, scenarios = split_sections(text, 2)
    body = dict(scenarios).get(scenario_id)
    if body is None:
        known = ", ".join(title for title, _ in scenarios)
        raise ScenarioError("Scenario {} not found in scenare.md (known: {})".format(scenario_id, known))
    _, fields_list = split_sections(body, 3)
    fields = dict(fields_list)
    phases = []
    for title, phase_body in fields_list:
        if title.startswith("Fáza"):
            _, sub = split_sections(phase_body, 4)
            phases.append(phase_from_fields(dict(sub)))
    if not phases:
        phases.append(phase_from_fields(fields))
    return {"project": fields.get("Projekt", "projekt").strip(), "phases": phases}


# ---------------------------------------------------------------- commands

def find_claude():
    """Return the path of the claude command, or None."""
    for name in ("claude", "claude.cmd"):
        found = shutil.which(name)
        if found:
            return found
    return None


def main_chat_command(claude, model, session_id):
    """The message goes in through stdin, so the command carries no message."""
    command = [claude, "-p", "--plugin-dir", str(PLUGIN_DIR), "--model", model,
               "--output-format", "json", "--permission-mode", "acceptEdits",
               *IZOLACIA, *SANDBOX,
               "--allowedTools", ALLOWED_TOOLS]
    if session_id:
        command += ["--resume", session_id]
    return command


def simulator_command(claude):
    """The prompt goes in through stdin; `--tools ""` switches all built-in tools off."""
    return [claude, "-p", "--model", SIMULATOR_MODEL, "--output-format", "json", "--tools", "", *IZOLACIA, *SANDBOX]


def build_simulator_prompt(persona, transcript):
    lines = ["You play a user chatting with an AI assistant. Stay in the role below. Do not use any tools.",
             "", "ROLE:", persona, "", "CONVERSATION SO FAR:"]
    for speaker, text in transcript:
        lines += ["{}: {}".format("You" if speaker == "user" else "Assistant", text), ""]
    lines += ["Reply with ONLY your next message to the assistant, in the language of your role.",
              "If your role says the conversation is over, reply with the single word END."]
    return "\n".join(lines)


def print_dry_run(scenario, args, claude):
    model = args.model
    print("Dry run - nothing is started.")
    print("Scenario {}: project '{}', {} phase(s)".format(args.id, scenario["project"], len(scenario["phases"])))
    print("Project copy runs in a temporary folder; the final copy goes to {}/<{}-time>/projekt/".format(
        VYSLEDKY, args.id))
    print("Timeout per call: {} minutes".format(args.timeout))
    for number, phase in enumerate(scenario["phases"], 1):
        max_rounds = args.max_kol or phase["max_rounds"]
        print("\n--- Phase {} (max {} rounds, new chat) ---".format(number, max_rounds))
        print("First round (cwd = project copy, message on stdin: {!r}):".format(phase["first"]))
        print("  " + shlex.join(main_chat_command(claude, model, None)))
        print("Next round (cwd = project copy, stdin = the simulated user message):")
        print("  " + shlex.join(main_chat_command(claude, model, "<session_id>")))
    print("\nSimulated user (cwd = empty temp folder, prompt on stdin):")
    print("  " + shlex.join(simulator_command(claude)))


# ---------------------------------------------------------------- running claude

def run_claude(command, cwd, timeout_minutes, stdin_text=None):
    """Run a command and return (parsed JSON or None, raw stdout, error text)."""
    try:
        done = subprocess.run(command, cwd=str(cwd), input=stdin_text, capture_output=True,
                              text=True, encoding="utf-8", timeout=timeout_minutes * 60)
    except subprocess.TimeoutExpired:
        return None, "", "Timeout after {} minutes".format(timeout_minutes)
    error = "" if done.returncode == 0 else "Exit code {}: {}".format(done.returncode, done.stderr[-500:])
    try:
        return json.loads(done.stdout), done.stdout, error
    except ValueError:
        return None, done.stdout, error or "Output was not JSON"


def says_end(reply):
    """True when END is the whole reply, its last line or its last word; the text before it is dropped."""
    words = reply.strip().split()
    return bool(words) and words[-1].strip(".!, ").upper() == "END"


def ask_simulator(claude, persona, transcript, sim_dir, timeout_minutes):
    """Return (next user message, error); message is None when the user says END or the call fails."""
    data, raw, error = run_claude(simulator_command(claude), sim_dir, timeout_minutes,
                                  build_simulator_prompt(persona, transcript))
    reply = data.get("result", "") if isinstance(data, dict) else raw
    reply = reply.strip()
    if error or not reply:
        return None, error or "Simulator returned nothing"
    if says_end(reply):
        return None, ""
    return reply, ""


# ---------------------------------------------------------------- project snapshots

def list_files(project):
    """Relative paths of all files in the project copy."""
    return sorted(path.relative_to(project).as_posix() for path in project.rglob("*")
                  if path.is_file() and not IGNORED_NAMES & set(path.parts))


def file_hashes(root):
    """Map of relative path -> sha256 of the content, for every file under root."""
    return {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in list_files(root)}


def changes_report(start, project):
    """Markdown list of files added, changed and deleted against the starting project."""
    before, after = file_hashes(start), file_hashes(project)
    groups = (("Added", sorted(set(after) - set(before))),
              ("Changed", sorted(n for n in after if n in before and after[n] != before[n])),
              ("Deleted", sorted(set(before) - set(after))))
    lines = ["## Changes against the starting project", ""]
    for title, names in groups:
        lines += ["### {} ({})".format(title, len(names))] + ["- " + name for name in names] + [""]
    return "\n".join(lines)


def snapshot_line(project):
    visible = [name for name in list_files(project) if name.split("/")[0] in SHOWN_DIRS + ("MARKER.txt",)]
    return "Files in ctx/ and docs/ now: " + (", ".join(visible) if visible else "(none)")


def final_report(project):
    lines = ["## Final state of the project copy", "", "### All files", ""]
    lines += ["- " + name for name in list_files(project)]
    marker = (project / "MARKER.txt").exists()
    lines += ["", "MARKER.txt exists: {}".format("YES" if marker else "no"), ""]
    shown = [name for name in list_files(project)
             if name.split("/")[0] in SHOWN_DIRS or name in SHOWN_FILES]
    for name in shown:
        content = (project / name).read_text(encoding="utf-8", errors="replace")
        lines += ["### " + name, "", "~~~", content.rstrip(), "~~~", ""]
    return "\n".join(lines)


# ---------------------------------------------------------------- main flow

def append(path, text):
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def run_phase(number, phase, args, claude, project, sim_dir, prepis):
    """Run one chat (phase). Return its total cost."""
    append(prepis, "\n## Phase {}\n".format(number))
    max_rounds = args.max_kol or phase["max_rounds"]
    transcript, session_id, total_cost, message = [], None, 0.0, phase["first"]
    for round_number in range(1, max_rounds + 1):
        transcript.append(("user", message))
        append(prepis, "\n### Round {} - user\n\n{}\n".format(round_number, message))
        data, raw, error = run_claude(main_chat_command(claude, args.model, session_id), project, args.timeout, message)
        answer = data.get("result", "") if isinstance(data, dict) else raw[-2000:]
        info = data if isinstance(data, dict) else {}
        session_id = info.get("session_id", session_id)
        cost = info.get("total_cost_usd")
        # With --resume, total_cost_usd is the running total of the whole session, so keep the latest value.
        total_cost = max(total_cost, cost or 0.0)
        transcript.append(("assistant", answer))
        append(prepis, "\n### Round {} - assistant{}\n\n{}\n\n{}\n".format(
            round_number, " (cost ${:.2f})".format(cost) if cost else "", answer, snapshot_line(project)))
        if error:
            append(prepis, "\nERROR in main chat: {}\n".format(error))
            break
        message, sim_error = ask_simulator(claude, phase["persona"], transcript, sim_dir, args.timeout)
        if message is None:
            append(prepis, "\nPhase ended: {}\n".format(sim_error or "simulated user said END"))
            break
    else:
        append(prepis, "\nPhase ended: maximum rounds ({}) reached\n".format(max_rounds))
    return total_cost


def resolve_start_project(name):
    candidate = Path(name)
    if candidate.is_dir():
        return candidate.resolve()
    return TESTY / name


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Run one b6 plugin test scenario.")
    parser.add_argument("id", help="scenario ID, for example S1")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="model of the main chat (default opus)")
    parser.add_argument("--projekt", help="starting project folder (name in testy/ or a path)")
    parser.add_argument("--max-kol", type=int, help="maximum rounds per phase")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_MINUTES,
                        help="minutes allowed for one claude call (default {})".format(DEFAULT_TIMEOUT_MINUTES))
    parser.add_argument("--sucho", action="store_true", help="print the commands, run nothing")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        scenario = load_scenario(args.id)
    except (ScenarioError, OSError) as problem:
        print("Error: {}".format(problem))
        return 2
    claude = find_claude()
    if args.sucho:
        print_dry_run(scenario, args, claude or "claude")
        return 0
    if not claude:
        print("Error: the claude command was not found on PATH.")
        return 2
    start = resolve_start_project(args.projekt or scenario["project"])
    if not start.is_dir():
        print("Error: starting project folder not found: {}".format(start))
        return 2
    run_dir = VYSLEDKY / "{}-{}".format(args.id, datetime.now().strftime("%Y-%m-%d_%H%M%S"))
    run_dir.mkdir(parents=True)
    work_root = Path(tempfile.mkdtemp(prefix="b6-test-"))
    try:
        return run_scenario(args, scenario, claude, start, run_dir, work_root)
    finally:
        shutil.rmtree(str(work_root), ignore_errors=True)


def git_state_above(folder):
    """Return 'none', 'found' or 'unknown' (git missing) for a git repository above the folder."""
    if not shutil.which("git"):
        return "unknown"
    done = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=str(folder),
                          capture_output=True, text=True, encoding="utf-8")
    return "found" if done.returncode == 0 and done.stdout.strip() else "none"


def run_scenario(args, scenario, claude, start, run_dir, work_root):
    project = work_root / "projekt"
    sim_dir = work_root / "simulator"
    shutil.copytree(str(start), str(project), ignore=shutil.ignore_patterns(*IGNORED_NAMES))
    sim_dir.mkdir()
    git_state = git_state_above(project)
    if git_state == "found":
        print("Error: the temporary folder {} lies inside a git repository; set TMPDIR elsewhere.".format(work_root))
        return 2
    if git_state == "unknown":
        print("Warning: git was not found, so the absence of git above the project copy was not checked.")
    prepis = run_dir / "prepis.md"
    prepis.write_text("# Scenario {} - {}\n\nProject: {}\nModel: {}\nPlugin: {}\nGit above the copy: {}\n".format(
        args.id, datetime.now().strftime("%Y-%m-%d %H:%M"), start.name, args.model, PLUGIN_DIR, git_state),
        encoding="utf-8")
    total = 0.0
    for number, phase in enumerate(scenario["phases"], 1):
        total += run_phase(number, phase, args, claude, project, sim_dir, prepis)
    append(prepis, "\nTotal cost: ${:.2f}\n\n{}\n{}\n".format(
        total, changes_report(start, project), final_report(project)))
    shutil.copytree(str(project), str(run_dir / "projekt"), ignore=shutil.ignore_patterns(*IGNORED_NAMES))
    print("Done. Transcript: {}".format(prepis))
    return 0


if __name__ == "__main__":
    sys.exit(main())
