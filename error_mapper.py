def map_error_to_concepts(exec_result):
    status = exec_result["status"]

    if status == "compile_error":
        return ["syntax", "declarations"]

    if status == "timeout":
        return ["loops", "conditions"]

    if status == "runtime_error":
        return ["pointers", "memory"]

    if status == "wrong_answer":
        return ["logic", "operators"]

    return []
