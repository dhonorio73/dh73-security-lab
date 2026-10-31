import unittest
from unittest.mock import patch

from checker import (
    HEADER_LABELS,
    RECOMMENDED_HEADERS,
    analyze_headers,
    create_html_report,
    load_response,
)


class AnalyzeHeadersTests(unittest.TestCase):
    def test_detects_present_and_missing_headers(self):
        result = analyze_headers(
            {
                "headers": {
                    "Content-Security-Policy": "default-src 'self'",
                    "X-Content-Type-Options": "nosniff",
                }
            }
        )

        self.assertEqual(
            result["present"],
            ["content-security-policy", "x-content-type-options"],
        )
        self.assertEqual(
            result["missing"],
            sorted(
                set(RECOMMENDED_HEADERS)
                - {"content-security-policy", "x-content-type-options"}
            ),
        )

    def test_header_name_matching_is_case_insensitive(self):
        result = analyze_headers({"headers": {"rEfErReR-pOlIcY": "no-referrer"}})

        self.assertIn("referrer-policy", result["present"])

    def test_accepts_all_recommended_headers(self):
        result = analyze_headers({"headers": dict.fromkeys(RECOMMENDED_HEADERS, "test")})

        self.assertEqual(result["missing"], [])
        self.assertEqual(result["present"], sorted(RECOMMENDED_HEADERS))

    def test_rejects_missing_or_invalid_headers_field(self):
        for response in ({}, {"headers": []}, {"headers": None}):
            with self.subTest(response=response):
                with self.assertRaises(ValueError):
                    analyze_headers(response)

    def test_html_report_shows_present_and_missing_headers(self):
        result = analyze_headers(
            {"headers": {"X-Content-Type-Options": "nosniff"}}
        )

        report = create_html_report(result)

        self.assertIn("X-Content-Type-Options", report)
        self.assertIn(">Presente</span>", report)
        self.assertIn("Content-Security-Policy", report)
        self.assertIn(">Ausente</span>", report)
        self.assertIn("Nenhum site foi acessado.", report)

    def test_html_report_escapes_header_names(self):
        malicious_header = '<script>alert("x")</script>'
        with patch.dict(
            RECOMMENDED_HEADERS,
            {malicious_header: "Cabeçalho de teste"},
        ), patch.dict(HEADER_LABELS, {malicious_header: malicious_header}):
            report = create_html_report(
                {"present": [malicious_header], "missing": []}
            )

        self.assertNotIn("<script>", report)
        self.assertIn("&lt;script&gt;", report)


class LoadResponseTests(unittest.TestCase):
    def test_loads_example_json(self):
        from pathlib import Path

        example = Path(__file__).parents[1] / "examples" / "response.json"
        response = load_response(example)

        self.assertEqual(response["status"], 200)
        self.assertIn("Content-Security-Policy", response["headers"])

    def test_rejects_non_object_json(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.json"
            path.write_text("[]", encoding="utf-8")

            with self.assertRaises(ValueError):
                load_response(path)


if __name__ == "__main__":
    unittest.main()
