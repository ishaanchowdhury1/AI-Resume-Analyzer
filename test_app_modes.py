"""
Comprehensive Test Script for Resume Analyzer
Tests:
1. Mode 1: No API Key (Built-in Zero-Key ATS Engine)
2. Mode 2: Configured / Invalid API Key (Fallback without key leaks)
3. Text extraction and security audit
"""

import os
import json
from resume_analyzer import analyze_resume, fallback_heuristic_analyzer, extract_text_from_file

SAMPLE_RESUME = """
JOHN DOE
Software Engineer | john@example.com | (555) 123-4567 | linkedin.com/in/johndoe
Experience:
Senior Developer at Tech Corp (2020-Present)
- Developed REST APIs in Python, React, PostgreSQL, reducing query latency by 40%.
- Engineered microservices with AWS and Docker.
Skills: Python, React, SQL, AWS, Docker, Kubernetes
Education: B.S. Computer Science
"""

SAMPLE_JD = """
Senior Full Stack Developer
Looking for a Senior Developer with expertise in Python, React, SQL, and AWS.
Must have experience building microservices and optimizing database performance.
"""

def test_no_api_key_mode():
    print("Testing Mode 1: No API Key provided...")
    res = analyze_resume(SAMPLE_RESUME, SAMPLE_JD, api_key="", provider="Auto-detect")
    
    assert isinstance(res, dict), "Result must be a dictionary"
    assert "match_score" in res, "Missing match_score"
    assert "verdict" in res, "Missing verdict"
    assert "strengths" in res, "Missing strengths"
    assert "missing_skills" in res, "Missing missing_skills"
    assert "matched_skills" in res, "Missing matched_skills"
    assert "bullet_rewrites" in res, "Missing bullet_rewrites"
    assert 0 <= res["match_score"] <= 100, f"Invalid score {res['match_score']}"
    
    # Verify no secret key leakage
    res_str = json.dumps(res)
    assert "gsk_" not in res_str and "sk-" not in res_str, "Key leak detected in result"
    print(f"✅ Mode 1 Passed! Match Score: {res['match_score']}, Skills Matched: {len(res['matched_skills'])}")

def test_configured_api_key_fallback_mode():
    print("Testing Mode 2: Configured API Key (with simulated network/auth handling)...")
    dummy_key = "gsk_test_dummy_key_123456789"
    res = analyze_resume(SAMPLE_RESUME, SAMPLE_JD, api_key=dummy_key, provider="Groq")
    
    assert isinstance(res, dict), "Result must be a dictionary"
    assert "match_score" in res, "Missing match_score"
    
    # Verify dummy API key is NOT leaked in output string or warning
    res_str = json.dumps(res)
    assert dummy_key not in res_str, "CRITICAL SECURITY WARNING: API Key leaked in output!"
    print(f"✅ Mode 2 Passed! API key remained private and safe. Fallback score: {res['match_score']}")

def test_text_extraction():
    print("Testing File Extraction...")
    sample_bytes = SAMPLE_RESUME.encode("utf-8")
    extracted = extract_text_from_file(sample_bytes, "resume.txt")
    assert "JOHN DOE" in extracted, "Text extraction failed"
    print("✅ File extraction passed!")

if __name__ == "__main__":
    print("Beginning Resume Analyzer Verification Suite...\n")
    test_no_api_key_mode()
    test_configured_api_key_fallback_mode()
    test_text_extraction()
    print("\n🎉 ALL VERIFICATION TESTS PASSED SUCCESSFULLY!")
