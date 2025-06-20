from mcp.server.fastmcp import FastMCP
import random


mcp = FastMCP("Demo")

@mcp.tool()
def generate_random_number(min, max):
    """I can be used to generate a random number between an integer 'min' and an integer 'max'.
    input_value={'max': int, 'min': int}"""
    return random.randint(min, max)

@mcp.tool()
def approve_score(score: int) -> str:
    """I must be used to approve or deny users' scores.
    input_value={'score': int} 
    """
    return "Approved" if score > 50 else "Denied"

# # JZ: HOMEWORK add another tool here!
@mcp.tool()
def choose_icecream(ice_creams: list[str]): 
    """I can be used to help choose a random ice cream flavor"""
    return random.choice(ice_creams)


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='sse')
