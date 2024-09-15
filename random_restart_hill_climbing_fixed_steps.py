import random
import pandas as pd
import time

def count_safe_pairs(board_state):
    """Calculate the number of non-attacking pairs of queens."""
    max_safe_pairs = 28  # Max pairs for 8 queens (n * (n-1) / 2 where n = 8)
    attacking_pairs = 0
    
    for queen_a in range(8):
        for queen_b in range(queen_a + 1, 8):
            # Check if queens are in the same row or on the same diagonal
            if board_state[queen_a] == board_state[queen_b] or abs(board_state[queen_a] - board_state[queen_b]) == abs(queen_a - queen_b):
                attacking_pairs += 1

    return max_safe_pairs - attacking_pairs

def generate_random_board():
    """Generate a random state for 8 queens."""
    return [random.randint(0, 7) for _ in range(8)]

def random_walk_climb(board_state, max_no_improve_steps):
    """Perform Random-Walk Hill Climbing with additional metrics."""
    current_board = board_state
    current_safe_pairs = count_safe_pairs(current_board)
    step_count = 0
    sideways_moves_count = 0
    local_minima_count = 0
    start_time = time.time()
    
    while True:
        step_count += 1
        potential_neighbors = []
        for col in range(8):
            for row in range(8):
                if current_board[col] != row:
                    new_board = list(current_board)
                    new_board[col] = row
                    potential_neighbors.append((new_board, count_safe_pairs(new_board)))
        
        board_state, current_safe_pairs = random.choice(potential_neighbors)
        
        if current_safe_pairs == 28:
            elapsed_time = time.time() - start_time
            return board_state, current_safe_pairs, step_count, sideways_moves_count, local_minima_count, elapsed_time
        
        # Check for local minima
        if step_count > max_no_improve_steps:
            local_minima_count += 1
        
        sideways_moves_count += 1

def random_restart_climb_fixed(num_restarts, max_no_improve_steps, steps_before_restart):
    """Perform Random-Restart Hill Climbing with fixed steps and additional metrics."""
    total_successes = 0
    total_step_count = 0
    total_time = 0
    all_step_counts = []
    
    for _ in range(num_restarts):
        board_state = generate_random_board()
        step_count = 0
        while True:
            final_board, final_safe_pairs, step_count, sideways_moves_count, local_minima_count, elapsed_time = random_walk_climb(board_state, steps_before_restart)
            total_time += elapsed_time
            all_step_counts.append(step_count)
            
            if final_safe_pairs == 28:
                total_successes += 1
                total_step_count += step_count
                break
    
    avg_steps_for_success = total_step_count / total_successes if total_successes > 0 else 0
    avg_steps_for_stuck = (num_restarts - total_successes) / num_restarts if num_restarts > 0 else 0
    avg_time = total_time / num_restarts if num_restarts > 0 else 0
    
    return {
        'total_successes': total_successes,
        'total_step_count': total_step_count,
        'num_restarts': num_restarts,
        'avg_time': avg_time,
        'avg_steps_for_success': avg_steps_for_success,
        'avg_steps_for_stuck': avg_steps_for_stuck,
        'all_step_counts': all_step_counts
    }

# Parameters
simulations = 10000  
max_no_improve_steps = 750
restart_after_steps = 500

# Run Random-Restart Hill Climbing (Fixed Steps) simulation
fixed_step_climb_results = random_restart_climb_fixed(simulations, max_no_improve_steps, restart_after_steps)

# Display results in tabular format
fixed_step_climb_df = pd.DataFrame(
    [['Random-Restart Hill-Climbing (Fixed Steps)'] + [
        fixed_step_climb_results['total_successes'] * 100 / simulations,  # Success (%)
        (simulations - fixed_step_climb_results['total_successes']) * 100 / simulations,  # Stuck Probability (%)
        fixed_step_climb_results['avg_steps_for_success'],  # Avg Steps (Successful)
        fixed_step_climb_results['avg_steps_for_stuck'],  # Avg Steps (Stuck)
    ]],
    columns=[
        'Algorithm', 'Success (%)', 'Stuck Probability (%)', 
        'Avg Steps (Successful)', 'Avg Steps (Stuck)'
    ]
)
print(fixed_step_climb_df.to_string(index=False))

# Display additional details
print("\nDetailed Metrics:")
print(f"Total Successful Solutions: {fixed_step_climb_results['total_successes']}")
print(f"Total Steps Taken for All Solutions: {sum(fixed_step_climb_results['all_step_counts'])}")
print(f"Average Steps Taken for Each Solution: {sum(fixed_step_climb_results['all_step_counts']) / fixed_step_climb_results['total_successes'] if fixed_step_climb_results['total_successes'] > 0 else 0}")
