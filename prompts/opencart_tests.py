OPENCART_SYSTEM_PROMPT = """
Generate test cases for OpenCart e-commerce platform.

Coverage areas:
- product catalog
- shopping cart
- checkout process
- payments
- coupons & discounts
- user accounts
- order history
- admin panel (basic)
- stock management
- shipping rules

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

Generate at least 60 test cases.
Include:
- positive
- negative
- boundary
- security (SQLi, XSS)
- performance cases
"""