import random

def generate_random_board():
    """Generate a random 8-queens board state (one queen per column)."""
    return [random.randint(0, 7) for _ in range(8)]

def count_safe_queen_pairs(board):
    """Count the number of non-attacking queen pairs."""
    total_pairs = 28  # Total number of pairs of queens in an 8-queens problem (C(8, 2) = 28)
    attacking_pairs = 0
    for i in range(len(board)):
        for j in range(i + 1, len(board)):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                attacking_pairs += 1
    return total_pairs - attacking_pairs

def perform_hill_climb(board):
    """Perform hill-climbing to maximize the number of non-attacking pairs."""
    current_safe_pairs = count_safe_queen_pairs(board)
    steps_taken = 0
    
    while True:
        steps_taken += 1
        neighbors = []
        for col in range(8):
            for row in range(8):
                if board[col] != row:
                    new_board = list(board)
                    new_board[col] = row
                    neighbors.append((new_board, count_safe_queen_pairs(new_board)))
        
        # Sort neighbors by number of non-attacking pairs
        neighbors.sort(key=lambda x: x[1], reverse=True)
        
        # Choose the best neighbor
        best_neighbor, best_safe_pairs = neighbors[0]
        
        # Check if improvement is possible
        if best_safe_pairs > current_safe_pairs:
            board = best_neighbor
            current_safe_pairs = best_safe_pairs
        else:
            # No improvement, return current board
            return board, current_safe_pairs, steps_taken

def simulate_hill_climbing(num_trials):
    """Run multiple simulations and return the best results."""
    successful_runs = 0
    success_steps = []
    stuck_steps = []
    optimal_solution = None
    max_safe_pairs = 0
    fewest_steps = float('inf')
    
    for _ in range(num_trials):
        board = generate_random_board()
        final_board, final_safe_pairs, steps_taken = perform_hill_climb(board)
        
        if final_safe_pairs == 28:
            successful_runs += 1
            success_steps.append(steps_taken)
        else:
            stuck_steps.append(steps_taken)
        
        # Track the best solution found
        if (final_safe_pairs > max_safe_pairs or
            (final_safe_pairs == max_safe_pairs and steps_taken < fewest_steps)):
            optimal_solution = final_board
            max_safe_pairs = final_safe_pairs
            fewest_steps = steps_taken
    
    success_rate = successful_runs / num_trials
    avg_steps_to_success = sum(success_steps) / successful_runs if successful_runs > 0 else 0
    avg_steps_to_stuck = sum(stuck_steps) / (num_trials - successful_runs) if (num_trials - successful_runs) > 0 else 0
    
    return (success_rate, avg_steps_to_success, avg_steps_to_stuck, 
            optimal_solution, max_safe_pairs, fewest_steps)

def print_board(board):
    """Print the board with queens and dots."""
    chessboard = [['.' for _ in range(8)] for _ in range(8)]
    for col, row in enumerate(board):
        chessboard[row][col] = 'Q'
    
    for row in chessboard:
        print(' '.join(row))

# Parameters
num_trials = 1000
best_outcome = None
highest_success_rate = 0

# Run simulations
print("Running hill-climbing simulations...")
simulation_results = simulate_hill_climbing(num_trials)

# Check if the current results have a better success rate
if simulation_results[0] > highest_success_rate:
    highest_success_rate = simulation_results[0]
    best_outcome = simulation_results

# Print the best results
if best_outcome:
    print("\nBest Results Found:")
    print(f"Success Rate: {best_outcome[0] * 100:.2f}%")
    print(f"Average Steps for Success: {best_outcome[1]}")
    print(f"Average Steps when Stuck: {best_outcome[2]}")
    print("\nBest Solution Found:")
    print_board(best_outcome[3])
    print(f"Non-Attacking Pairs: {best_outcome[4]}")
    print(f"Steps to Find Solution: {best_outcome[5]}")
