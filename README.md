# Optimal-Thief

CORE IDEA:

The player has a limited-capacity bag and must choose the best combination of items to maximize total value without exceeding the weight limit.

This game demonstrates the Knapsack Problem, a classic optimization problem in computer science.

LEARNING OBJECTIVES:

• Knapsack Problem (0/1 Knapsack concept)
• Optimization and decision making
• Brute-force vs smart selection thinking
• Trade-off between weight and value

GAMEPLAY FLOW:

① Title Screen
Displays game name and instructions.

② Bag Capacity
Shows the maximum weight the player can carry.

③ Item List
A list of items is shown.

④ Each Item Has:
• Weight
• Value

⑤ Player Selection
Player clicks items to add or remove them from the bag.

⑥ Live Tracking
Shows:
• Total weight
• Total value

⑦ Confirm Selection
Player locks in chosen items.

⑧ Result Screen
Shows outcome:
• Invalid (over capacity)
• Valid but not optimal
• Optimal or near-optimal solution

RULES:

• If total weight > capacity → LOSE ❌
• If valid but not best → PARTIAL WIN ⚠️
• If best or near-best → WIN 🏆

EXAMPLE:

Bag Capacity: 10

Items:
• Gold Ring → Weight 2, Value 6
• Laptop → Weight 5, Value 10
• Painting → Weight 6, Value 12
• Watch → Weight 3, Value 7

GOAL:

Choose items that give the highest value without exceeding weight 10.

FEATURES:

• Clickable item selection
• Real-time weight/value display
• Confirm button
• One full playable round
• Result screen


Try it out and have fun! Also let me know about any bugs.
