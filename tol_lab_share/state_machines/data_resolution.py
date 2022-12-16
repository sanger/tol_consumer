from statemachine import StateMachine, State


class DataResolution(StateMachine):
    # states
    pending = State("pending", initial=True)
    valid = State("valid")
    invalid = State("invalid")
    resolving = State("resolving")
    resolved = State("resolved")
    error = State("error")

    # transitions
    validation_passed = pending.to(valid) | valid.to(valid) | invalid.to(valid) | resolved.to(resolved)
    validation_failed = pending.to(invalid) | invalid.to(invalid) | valid.to(invalid)
    request_resolution = valid.to(resolving) | resolved.to(resolved)
    resolution_successful = resolving.to(resolved) | resolved.to(resolved)
    resolution_failed = resolving.to(error) | resolved.to(error)
    retrieve_value = resolved.to(resolved)
    retrieve_feedback = invalid.to(invalid) | resolved.to(resolved) | error.to(error)
