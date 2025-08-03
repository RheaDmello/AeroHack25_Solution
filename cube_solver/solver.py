from cube import RubiksCube
#Only valid moves
MOVES=['U', 'U\'', 'D', 'D\'', 'L', 'L\'', 'R', 'R\'', 'F', 'F\'', 'B', 'B\'']

def solve_with_heuristic(cube, max_depth=10):
    # Solve cube using only valid moves.
    # It runs until the solution is found or max depth reached.
    # Uses Iterative Deepening DFS with pruning and heuristic method.
    
    #Opposite moves to avoid undoing
    opposites={
        'U': 'U\'', 'U\'': 'U',
        'D': 'D\'', 'D\'': 'D',
        'L': 'L\'', 'L\'': 'L',
        'R': 'R\'', 'R\'': 'R',
        'F': 'F\'', 'F\'': 'F',
        'B': 'B\'', 'B\'': 'B'}

    def heuristic(current_cube):
        #Estimate minimum moves needed (optimistic)
        solved=RubiksCube()
        errors=0
        for face in ['U','D','L','R','F','B']:
            for i in range(3):
                for j in range(3):
                    if current_cube.state[face][i][j]!=solved.state[face][i][j]:
                        errors+=1
        return errors//8  #Each move fixes ~8 stickers

    def dfs(current_cube, moves, max_d):
        #Depth-limited DFS
        if current_cube.is_solved():
            return moves[:]

        depth=len(moves)
        if depth>=max_d:
            return None

        #Prune estimated total cost exceeds depth limit
        if depth+heuristic(current_cube)>max_d:
            return None

        for move in MOVES:
            if moves:
                last_move=moves[-1]
                #Skip inverse: U after U'
                if opposites.get(last_move)==move:
                    continue
                #Skip same move repeated: U after U
                if last_move==move:
                    continue
            new_cube=current_cube.copy()
            new_cube.apply_move(move)
            result=dfs(new_cube, moves+[move], max_d)
            if result is not None:
                return result
        return None

    #Try increasing depth
    for d in range(1,max_depth+1):
        print(f"Trying depth {d}...")
        result = dfs(cube.copy(), [], d)
        if result is not None:
            print(f"Solved at depth {d}.")
            return result
    return ["Solution not found within maximum depth limit."]