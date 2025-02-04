
async def generate_random_number(max_value: int) -> int:
    import random
    return random.randint(0, max_value)


async def is_approved(score: int) -> str:
    return "Approved" if score > 50 else "Denied"
