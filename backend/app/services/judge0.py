import httpx

from app.config import settings


async def run_code(source_code: str, language_id: int, stdin: str) -> dict:
    """Execute source code on Judge0 and return normalized execution results."""
    if not settings.judge0_rapidapi_key:
        return {
            "stdout": None,
            "stderr": "Judge0 API key not configured.",
            "compile_output": None,
            "status": "Configuration Required",
            "time": None,
            "memory": None,
        }

    headers = {
        "X-RapidAPI-Key": settings.judge0_rapidapi_key,
        "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=60) as client:
        submit_response = await client.post(
            f"{settings.judge0_base_url}/submissions?base64_encoded=false&wait=true",
            headers=headers,
            json={"source_code": source_code, "language_id": language_id, "stdin": stdin},
        )
        submit_response.raise_for_status()
        data = submit_response.json()

    return {
        "stdout": data.get("stdout"),
        "stderr": data.get("stderr"),
        "compile_output": data.get("compile_output"),
        "status": data.get("status", {}).get("description", "Unknown"),
        "time": data.get("time"),
        "memory": data.get("memory"),
    }
