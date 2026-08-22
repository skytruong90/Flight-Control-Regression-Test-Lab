from __future__ import annotations
import argparse,json
from pathlib import Path
from .core import compare,simulate

def main()->None:
    p=argparse.ArgumentParser(description="Synthetic flight-control regression checker"); sub=p.add_subparsers(dest="cmd",required=True)
    run=sub.add_parser("run"); run.add_argument("--baseline",required=True); run.add_argument("--output",default="output/report.json")
    cap=sub.add_parser("capture"); cap.add_argument("--output",default="output/candidate-baseline.json")
    a=p.parse_args(); metrics=simulate()
    if a.cmd=="capture": result={"metrics":metrics,"tolerances":{k:{"rel":0.03,"abs":0.001} for k in metrics}}
    else: result=compare(metrics,json.loads(Path(a.baseline).read_text(encoding="utf-8")))
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2),encoding="utf-8"); print(json.dumps(result,indent=2))
    if a.cmd=="run" and not result["passed"]: raise SystemExit(2)
