from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import random


class RandomNumberInput(BaseModel):
    """Input schema for MyCustomTool."""
    #argument: int = Field(int, description="The tool is used for generating random numbers")
    number: int = Field(int, description="A number between 1 and 100.")

class RandomNumber(BaseTool):
    name: str = "Random_Number_Generator"
    description: str = ("Generates a Random Number \
                        There the input for this tool is a variable called 'number' which will be the max limit for a random number generator, you should pick a random number between 1 and 100"
    )
    
    args_schema: Type[BaseModel] = RandomNumberInput

    def _run(self, number):
        return random.randint(0,number)
