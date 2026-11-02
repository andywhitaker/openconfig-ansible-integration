#!/usr/bin/env bash
#
#    run.sh - Lab lifecycle, integration playbooks, and ansible-test wrappers
#
#    Usage:
#      ./run.sh <command> [options]
#
#    Commands:
#      deploy       Deploy the containerlab topology
#      run          Run the categorized integration playbooks
#      destroy      Destroy the containerlab topology
#      integration  deploy, run, destroy
#      units        ansible-test units (Python 3.13 by default, as in the lab)
#      sanity       ansible-test sanity (in the default container if docker is available)
#      help         Show this help message
#
#    Options:
#      -t, --topo <file>        Containerlab topology file (default: ./dev.clab.yml)
#      -p, --playbooks <file>   Playbook categories (default: ./playbooks.yml)
#      -c, --category <name>    Run only one category (default: all)
#      -q, --quiet              Write Ansible output to tests/output/logs only
#      -a, --all                Continue after a failed playbook
#      --python <version>       Python for units/sanity (default: 3.13)
#
#    A category whose inventory group has no hosts is reported as SKIPPED.
#    Results are written to tests/output/junit/integration.xml and
#    tests/output/integration-summary.md.
#
#    Example:
#      ./run.sh deploy
#      ./run.sh run --category all --quiet --all
#      ./run.sh destroy
#      ./run.sh units
#

set -euo pipefail

cd "$(dirname "$0")"

# --- Defaults ----------------------------------------------------------------

TOPOLOGY_FILE="./dev.clab.yml"
PLAYBOOK_FILE="./playbooks.yml"
CATEGORY=""
RUN_ALL=false
QUIET=false
PYTHON_VERSION="3.13"

OUTPUT_DIR="./output"
LOG_DIR="$OUTPUT_DIR/logs"
RESULTS=()

# --- Logging -----------------------------------------------------------------

log() {
  local bold="\033[1m"
  local color_red="\033[31m"
  local color_green="\033[32m"
  local color_yellow="\033[33m"
  local reset="\033[0m"

  local level="$1"; shift
  local msg="$*"
  case "$level" in
    BOLD) echo -e "${bold}${color_yellow}[INFO]${reset} ${bold}$msg${reset}" ;;
    INFO) echo -e "${color_yellow}[INFO]${reset} $msg" ;;
    OK) echo -e "${color_green}[OK]${reset} $msg" ;;
    SKIP) echo -e "${color_yellow}[SKIPPED]${reset} $msg" ;;
    FAIL) echo -e "${color_red}[FAIL]${reset} $msg" ;;
    *) echo "$msg" ;;
  esac
}

# --- YAML Helpers ------------------------------------------------------------

yaml_categories() {
python3 - "$PLAYBOOK_FILE" << EOF
import sys, yaml
data = yaml.safe_load(open(sys.argv[1]))
for c in data.get("categories", {}): print(c)
EOF
}

yaml_category_hosts() {
python3 - "$PLAYBOOK_FILE" "$1" << EOF
import sys, yaml
data = yaml.safe_load(open(sys.argv[1]))
print(data.get("categories", {}).get(sys.argv[2], {}).get("hosts", "all"))
EOF
}

yaml_playbooks() {
python3 - "$PLAYBOOK_FILE" "$1" << EOF
import sys, yaml
data = yaml.safe_load(open(sys.argv[1]))
cat = sys.argv[2]
for p in data.get("categories", {}).get(cat, {}).get("playbooks", []): print(p)
EOF
}

host_count() {
  local pattern="$1"
  local count
  count="$(ansible "$pattern" --list-hosts 2>/dev/null | sed -n 's/^ *hosts (\([0-9]*\)):.*/\1/p')"
  echo "${count:-0}"
}

# --- Containerlab Lifecycle --------------------------------------------------

start_lab() {
  log INFO "Deploying containerlab topology: $TOPOLOGY_FILE"
  sudo containerlab deploy -t "$TOPOLOGY_FILE" --reconfigure
  log OK "Containerlab deployed successfully"
}

stop_lab() {
  log INFO "Destroying containerlab topology"
  sudo containerlab destroy -t "$TOPOLOGY_FILE" || true
  log OK "Containerlab destroyed"
}

# --- Results -----------------------------------------------------------------

# Each result: category|playbook|status|seconds|message
record() {
  RESULTS+=("$1|$2|$3|$4|${5:-}")
}

xml_escape() {
  local s="$1"
  s="${s//&/&amp;}"
  s="${s//</&lt;}"
  s="${s//>/&gt;}"
  s="${s//\"/&quot;}"
  echo "$s"
}

