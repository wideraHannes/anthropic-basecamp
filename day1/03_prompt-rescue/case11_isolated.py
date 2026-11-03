"""Run a single eval case (default: 11) in isolation, several times, with the real harness.

Loads the prompt (cell 5) and the eval harness (cell 7) straight from Prompt_Rescue_solo.ipynb,
so it tests exactly what is saved on disk. Prints the drafted response and the judge verdict
for every repeat; the judge is a sampled LLM call, so one run is not enough.

    uv run python case11_isolated.py            # case 11, 5 repeats
    uv run python case11_isolated.py 12 3       # case 12, 3 repeats
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(d for d in [HERE, *HERE.parents] if (d / "basecamp_setup.py").is_file())
sys.path.insert(0, str(ROOT))
from basecamp_setup import connect  # noqa: E402

case_id = int(sys.argv[1]) if len(sys.argv) > 1 else 11
repeats = int(sys.argv[2]) if len(sys.argv) > 2 else 5

nb = json.loads((HERE / "Prompt_Rescue_solo.ipynb").read_text(encoding="utf-8"))
cells = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
prompt_cell = next(s for s in cells if "system_prompt = " in s and "class TicketResult" in s)
harness_cell = next(s for s in cells if "EVAL HARNESS" in s)

claude = connect()
ns = {"__name__": "case_runner", "claude": claude, "client": claude.client,
      "MODEL": claude.model, "FAST_MODEL": claude.fast_model, "BIG_MODEL": claude.big_model}
exec(prompt_cell, ns)
exec(harness_cell, ns)

cases_data = ns["_load_cases"](ns["_EVAL_CASES_B64"])
case = next(c for c in cases_data["cases"] if c["id"] == case_id)
subset = {"categories": {case["category"]: {"label": case["category"], "case_ids": [case_id]}},
          "cases": [case]}
client = claude.make_client(timeout=600.0)

print(f"Model: {ns['MODEL']} | case {case_id} ({case['category']}) | gold {case['gold_priority']} "
      f"| prompt {len(ns['system_prompt'])} chars | {repeats} repeats\n")
passes = 0
for i in range(repeats):
    out = ns["run_eval"](client, [ns["system_prompt"]], subset, output_format=ns["TicketResult"])
    r = out["results"][0] if isinstance(out, dict) and "results" in out else out[0]
    passes += bool(r.get("pass"))
    cls = r.get("parsed") or {}
    print(f"--- repeat {i + 1}: {'PASS' if r.get('pass') else 'FAIL'} {r.get('failures') or ''}")
    print(f"priority: {cls.get('priority')}  entities: {cls.get('entities')}")
    print(f"response: {cls.get('response')}")
    print(f"judge:    {r.get('judge_reason')}\n")
print(f"=== case {case_id}: {passes}/{repeats} passed")
