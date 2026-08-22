from __future__ import annotations
from typing import Any

def simulate(dt:float=0.02,duration:float=8.0,target:float=1.0,kp:float=1.25,ki:float=0.5,tau:float=0.75)->dict[str,float]:
    state=0.0; integral=0.0; peak=0.0; effort=0.0; rise_time=duration; reached=False
    for i in range(int(duration/dt)):
        t=(i+1)*dt; error=target-state; integral+=error*dt; cmd=kp*error+ki*integral; effort+=abs(cmd)*dt; state += (cmd-state)/tau*dt; peak=max(peak,state)
        if not reached and state>=0.9*target: rise_time=t; reached=True
    return {"final_error":abs(target-state),"overshoot":max(0.0,peak-target),"rise_time_s":rise_time,"control_effort":effort}

def compare(current:dict[str,float],baseline:dict[str,Any])->dict[str,Any]:
    differences={}; passed=True
    for metric,expected in baseline["metrics"].items():
        value=current[metric]; abs_tol=float(baseline["tolerances"][metric].get("abs",0.0)); rel_tol=float(baseline["tolerances"][metric].get("rel",0.0)); allowed=max(abs_tol,abs(float(expected))*rel_tol); delta=value-float(expected); ok=abs(delta)<=allowed; passed &= ok; differences[metric]={"baseline":expected,"current":value,"delta":delta,"allowed":allowed,"passed":ok}
    return {"passed":passed,"differences":differences}
