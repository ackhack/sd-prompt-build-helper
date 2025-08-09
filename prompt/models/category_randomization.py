from dataclasses import dataclass

#Represents the randomization properties of a category
@dataclass
class CategoryRandomization:
    #If prompts should be randomly added to the final prompt
    randomized: bool
    #Max amount of prompts to add to the final prompt, negative number for all
    max_prompts: int
    #Min amount of prompts to add to the final prompt, negative number for all
    min_prompts: int
