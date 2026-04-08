from __future__ import annotations

import os
import random
from typing import Any, Dict, List, Optional

from detector import detect_prompt_injection
from attack_generator import generate_attack

from agent import AdaptiveAgent
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

from models import (
    PromptInjectionObservation,
    PromptInjectionAction,
    PromptInjectionReward,
    EpisodeState,
)
from graders import grade
from tasks.task_definitions import ALL_TASKS, Task


# ✅ Category Mapping
def map_category(cat):
    if cat in ["override", "role_manipulation"]:
        return "jailbreak"
    elif cat == "data_exfiltration":
        return "direct_injection"
    else:
        return "none"


# ── FastAPI app ─────────────────────────────────────────
app = FastAPI(title="Prompt Injection Detector", version="1.0.0")


class PromptInjectionEnv:
    BENCHMARK = "prompt-injection-detector"

    def __init__(self) -> None:
        self.agent = AdaptiveAgent()
        self._tasks: List[Task] = ALL_TASKS
        self._task_index = 0
        self._step = 0
        self._done = False
        self._last_reward: Optional[float] = None
        self._cumulative_reward = 0.0
        self._last_obs: Optional[PromptInjectionObservation] = None

    # ── RESET ───────────────────────────────────────────
    async def reset(self) -> Dict[str, Any]:
        self._task_index = 0
        self._step = 0
        self._done = False
        self._last_reward = None
        self._cumulative_reward = 0.0

        obs = self._make_observation()
        self._last_obs = obs

        return {"observation": obs.model_dump(), "done": False}

    # ── STEP ────────────────────────────────────────────
    async def step(self, action_data: Dict[str, Any]) -> Dict[str, Any]:
        if self._done:
            raise ValueError("Episode is done. Call reset() first.")

        if self._last_obs is None:
            raise ValueError("Call /reset before /step")

        current_task = self._tasks[self._task_index]

        # 🔥 Use mutated input
        input_text = self._last_obs.user_input
        analysis = detect_prompt_injection(input_text, self.agent.weights)

        # 🔥 Category mapping
        raw_category = analysis["categories"][0] if analysis["categories"] else "none"
        mapped_category = map_category(raw_category)

        # 🔥 Build action (FULLY CORRECT)
        action = PromptInjectionAction(
            is_injection=analysis["is_attack"],
            attack_category=mapped_category,
            severity="high" if analysis["score"] > 0.7 else "medium" if analysis["score"] > 0.4 else "low",
            confidence=analysis["score"],
            explanation=f"Detected: {analysis['categories']}",
            recommended_action="block" if analysis["is_attack"] else "allow"
        )

        # 🔥 Grade
        reward_obj: PromptInjectionReward = grade(action, current_task)
        reward_val = reward_obj.total

        self.agent.update(analysis["categories"], reward_val)

        # Update state
        self._last_reward = reward_val
        self._cumulative_reward += reward_val
        self._step += 1

        # Next task
        self._task_index += 1
        done = self._task_index >= len(self._tasks)
        self._done = done

        if not done:
            next_obs = self._make_observation()
        else:
            next_obs = self._last_obs

        self._last_obs = next_obs

        return {
            "observation": next_obs.model_dump(),
            "reward": reward_val,
            "done": done,
            "info": {
                "task_id": current_task.id,
                "reward_breakdown": reward_obj.model_dump(),
                "tasks_remaining": len(self._tasks) - self._task_index,
            },
        }

    # ── STATE ───────────────────────────────────────────
    def state(self) -> Dict[str, Any]:
        return EpisodeState(
            current_task_id=self._tasks[min(self._task_index, len(self._tasks) - 1)].id,
            step=self._step,
            done=self._done,
            last_reward=self._last_reward,
            cumulative_reward=round(self._cumulative_reward, 4),
            task_ids=[t.id for t in self._tasks],
        ).model_dump()

    async def close(self):
        self._done = True

    # ── OBSERVATION ─────────────────────────────────────
    def _make_observation(self) -> PromptInjectionObservation:
        task = self._tasks[self._task_index]

        if random.random() < 0.7:
            mutated_input = generate_attack(task.user_input)
        else:
            mutated_input = task.user_input

        return PromptInjectionObservation(
            task_id=task.id,
            task_description=task.description,
            system_prompt=task.system_prompt,
            user_input=mutated_input,
            context=task.context,
            step=self._step,
            max_steps=len(self._tasks),
            previous_feedback=None,
        )


# ── API ────────────────────────────────────────────────
_env = PromptInjectionEnv()


@app.post("/reset")
async def http_reset():
    return JSONResponse(content=await _env.reset())


@app.post("/step")
async def http_step(action: Dict[str, Any] = {}):
    try:
        return JSONResponse(content=await _env.step(action))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", "7860"))
    uvicorn.run(app, host="0.0.0.0", port=port)