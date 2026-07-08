import json
from experiments.run_experiment import run_ai, run_mbt
from metrics.metrics import coverage, duplicates, traceability

ai_req = json.load(open("data/moodle_requirements.json"))
uml = open("uml/moodle_mbt.mmd").read()

prompt_ai = open("prompts/prompt_ai.txt").read()
prompt_mbt = open("prompts/prompt_mbt.txt").read()

ai_output = run_ai(ai_req, prompt_ai)
mbt_output = run_mbt(ai_req, uml, prompt_mbt)

print("AI DONE")
print("MBT DONE")