"""
title: Approver & Scorer Agents Example
author: open-webui
author_url: https://github.com/open-webui
version: 0.1.0
required_open_webui_version: 0.3.9
"""

import random
import asyncio
import os
from typing import Optional, Dict

class Action:
    class Valves:
        # e.g., maximum value for random scores
        max_score: int = 100

    def __init__(self):
        self.valves = self.Valves()

    async def action(
        self,
        body: Dict,
        __user__=None,
        __event_emitter__=None,
        __event_call__=None,
    ) -> Optional[dict]:
        """
        Replicates the pydantic_agents.py logic:
          1. Generate a random score (like 'scorer').
          2. Determine 'approved' or 'denied' (like 'approver').
          3. Loop until the score usage is consistent (just a contrived check here).
        """

        def generate_random_number(max_value: int) -> int:
            return random.randint(0, max_value)

        def is_approved(score: int) -> str:
            return "Approved" if score > 50 else "Denied"

        tool_usage = {}
        running = True

        while running:
            score = generate_random_number(self.valves.max_score)
            tool_usage["generate_random_number_return"] = score

            result = is_approved(score)
            tool_usage["is_approved_call"] = {"score": score, "decision": result}

            if tool_usage["generate_random_number_return"] == tool_usage["is_approved_call"]["score"]:
                running = False

        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "description": f"Done! Score={score}, Decision={result}",
                    "done": True
                }
            })

        return {
            "score": score,
            "decision": result,
            "explanation": f"Score={score}, so the user is {result}."
        }
