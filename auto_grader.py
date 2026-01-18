from c_executor import run_c_code
from error_mapper import map_error_to_concepts
from mastry_updater import update_mastery


def grade_code(source_code, test_cases):
    results = []
    passed = 0

    for idx, tc in enumerate(test_cases, start=1):
        result = run_c_code(source_code, tc.get("input", ""))

        # ❌ Compile / runtime / timeout errors
        if result["status"] != "success":
            concepts = map_error_to_concepts(result)

            results.append({
                "test": idx,
                "status": result["status"],
                "error": result.get("error", result.get("stderr")),
                "weak_concepts": concepts
            })

            # Penalize weak concepts
            if concepts:
                update_mastery(concepts, success=False)

            continue

        # ✅ Program ran successfully — check output
        output = result["output"].strip()
        expected = tc["expected"].strip()

        if output == expected:
            passed += 1
            results.append({
                "test": idx,
                "status": "passed"
            })
        else:
            concepts = map_error_to_concepts({"status": "wrong_answer"})

            results.append({
                "test": idx,
                "status": "failed",
                "expected": expected,
                "got": output,
                "weak_concepts": concepts
            })

            update_mastery(concepts, success=False)

    # Reinforce logic if ALL tests passed
    if passed == len(test_cases) and passed > 0:
        update_mastery(["logic"], success=True)

    score = passed / len(test_cases) if test_cases else 0.0

    return {
        "passed": passed,
        "total": len(test_cases),
        "score": round(score, 2),
        "details": results
    }
