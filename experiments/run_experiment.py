from core.runner import run as run_single
from utils.io import load_json
from pathlib import Path
from core.diagram_parser import load_mermaid_file


def run_all():

    base_ai = load_json("prompts/base_ai.json")

    experiments = []

    apps = [
        ("moodle", "requirements/moodle_requirements.json", "prompts/apps/moodle.json", "diagrams/moodle.mmd"),
        ("opencart", "requirements/opencart_requirements.json", "prompts/apps/opencart.json", "diagrams/opencart.mmd"),
        ("emr", "requirements/openemr_requirements.json", "prompts/apps/emr.json", "diagrams/openemr.mmd"),
    ]

    # =========================
    # AI BASIC (3 runs)
    # =========================
    for app, req, app_cfg, uml in apps:
        for i in range(1, 4):
            experiments.append({
                "name": f"{app}_AI_BASIC_run{i}",
                "req": req,
                "app": app_cfg,
                "uml": None,
                "mode": "AI",
                "out": f"outputs/ai_basic/{app}_run{i}.json"
            })

    # =========================
    # AI ADVANCED (3 runs)
    # =========================
    for app, req, app_cfg, uml in apps:
        for i in range(1, 4):
            experiments.append({
                "name": f"{app}_AI_ADV_run{i}",
                "req": req,
                "app": app_cfg,
                "uml": None,
                "mode": "AI_ADV",
                "out": f"outputs/ai_advanced/{app}_run{i}.json"
            })

    # =========================
    # MBT UML (3 runs)
    # =========================
    for app, req, app_cfg, uml in apps:
        for i in range(1, 4):
            experiments.append({
                "name": f"{app}_MBT_run{i}",
                "req": req,
                "app": app_cfg,
                "uml": uml,
                "mode": "MBT",
                "out": f"outputs/mbt/{app}_run{i}.json"
            })

    # =========================
    # RUN ALL
    # =========================
    for exp in experiments:

        # uml_data = load_json(exp["uml"]) if exp["uml"] else None
        uml_data = (
            load_mermaid_file(exp["uml"])
            if exp["uml"]
            else None
        )
        print(f"\nRunning: {exp['name']}")

        run_single(
            requirements=load_json(exp["req"]),
            base_prompt=base_ai,
            app_config=load_json(exp["app"]),
            output_path=exp["out"],
            uml=uml_data,
            mode=exp["mode"]
        )


if __name__ == "__main__":
    run_all()