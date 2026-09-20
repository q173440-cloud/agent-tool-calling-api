from agent import run_agent

cases = [
    {
        "name": "No Tool",
        "question": "你好",
        "expected": [],
        "require_non_empty": True
    },
    {
        "name": "Single Tool",
        "question": "查询 P001 的库存",
        "expected": ["P001", "12"]
    },
    {
        "name": "Multi Tool",
        "question": "查询订单 A1001。如果已经发货，再查询 P001 的库存。",
        "expected": ["A1001", "已发货", "P001", "12"]
    },
    {
        "name": "Conditional Tool",
        "question": "查询 A1002。如果已发货才查询 P001 的库存。",
        "expected": ["A1002", "处理中"],
        "forbidden_together": ["P001", "12"]
    }
]

for case in cases:
    passed = True

    actual_answer = run_agent(case["question"])
    print("actual_answer:", actual_answer)

    if case.get("require_non_empty", False):
        if not actual_answer:
            passed = False

    for expected in case["expected"]:
        if expected not in actual_answer:
            passed = False
            break

    forbidden_together = case.get("forbidden_together")
    if forbidden_together:
        if all(item in actual_answer for item in forbidden_together):
            passed = False

    if passed:
        print(case["name"] + ":PASS")
    else:
        print(case["name"] + ":FAIL")