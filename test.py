import requests
res = requests.post("http://localhost:8000/api/grade", json={
    "code": "#include <stdio.h>\nint main() { int a, b; scanf(\"%d %d\", &a, &b); printf(\"%d\", a+b); return 0; }",
    "test_cases": [{"input": "3 4", "expected": "7"}, {"input": "10 20", "expected": "30"}]
})
print(res.json())
