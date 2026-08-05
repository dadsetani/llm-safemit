import pandas as pd
import json
import re
from pathlib import Path
from validator import validate_and_correct, GENERIC_TARGETS

def extract_json(text):
    if pd.isna(text): return None
    text = str(text).strip()
    # Remove Markdown code fences
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match: return None
    try:
        return json.loads(match.group(0))
    except:
        return None

def evaluate_scenario(row, scenarios_df):
    """Evaluate a single parsed output against scenario constraints."""
    errors = []
    
    # Get scenario details
    scenario_row = scenarios_df[scenarios_df['scenario_id'] == row['scenario_id']].iloc[0]
    approval_required = bool(scenario_row.get('human_approval_required', False))
    
    action = str(row.get("action", "")).strip().lower()
    scope = str(row.get("scope", "")).strip().lower()
    target = str(row.get("target", "")).strip().lower()
    
    allowed_actions = {"allow", "monitor", "rate-limit", "isolate", "drop", "escalate"}
    allowed_scopes = {"flow", "host", "service", "switch-port", "switch"}
    
    valid_action = action in allowed_actions
    valid_scope = scope in allowed_scopes
    specific_target = target not in GENERIC_TARGETS and len(target) > 3
    
    if not valid_action: errors.append("bad_action")
    if not valid_scope: errors.append("bad_scope")
    if not specific_target: errors.append("generic_target")
    
    # Policy Compliance Check
    policy_compliant = True
    destructive_action = action in {"drop", "isolate"}
    
    if approval_required and destructive_action:
        policy_compliant = False
        errors.append("policy_violation")
        
    acceptable_action = valid_action and not (action == "drop" and str(scenario_row.get('availability_constraint', '')).lower() == "high")
    
    operationally_good = (
        valid_action and 
        valid_scope and 
        specific_target and 
        acceptable_action and 
        policy_compliant
    )
    
    return pd.Series({
        "valid_action": valid_action,
        "valid_scope": valid_scope,
        "specific_target": specific_target,
        "acceptable_action": acceptable_action,
        "policy_compliant": policy_compliant,
        "operationally_good": operationally_good,
        "error_type": "none" if len(errors) == 0 else "; ".join(sorted(set(errors)))
    })

if __name__ == "__main__":
    print("Evaluation module loaded.")