write_reports() {
  local junit="$OUTPUT_DIR/junit/integration.xml"
  local summary="$OUTPUT_DIR/integration-summary.md"
  local total=0 failures=0 skipped=0 entry category playbook status seconds message

  mkdir -p "$OUTPUT_DIR/junit"
  for entry in ${RESULTS[@]+"${RESULTS[@]}"}; do
    IFS='|' read -r category playbook status seconds message <<< "$entry"
    total=$((total + 1))
    [[ "$status" == "failed" ]] && failures=$((failures + 1))
    [[ "$status" == "skipped" ]] && skipped=$((skipped + 1))
  done

  {
    echo '<?xml version="1.0" encoding="UTF-8"?>'
    echo "<testsuites><testsuite name=\"integration\" tests=\"$total\" failures=\"$failures\" skipped=\"$skipped\">"
    for entry in ${RESULTS[@]+"${RESULTS[@]}"}; do
      IFS='|' read -r category playbook status seconds message <<< "$entry"
      echo -n "  <testcase classname=\"$(xml_escape "$category")\" name=\"$(xml_escape "$playbook")\" time=\"$seconds\">"
      case "$status" in
        failed) echo -n "<failure message=\"$(xml_escape "$message")\"/>" ;;
        skipped) echo -n "<skipped message=\"$(xml_escape "$message")\"/>" ;;
      esac
      echo "</testcase>"
    done
    echo "</testsuite></testsuites>"
  } > "$junit"

  {
    echo "### Integration results"
    echo
    echo "$((total - failures - skipped)) passed, $failures failed, $skipped skipped"
    echo
    echo "| Category | Playbook | Result | Time |"
    echo "| --- | --- | --- | --- |"
    for entry in ${RESULTS[@]+"${RESULTS[@]}"}; do
      IFS='|' read -r category playbook status seconds message <<< "$entry"
      echo "| $category | $playbook | $status${message:+ ($message)} | ${seconds}s |"
    done
  } > "$summary"

  log INFO "Results: $junit, $summary"
}

# --- Playbook Runner ---------------------------------------------------------

run_playbook() {
  local category="$1"
  local pb="$2"
  local start_time result=0 duration logfile
  start_time=$(date +%s)
  logfile="$LOG_DIR/${category}__$(basename "$pb" .yml).log"

  set +e
  if $QUIET; then
    log INFO "Running: ansible-playbook $pb"
    ansible-playbook "$pb" > "$logfile" 2>&1
    result=$?
  else
    log BOLD "Running: ansible-playbook $pb"
    ANSIBLE_FORCE_COLOR=true ansible-playbook "$pb" 2>&1 | tee "$logfile" | sed 's/^/    /'
    result=${PIPESTATUS[0]}
  fi
  set -e

  duration=$(( $(date +%s) - start_time ))

  if [[ $result -eq 130 ]]; then
    log FAIL "Execution interrupted by user (Ctrl-C)"
    exit "$result"
  elif [[ $result -ne 0 ]]; then
    log FAIL "$pb failed after ${duration}s (log: $logfile)"
    record "$category" "$pb" failed "$duration" "exit code $result"
    TEST_FAILED=true
    if ! $RUN_ALL; then
      write_reports
      exit 1
    fi
  else
    log OK "$pb succeeded in ${duration}s"
    record "$category" "$pb" passed "$duration"
  fi
}

# --- Test Orchestration ------------------------------------------------------

run_tests() {
  local category hosts count playbook
  TEST_FAILED=false
  mkdir -p "$LOG_DIR"
  log INFO "Running playbooks from $PLAYBOOK_FILE"
  for category in $(yaml_categories); do
    if [[ -n "$CATEGORY" && "$CATEGORY" != "all" && "$CATEGORY" != "$category" ]]; then
      continue
    fi

    log INFO "=== CATEGORY: $category ==="
    hosts="$(yaml_category_hosts "$category")"
    count="$(host_count "$hosts")"
    if [[ "$count" -eq 0 ]]; then
      log SKIP "$category: no hosts in inventory group '$hosts'"
      while IFS= read -r playbook; do
        record "$category" "$playbook" skipped 0 "no hosts in $hosts"
      done < <(yaml_playbooks "$category")
      continue
    fi

    while IFS= read -r playbook; do
      run_playbook "$category" "$playbook"
    done < <(yaml_playbooks "$category")
  done

  write_reports
  if $TEST_FAILED; then
    exit 1
  fi
}

# --- Sequences ---------------------------------------------------------------

integration_run() {
  log INFO "Starting full integration sequence"
  start_lab
  local status=0
  ( run_tests ) || status=$?
  stop_lab
  if [[ $status -ne 0 ]]; then
    exit "$status"
  fi
  log OK "Integration sequence completed"
}

units_run() {
  ../tools/ansible_test.sh units --venv --python "$PYTHON_VERSION"
}

sanity_run() {
  if docker info > /dev/null 2>&1; then
    ../tools/ansible_test.sh sanity --docker default
  else
    log INFO "docker not available, running sanity in a venv for Python $PYTHON_VERSION only"
    ../tools/ansible_test.sh sanity --venv --python "$PYTHON_VERSION"
  fi
}

# --- CLI ---------------------------------------------------------------------

COMMAND="${1:-help}"
shift || true

while [[ $# -gt 0 ]]; do
  case "$1" in
    -t|--topo) TOPOLOGY_FILE="$2"; shift 2 ;;
    -p|--playbooks) PLAYBOOK_FILE="$2"; shift 2 ;;
    -c|--category) CATEGORY="$2"; shift 2 ;;
    -q|--quiet) QUIET=true; shift ;;
    -a|--all) RUN_ALL=true; shift ;;
    --python) PYTHON_VERSION="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

case "$COMMAND" in
  deploy) start_lab ;;
  run) run_tests ;;
  destroy) stop_lab ;;
  integration) integration_run ;;
  units) units_run ;;
  sanity) sanity_run ;;
  help) grep '^#  ' "$0" | sed 's/^# \{0,4\}//'; exit 0 ;;
  *) echo "Usage: $0 {deploy|run|destroy|integration|units|sanity|help}"; exit 1 ;;
esac
