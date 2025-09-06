import argparse, json, os
from datetime import datetime

#Specifies where logs are kepy
RUN_DIR = "data/logs"

def main():

    #Creates command line parser object
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["clean", "attack"], default="clean")
    parser.add_argument("--policy", choices=["normal", "strict"], default="normal")
    args = parser.parse_args()

    #Ensures log directory already exists
    os.makedirs(RUN_DIR, exist_ok=True)
    run_id = f"run-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

    #Creates JSON record
    record = {
        "run_id": run_id,
        "mode": args.mode,
        "policy": args.policy,
        "message": "Day-1 sanity check: pipeline placeholder executed."
    }

    #Writes JSON records
    with open(os.path.join(RUN_DIR, f"{run_id}.jsonl"), "w", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    print(f"[OK] {record}")

if __name__ == "__main__":
    main()