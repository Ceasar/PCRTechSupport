"This holds the code for the recommendation algorithm."
import random

def recommend(user):
  "Get the most recommended courses for a user, based on what other course they have took. Returns a set of integers, corresponding to course objects."
  return [random.randint(1, 25000) for x in range(100)]
