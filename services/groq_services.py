import os
from groq import Groq


class GroqService:
    """AI service for the SIWES Management System."""

    MODEL = "openai/gpt-oss-20b"

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not configured. "
                "Set the environment variable before using the AI service."
            )

        self.client = Groq(api_key=api_key)

    def _generate(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an AI assistant for a SIWES Management "
                            "System. Help students write clear, professional "
                            "and truthful internship logbook entries. "
                            "Never invent activities or experiences."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.4,
                max_completion_tokens=500,
            )

            result = response.choices[0].message.content

            if not result:
                raise RuntimeError("AI returned an empty response.")

            return result.strip()

        except Exception as exc:
            raise RuntimeError(f"Groq request failed: {exc}") from exc

    def generate_logbook_entry(self, activities):
        """Turn raw student activities into a professional logbook entry."""

        prompt = f"""
Rewrite these student's raw SIWES activities into a professional
logbook entry.

Student activities:
{activities}

Return exactly these sections:

Activities:
Skills Learned:
Challenges:

Keep the information truthful. Do not add activities that were not provided.
"""

        return self._generate(prompt)

    def generate_progress_summary(self, activities):
        """Generate a professional summary of student progress."""

        prompt = f"""
Create a concise professional SIWES progress summary based only on
the following activities:

{activities}

Include:

1. Overall Progress
2. Skills Developed
3. Areas for Improvement
4. Recommended Next Steps

Do not invent information.
"""

        return self._generate(prompt)


def test_groq():
    print("=" * 55)
    print("SIWES AI CONNECTION TEST")
    print("=" * 55)
    print(f"API key: {'LOADED' if os.getenv('GROQ_API_KEY') else 'MISSING'}")
    print(f"Model: {GroqService.MODEL}")
    print("Connecting to Groq...")

    try:
        service = GroqService()

        result = service.generate_logbook_entry(
            "I worked on the student database and learned "
            "how foreign keys connect tables."
        )

        print("\n--- AI RESPONSE ---")
        print(result)
        print("\nAI test successful!")

    except Exception as exc:
        print("\nAI test failed:")
        print(exc)


if __name__ == "__main__":
    test_groq()