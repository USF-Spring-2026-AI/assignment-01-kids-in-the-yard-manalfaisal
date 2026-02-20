# AI Assignment 01 - Kids in the Yard

# Comparison 
## What tool(s) did you use?
I used ChatGPT to assist with debugging, probability handling logic, and clarifying implementation details for random selection and mapping. I also referenced official Python documentation (to also get a bit of a refresh) for the csv module and the random module.

## If you used an LLM, what was your prompt to the LLM?
I asked targeted questions while implementing specific parts of the project. For example, I asked how to correctly implement weighted random selection in Python, how to convert a probability value into a boolean outcome using random.random(), and how to handle dictionary key errors when working with CSV data. I also asked for clarification on edge cases related to decade-based lookups and probability ranges. 
I basically used the LLM primarily for debugging support and conceptual clarification.

## What differences are there between your implementation and the LLM?
While the LLM provided guidance on probability handling and weighted selection patterns, my final implementation differs in several ways:
- I structured the family tree expansion using a breadth-first traversal style approach with a to_process list.
- I implemented explicit decade clamping (e.g., defaulting to 1950 when earlier decades appear).
- I manually constructed the rank-to-probability dictionary mapping from the CSV file rather than relying on pre-built structures.
- I added backup logic so that if a birth decade is missing from the dataset, the program defaults to a valid decade instead of crashing.

The final structure, organization, and flow control decisions reflect my own design choices.

## What changes would you make to your implementation in general based on suggestions from the LLM?
Based on feedback and suggestions, there are a few improvements I would consider making. First, I would probably move the repeated decade calculation logic into a small helper function so I don't repeat the same code in multiple places. That would make the code cleaner and easier to maintain. I would also improve how the program handles bad or missing data in the CSV files by adding more validation checks. Right now it assumes the data is formatted correctly, so adding safeguards would make it more robust. Finally, I would improve efficiency by replacing pop(0) with deque from the collections module, since removing from the front of a list is less efficient for larger datasets.

## What changes would you refuse to make?
I wouldn't remove the object-oriented structure of the project, because separating everything into classes made the code much easier to organize and understand. It helped keep the responsibilities clear between generating data and building the tree.

I also wouldn't simplify the probability logic in a way that ignore the assignment requirements, like removing the decade-based differences in birth and marriage rates. That was an important part of making the simulation realistic.
