import random
import time
import pandas as pd

def safe_queen_pairs(board):
    """Calculate the number of non-attacking pairs of queens."""
    max_pairs = 28  # Max pairs for 8 queens (n * (n-1) / 2 where n = 8)
    attack_pairs = 0
    
    for i in range(8):
        for j in range(i + 1, 8):
            # Check if queens are in the same row or on the same diagonal
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                attack_pairs += 1

    return max_pairs - attack_pairs


def generate_random_board():
    """Generate a random board state for 8 queens."""
    return [random.randint(0, 7) for _ in range(8)]


def hill_climbing_with_random_walk(board, step_limit):
    """Perform Hill Climbing with Random Walk."""
    current_board = board
    current_safe_pairs = safe_queen_pairs(current_board)
    move_count = 0
    random_steps = 0
    
    while True:
        move_count += 1
        neighbor_boards = []
        for column in range(8):
            for row in range(8):
                if current_board[column] != row:
                    new_board = list(current_board)
                    new_board[column] = row
                    neighbor_boards.append((new_board, safe_queen_pairs(new_board)))
        
        board, current_safe_pairs = random.choice(neighbor_boards)
        
        if current_safe_pairs == 28:
            return board, current_safe_pairs, move_count, random_steps
        
        random_steps += 1


def restart_hill_climb_with_time_limit(restart_count, time_limit_per_try):
    """Perform Hill Climbing with Random Restarts and Time Limit."""
    solutions = 0
    total_moves = 0
    retry_attempts = 0
    
    for _ in range(restart_count):
        board = generate_random_board()
        start_time = time.time()
        move_count = 0
        while time.time() - start_time < time_limit_per_try:
            final_board, final_safe_pairs, move_count, _ = hill_climbing_with_random_walk(board, 1000)  # Set a high max steps limit
            if final_safe_pairs == 28:
                solutions += 1
                total_moves += move_count
                break
            else:
                retry_attempts += 1
    
    return solutions, total_moves, retry_attempts, restart_count

# Parameters
simulation_count = 100
time_limit_per_try = 60  # in seconds

# Run Hill Climbing with Random Restarts and Time Limit
time_limit_results = restart_hill_climb_with_time_limit(simulation_count, time_limit_per_try)

# Display results in tabular format
time_limit_df = pd.DataFrame(
    [['Hill-Climbing with Time Limit'] + [
        time_limit_results[0] * 100 / simulation_count,  # Success (%)
        time_limit_results[2] * 100 / simulation_count,  # Stuck Probability (%)
        time_limit_results[1] / time_limit_results[0] if time_limit_results[0] > 0 else 0,  # Avg Moves (Successful)
        time_limit_results[2] / (simulation_count - time_limit_results[0]) if (simulation_count - time_limit_results[0]) > 0 else 0,  # Avg Moves (Stuck)
        0,  # Avg Random Steps (Successful)
        0   # Avg Random Steps (Stuck)
    ]],
    columns=[
        'Algorithm', 'Success (%)', 'Stuck Probability (%)', 
        'Avg Moves (Successful)', 'Avg Moves (Stuck)', 
        'Avg Random Steps (Successful)', 'Avg Random Steps (Stuck)'
    ]
)
print(time_limit_df.to_string(index=False))
