import os
from google import genai
from google.genai import types


class GeminiService:
    """Handles Gemini AI features for the SIWES Management System."""

    MODEL = "gemini-3.8-flash"
    TIMEOUT_MS = 30000  # 30 seconds

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. "
                "Set the environment variable before running the application."
            )

        self.client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                timeout=self.TIMEOUT_MS
            )
        )

    # =========================================================
    # INTERNAL GEMINI REQUEST
    # =========================================================

    def _generate(self, prompt):
        """Send a prompt to Gemini with proper error handling."""

        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        try:
            response = self.client.models.generate_content(
                model=self.MODEL,
                contents=prompt.strip()
            )

        except Exception as error:
            raise RuntimeError(
                f"Gemini request failed: {error}"
            ) from error

        if response is None:
            raise RuntimeError("Gemini returned no response.")

        text = getattr(response, "text", None)

        if not text or not text.strip():
            raise RuntimeError("Gemini returned an empty response.")

        return text.strip()

    # =========================================================
    # LOGBOOK AI
    # =========================================================

    def generate_logbook_entry(self, activities):
        """Generate a professional SIWES logbook entry."""

        if not activities or not activities.strip():
            raise ValueError(
                "Please provide internship activities."
            )

        prompt = f"""
You are an AI assistant inside a SIWES Management System.

The student provided these internship notes:

{activities.strip()}

Turn the notes into a professional SIWES logbook entry.

Use exactly these three sections:

ACTIVITIES:
Rewrite the student's activities professionally.

SKILLS LEARNED:
List the practical or technical skills learned.

CHALLENGES:
List realistic challenges related to the activities.

Rules:
- Do not invent activities.
- Do not exaggerate the student's experience.
- Keep the response concise.
- Make it suitable for an academic SIWES logbook.
"""

        return self._generate(prompt)

    # =========================================================
    # PROGRESS SUMMARY
    # =========================================================

    def generate_progress_summary(self, activities):
        """Generate a short SIWES progress summary."""

        if not activities or not activities.strip():
            raise ValueError(
                "Please provide internship activities."
            )

        prompt = f"""
You are an academic SIWES progress assistant.

Based only on these student activities:

{activities.strip()}

Write a concise professional progress summary.

Include:

1. Main work completed
2. Skills developed
3. Areas for improvement

Do not invent information.
Keep the summary suitable for an internship report.
"""

        return self._generate(prompt)

    # =========================================================
    # CLOSE CLIENT
    # =========================================================

    def close(self):
        """Close the Gemini client cleanly."""

        try:
            self.client.close()
        except Exception:
            pass


# =============================================================
# TEST
# =============================================================

def test_gemini():
    """Test the Gemini connection."""

    print("=" * 60)
    print("GEMINI AI CONNECTION TEST")
    print("=" * 60)

    print("API key:", "LOADED" if os.getenv("GEMINI_API_KEY") else "MISSING")
    print(f"Model: {GeminiService.MODEL}")
    print("Timeout: 30 seconds")
    print()
    print("Connecting to Gemini...")

    service = None

    try:
        service = GeminiService()

        result = service.generate_logbook_entry(
            "I worked on Python programming and connected "
            "an application to a SQLite database."
        )

        print()
        print("Gemini response:")
        print("-" * 60)
        print(result)
        print("-" * 60)
        print()
        print("Gemini connection test successful.")

    except Exception as error:
        print()
        print("Gemini test failed:")
        print(error)

    finally:
        if service is not None:
            service.close()


if __name__ == "__main__":
    try:
        test_gemini()

    except KeyboardInterrupt:
        print("\nTest cancelled.")