import json, os, uuid

class Telemetry:
    def __init__(self, run_id: str, log_dir: str = "data/logs"):
        self.run_id = run_id
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.path = os.path.join(log_dir, f"{run_id}.jsonl")

    #Method to append a single event
    def log(self, kind: str, payload: dict):
        rec = {"type": kind, **payload, "run_id": self.run_id, "_id": str(uuid.uuid4())}
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
