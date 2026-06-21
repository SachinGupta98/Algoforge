from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.schemas import CoachRequest, CoachResponse, ExecuteRequest, ExecuteResponse
from app.services.judge0 import run_code
from app.services.logic_ai import get_coaching_response

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health() -> dict:
    return {"status": "ok", "service": settings.app_name}


@app.get("/api/roadmap")
async def roadmap() -> dict:
    return {
        "phase_1": [
            "Smart dashboard MVP",
            "Arrays + Strings starter problem bank",
            "Judge0-powered coding workspace",
            "Logic AI Socratic coaching",
        ],
        "phase_2": [
            "Voice input coach mode",
            "Hindi / regional language mode",
            "Interview simulation mode",
            "Pattern recognition engine",
        ],
        "theme": "amber/orange",
    }


@app.get("/api/problems")
async def list_problems() -> dict:
    return {
        "items": [
            {
                "id": "two-sum",
                "title": "Two Sum",
                "difficulty": "Easy",
                "forge_difficulty": 3,
                "topic": "Arrays",
                "statement": "Given an integer array nums and an integer target, return indices of two numbers such that they add up to target.",
                "starter_code": {
                    "python": "def two_sum(nums, target):\n    # write your solution\n    return []",
                    "cpp": "#include <vector>\nusing namespace std;\nvector<int> twoSum(vector<int>& nums, int target) {\n    return {};\n}",
                    "java": "class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        return new int[]{};\n    }\n}",
                    "c": "#include <stdio.h>\nint main(){\n    return 0;\n}",
                },
                "hints": [
                    "Can you remember what you've seen before while scanning left to right?",
                    "What data structure gives O(1) lookup for complements?",
                    "Try a hash map: complement = target - nums[i]",
                ],
            }
        ]
    }


@app.post("/api/ai/coach", response_model=CoachResponse)
async def ai_coach(request: CoachRequest) -> CoachResponse:
    try:
        reply, provider = await get_coaching_response(request.question, request.topic, request.student_level)
        return CoachResponse(reply=reply, provider=provider)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"AI coach failed: {exc}") from exc


@app.post("/api/code/execute", response_model=ExecuteResponse)
async def execute_code(request: ExecuteRequest) -> ExecuteResponse:
    try:
        result = await run_code(request.source_code, request.language_id, request.stdin)
        return ExecuteResponse(**result)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"Code execution failed: {exc}") from exc
