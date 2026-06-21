import httpx

from app.config import settings


SOCRATIC_FALLBACK = """Let's think this through together.
1) Restate the problem in one sentence.
2) Identify input size and constraints.
3) Ask: can brute force work first?
4) Which pattern fits best (two pointers, sliding window, prefix sum, etc.)?
5) Test your idea on a small edge case."""


async def get_coaching_response(question: str, topic: str, student_level: str) -> tuple[str, str]:
    if not settings.groq_api_key:
        return (
            f"Topic: {topic} | Level: {student_level}\n{SOCRATIC_FALLBACK}\nQuestion: {question}",
            "fallback",
        )

    headers = {
        "Authorization": "Bearer " + settings.groq_api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.groq_model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Logic AI for AlgoForge. Use Socratic teaching. "
                    "Never reveal full final code directly. Explain why before what. "
                    "Keep the tone friendly and concise."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Student level: {student_level}. Topic: {topic}. "
                    f"Question: {question}"
                ),
            },
        ],
        "temperature": 0.4,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        return content, "groq"
