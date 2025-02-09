import pandas as pd

df = pd.read_csv("data/boardgames_ranks.csv")

# Drop columns
df = df.drop(columns=["yearpublished", "bayesaverage", "average", "is_expansion", "abstracts_rank", "cgs_rank", "childrensgames_rank", "familygames_rank", "partygames_rank", "strategygames_rank", "thematic_rank", "wargames_rank"])
df = df[df.usersrated >= 100]
df.to_csv("data/cleaned_boardgames_ranks.csv", index=False)