EMR_SYSTEM_PROMPT = """
Generate test cases for an Electronic Medical Records (EMR) system.

Coverage areas:
- patient registration
- medical history
- prescriptions
- appointments
- access control (doctor/nurse/admin)
- data privacy (HIPAA-like rules)
- audit logs

Return ONLY JSON:
{
  "tests": [
    {
      "id": "",
      "requirement": "",
      "title": "",
      "steps": [{"step": ""}],
      "expected_result": "",
      "priority": "",
      "test_type": ""
    }
  ]
}

Generate 50+ test cases.
Ensure strong security and edge case coverage.
"""