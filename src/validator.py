import pandas as pd

# Generic targets that are considered too vague for operational SDN rules
GENERIC_TARGETS = {
    "host", "hosts", "flow", "flows", "service", "services",
    "network", "traffic", "device", "devices", "switch", "switch_port"
}

def infer_specific_target(row):
    """
    Lightweight validator to correct generic targets based on scenario context.
    """
    scenario = str(row.get("scenario", "")).lower()
    category = str(row.get("category", "")).lower()
    current_target = str(row.get("target", "")).strip().lower()

    # If target is already specific, keep it
    if current_target not in GENERIC_TARGETS:
        return row["target"]

    # Rule-based correction logic
    if "switch" in category or "flow-table" in scenario or "s7" in scenario:
        return "switch s7 control-plane or affected switch port"

    if "host" in scenario and "malicious" in scenario:
        return "suspected malicious host"

    if "smb" in scenario:
        return "endpoint initiating SMB connections"

    if "service" in scenario:
        return "affected service endpoint"

    if "flow" in scenario:
        return "suspicious flow"

    return row["target"]

def validate_and_correct(df):
    """Apply validation to a dataframe of LLM outputs."""
    df = df.copy()
    df["original_target"] = df["target"]
    df["target"] = df.apply(infer_specific_target, axis=1)
    
    # Check if correction happened
    df["target_corrected"] = (
        df["original_target"].str.lower().isin(GENERIC_TARGETS) & 
        ~df["target"].str.lower().isin(GENERIC_TARGETS)
    )
    
    return df
