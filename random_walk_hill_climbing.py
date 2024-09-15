import random
import pandas as pd

def count_safe_queen_pairs(board):
    """Count the number of non-attacking pairs of queens."""
    total_pairs = 28  # Max pairs for 8 queens (n * (n-1) / 2 where n = 8)
    attacking_pairs = 0
    
    for i in range(8):
        for j in range(i + 1, 8):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                attacking_pairs += 1

    return total_pairs - attacking_pairs

def generate_random_board():
    """Generate a random board state for 8 queens."""
    return [random.randint(0, 7) for _ in range(8)]

def random_board_neighbor(board):
    """Generate a random neighbor by changing the position of one queen."""
    column = random.randint(0, 7)  # Random column
    row = random.randint(0, 7)  # Random row
    while board[column] == row:
        row = random.randint(0, 7)  # Ensure the new row is different
    
    new_board = list(board)
    new_board[column] = row
    return new_board

def random_walk_hill_climb(board, max_no_improvement_steps, sideways_limit):
    """Perform Random-Walk Hill Climbing with sideways moves."""
    current_board = board
    current_safe_pairs = count_safe_queen_pairs(current_board)
    total_steps = 0
    sideways_steps = 0
    
    while total_steps < max_no_improvement_steps:
        total_steps += 1
        
        # Generate a random neighbor and evaluate it
        neighbor_board = random_board_neighbor(current_board)
        neighbor_safe_pairs = count_safe_queen_pairs(neighbor_board)
        
        # Accept the neighbor even if it's not an improvement (random walk)
        current_board = neighbor_board
        current_safe_pairs = neighbor_safe_pairs
        
        if current_safe_pairs == 28:  # Solution found
            return current_board, current_safe_pairs, total_steps, sideways_steps
        
        sideways_steps += 1
        if sideways_steps >= sideways_limit:
            break

    # Return the state even if not optimal (stuck)
    return current_board, current_safe_pairs, total_steps, sideways_steps

def simulate_random_walk(num_trials, max_no_improvement_steps, sideways_limit):
    """Run Random-Walk Hill Climbing simulations and return results."""
    successes = 0
    total_success_steps = 0
    total_stuck_steps = 0
    total_success_sideways = 0
    total_stuck_sideways = 0
    stuck_cases = 0
    
    for _ in range(num_trials):
        final_board, final_safe_pairs, steps, sideways_steps = random_walk_hill_climb(
            generate_random_board(), max_no_improvement_steps, sideways_limit
        )
        
        if final_safe_pairs == 28:  # Success
            successes += 1
            total_success_steps += steps
            total_success_sideways += sideways_steps
        else:  # Stuck
            stuck_cases += 1
            total_stuck_steps += steps
            total_stuck_sideways += sideways_steps

    # Calculate success rate, average steps, and sideways moves
    success_rate = (successes / num_trials) * 100
    stuck_rate = (stuck_cases / num_trials) * 100

    avg_success_steps = total_success_steps / successes if successes > 0 else 0
    avg_stuck_steps = total_stuck_steps / stuck_cases if stuck_cases > 0 else 0

    avg_success_sideways = total_success_sideways / successes if successes > 0 else 0
    avg_stuck_sideways = total_stuck_sideways / stuck_cases if stuck_cases > 0 else 0
    
    return [
        success_rate, stuck_rate, 
        avg_success_steps, avg_stuck_steps, 
        avg_success_sideways, avg_stuck_sideways
    ]

# Parameters
num_trials = 1000
max_no_improvement_steps = 200
sideways_limits = 100

# Run Random-Walk Hill Climbing simulation for each limit
sim_results = []
for limit in sideways_limits:
    rwc_results = simulate_random_walk(num_trials, max_no_improvement_steps, limit)
    sim_results.append([limit] + rwc_results)

# Create a DataFrame to display the results
random_walk_df = pd.DataFrame(
    sim_results,
    columns=[
        'Sideways Moves Limit', 'Success Rate (%)', 'Stuck Rate (%)', 
        'Avg Steps (Success)', 'Avg Steps (Stuck)', 
        'Avg Sideways Moves (Success)', 'Avg Sideways Moves (Stuck)'
    ]
)

# Print the results
print(random_walk_df.to_string(index=False))
