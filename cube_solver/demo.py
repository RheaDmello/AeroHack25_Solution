from cube import RubiksCube
from solver import solve_with_heuristic
from utils import print_moves

def test_case(title, scramble_moves):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")

    cube=RubiksCube()
    print("Original Solved Cube:")
    print(cube)

    #Apply scramble
    for move in scramble_moves:
        cube.apply_move(move)
    print(f"\nScrambled with: {' '.join(scramble_moves)}")
    print("\nScrambled cube:")
    print(cube)

    #Solve 
    print("Solving...")
    solution = solve_with_heuristic(cube, max_depth=10)

    if solution and isinstance(solution, list) and "not found" not in solution[0].lower():
        print("=======Solution found=======")
        print(f"Number of moves: {len(solution)}")
        print("Solution sequence:")
        print_moves(solution)

        #Verify solution
        test_cube=RubiksCube()
        for move in scramble_moves:
            test_cube.apply_move(move)
        for move in solution:
            test_cube.apply_move(move)
        print("Is cube solved after applying solution?", test_cube.is_solved())
    else:
        print("Solution not found within maximum depth.")


def main():
    #Test case 1:Simple (2 moves)
    test_case("Test Case 1: Simple Scramble", ['F', 'R'])
    #Test case 2:Medium (4 moves)
    test_case("Test Case 2: Medium Scramble", ['U', 'R', 'F\'', 'L'])
    #Test case 3:Random 6 move scramble
    cube=RubiksCube()
    scramble_seq = cube.scramble(6)
    test_case("Test Case 3: Random 6-Move Scramble", scramble_seq)
    #Test case 4:8 move scramble
    cube=RubiksCube()
    scramble_seq =cube.scramble(8)
    test_case("Test Case 4: Random 8-Move Scramble", scramble_seq)

if __name__ =="__main__":
    main()