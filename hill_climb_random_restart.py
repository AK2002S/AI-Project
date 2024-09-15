import random
import pandas as pd
import time

def count_non_attacking_pairs(board):
    """Calculate the number of non-attacking pairs of queens."""
    max_safe_pairs = 28  # Max pairs for 8 queens (n * (n-1) / 2 where n = 8)
    attacking_pairs = 0
    
    for i in range(8):
        for j in range(i + 1, 8):
            # Check if queens are in the same row or on the same diagonal
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                attacking_pairs += 1

    return max_safe_pairs - attacking_pairs

def generate_random_board():
    """Generate a random board state for 8 queens."""
    return [random.randint(0, 7) for _ in range(8)]

def random_walk_hill_climb(board, max_no_improvement_steps):
    """Perform Random-Walk Hill Climbing with additional metrics."""
    current_board = board
    current_safe_pairs = count_non_attacking_pairs(current_board)
    total_steps = 0
    sideway_moves = 0
    local_minima_count = 0
    start_time = time.time()
    
    while True:
        total_steps += 1
        neighbors = []
        for col in range(8):
            for row in range(8):
                if current_board[col] != row:
                    new_board = list(current_board)
                    new_board[col] = row
                    neighbors.append((new_board, count_non_attacking_pairs(new_board)))
        
        current_board, current_safe_pairs = random.choice(neighbors)
        
        if current_safe_pairs == 28:
            time_taken = time.time() - start_time
            return current_board, current_safe_pairs, total_steps, sideway_moves, local_minima_count, time_taken
        
        # Check for local minima
        if total_steps > max_no_improvement_steps:
            local_minima_count += 1
        
        sideway_moves += 1

def random_restart_hill_climb_fixed_steps(num_restarts, max_no_improvement_steps, steps_per_restart):
    """Perform Random-Restart Hill Climbing with fixed steps and additional metrics."""
    successful_attempts = 0
    total_steps_taken = 0
    total_time = 0
    all_steps_list = []
    
    for _ in range(num_restarts):
        board = generate_random_board()
        steps = 0
        while True:
            final_board, safe_pairs, steps, sideway_moves, local_minima, time_taken = random_walk_hill_climb(board, steps_per_restart)
            total_time += time_taken
            all_steps_list.append(steps)
            
            if safe_pairs == 28:
                successful_attempts += 1
                total_steps_taken += steps
                break
    
    avg_steps_success = total_steps_taken / successful_attempts if successful_attempts > 0 else 0
    avg_steps_failure = (num_restarts - successful_attempts) / num_restarts if num_restarts > 0 else 0
    avg_time_per_restart = total_time / num_restarts if num_restarts > 0 else 0
    
    return {
        'success_count': successful_attempts,
        'total_steps': total_steps_taken,
        'num_restarts': num_restarts,
        'avg_time': avg_time_per_restart,
        'avg_steps_success': avg_steps_success,
        'avg_steps_failure': avg_steps_failure,
        'steps_list': all_steps_list
    }

# Parameters
num_trials = 10000  
max_no_improvement_steps = 750
restart_after_steps = 500

# Run Random-Restart Hill Climbing (Fixed Steps) simulation
hill_climb_results = random_restart_hill_climb_fixed_steps(num_trials, max_no_improvement_steps, restart_after_steps)

# Display results in tabular format
results_df = pd.DataFrame(
    [['Random-Restart Hill-Climbing (Fixed Steps)'] + [
        hill_climb_results['success_count'] * 100 / num_trials,  # Success (%)
        (num_trials - hill_climb_results['success_count']) * 100 / num_trials,  # Stuck Probability (%)
        hill_climb_results['avg_steps_success'],  # Avg Steps (Successful)
        hill_climb_results['avg_steps_failure'],  # Avg Steps (Stuck)
    ]],
    columns=[
        'Algorithm', 'Success (%)', 'Stuck Probability (%)', 
        'Avg Steps (Successful)', 'Avg Steps (Stuck)'
    ]
)
print(results_df.to_string(index=False))

# Display additional details
print("\nDetailed Metrics:")
print(f"Total Successful Solutions: {hill_climb_results['success_count']}")
print(f"Total Steps Taken for All Solutions: {sum(hill_climb_results['steps_list'])}")
print(f"Average Steps Taken for Each Solution: {sum(hill_climb_results['steps_list']) / hill_climb_results['success_count'] if hill_climb_results['success_count'] > 0 else 0}")
