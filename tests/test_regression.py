from flight_regression.core import compare,simulate

def test_simulation_is_deterministic()->None:
    assert simulate()==simulate()

def test_comparison_detects_drift()->None:
    metrics=simulate(); baseline={"metrics":dict(metrics),"tolerances":{k:{"abs":0.0,"rel":0.0} for k in metrics}}
    assert compare(metrics,baseline)["passed"]
    baseline["metrics"]["rise_time_s"]+=1.0
    assert not compare(metrics,baseline)["passed"]
