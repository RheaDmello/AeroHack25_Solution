from copy import deepcopy
class RubiksCube:
    def __init__(self,state=None):
        # Initialize a 3x3 Rubiks Cube
        # Faces: U(Up), D(Down), L(Left), R(Right), F(Front), B(Back)
        # Colors: W(white), Y(yellow), R(red), O(orange), G(green), B(blue)
        # Default: Solved state
        
        if state is None:
            self.state = {
                'U': [['W']*3 for _ in range(3)],
                'D': [['Y']*3 for _ in range(3)],
                'L': [['G']*3 for _ in range(3)],
                'R': [['B']*3 for _ in range(3)],
                'F': [['R']*3 for _ in range(3)],
                'B': [['O']*3 for _ in range(3)]
            }
        else:
            self.state = deepcopy(state)

    def copy(self):
        return RubiksCube(self.state)

    def rotate_face_clockwise(self, face):
        # To rotate a face 90 degrees clockwise
        self.state[face]=[list(row) for row in zip(*self.state[face][::-1])]

    def rotate_face_counterclockwise(self, face):
        #To rotate a face 90 degrees anti-clockwise
        for _ in range(3):
            self.rotate_face_clockwise(face)

    #Only valid moves are defined
    def U(self):self.rotate_face_clockwise('U')
    def U_prime(self): self.rotate_face_counterclockwise('U')
    def D(self):self.rotate_face_clockwise('D')
    def D_prime(self): self.rotate_face_counterclockwise('D')
    def L(self):self.rotate_face_clockwise('L')
    def L_prime(self): self.rotate_face_counterclockwise('L')
    def R(self):self.rotate_face_clockwise('R')
    def R_prime(self): self.rotate_face_counterclockwise('R')
    def F(self):self.rotate_face_clockwise('F')
    def F_prime(self): self.rotate_face_counterclockwise('F')
    def B(self):self.rotate_face_clockwise('B')
    def B_prime(self): self.rotate_face_counterclockwise('B')

    #Update face colors after rotation
    def U(self):
        self.rotate_face_clockwise('U')
        temp=self.state['F'][0][:]
        self.state['F'][0]=self.state['R'][0][:]
        self.state['R'][0]=self.state['B'][0][:]
        self.state['B'][0]=self.state['L'][0][:]
        self.state['L'][0]=temp

    def U_prime(self):
        self.rotate_face_counterclockwise('U')
        temp=self.state['F'][0][:]
        self.state['F'][0]=self.state['L'][0][:]
        self.state['L'][0]=self.state['B'][0][:]
        self.state['B'][0]=self.state['R'][0][:]
        self.state['R'][0]=temp

    def D(self):
        self.rotate_face_clockwise('D')
        temp =self.state['F'][2][:]
        self.state['F'][2] =self.state['L'][2][:]
        self.state['L'][2] =self.state['B'][2][:]
        self.state['B'][2] =self.state['R'][2][:]
        self.state['R'][2] =temp

    def D_prime(self):
        self.rotate_face_counterclockwise('D')
        temp=self.state['F'][2][:]
        self.state['F'][2]=self.state['R'][2][:]
        self.state['R'][2]=self.state['B'][2][:]
        self.state['B'][2]=self.state['L'][2][:]
        self.state['L'][2]=temp

    def L(self):
        self.rotate_face_clockwise('L')
        temp=[self.state['U'][i][0] for i in range(3)]
        for i in range(3):
            self.state['U'][i][0]=self.state['B'][2-i][2]
            self.state['B'][2-i][2]=self.state['D'][i][0]
            self.state['D'][i][0]=self.state['F'][i][0]
            self.state['F'][i][0]=temp[i]

    def L_prime(self):
        self.rotate_face_counterclockwise('L')
        temp=[self.state['U'][i][0] for i in range(3)]
        for i in range(3):
            self.state['U'][i][0]=self.state['F'][i][0]
            self.state['F'][i][0]=self.state['D'][i][0]
            self.state['D'][i][0]=self.state['B'][2-i][2]
            self.state['B'][2-i][2]=temp[i]

    def R(self):
        self.rotate_face_clockwise('R')
        temp=[self.state['U'][i][2] for i in range(3)]
        for i in range(3):
            self.state['U'][i][2]=self.state['F'][i][2]
            self.state['F'][i][2]=self.state['D'][i][2]
            self.state['D'][i][2]=self.state['B'][2-i][0]
            self.state['B'][2-i][0]=temp[i]

    def R_prime(self):
        self.rotate_face_counterclockwise('R')
        temp =[self.state['U'][i][2] for i in range(3)]
        for i in range(3):
            self.state['U'][i][2] =self.state['B'][2-i][0]
            self.state['B'][2-i][0]=self.state['D'][i][2]
            self.state['D'][i][2]= self.state['F'][i][2]
            self.state['F'][i][2]=temp[i]

    def F(self):
        self.rotate_face_clockwise('F')
        temp = self.state['U'][2][:]
        self.state['U'][2]= [self.state['L'][i][2] for i in range(3)][::-1]
        [self.state['L'][i].__setitem__(2, self.state['D'][0][i]) for i in range(3)]
        self.state['D'][0]= [self.state['R'][i][0] for i in range(3)][::-1]
        [self.state['R'][i].__setitem__(0, temp[i]) for i in range(3)]

    def F_prime(self):
        self.rotate_face_counterclockwise('F')
        temp=self.state['U'][2][:]
        self.state['U'][2]=[self.state['R'][i][0] for i in range(3)]
        [self.state['R'][i].__setitem__(0, self.state['D'][0][2-i]) for i in range(3)]
        self.state['D'][0]=[self.state['L'][i][2] for i in range(3)]
        [self.state['L'][i].__setitem__(2, temp[2-i]) for i in range(3)]

    def B(self):
        self.rotate_face_clockwise('B')
        temp=self.state['U'][0][:]
        self.state['U'][0]=[self.state['R'][i][2] for i in range(3)]
        [self.state['R'][i].__setitem__(2, self.state['D'][2][2-i]) for i in range(3)]
        self.state['D'][2]=[self.state['L'][i][1] for i in range(3)]
        [self.state['L'][i].__setitem__(1, temp[2-i]) for i in range(3)]

    def B_prime(self):
        self.rotate_face_counterclockwise('B')
        temp=self.state['U'][0][:]
        self.state['U'][0]=[self.state['L'][i][1] for i in range(3)][::-1]
        [self.state['L'][i].__setitem__(1, self.state['D'][2][i]) for i in range(3)]
        self.state['D'][2]=[self.state['R'][i][2] for i in range(3)][::-1]
        [self.state['R'][i].__setitem__(2, temp[i]) for i in range(3)]

    def apply_move(self, move):
        #Apply a move string like 'U', 'F', 'R', 'U''
        move_map = {
            'U': self.U,
            'U\'':self.U_prime,
            'D': self.D,
            'D\'':self.D_prime,
            'L': self.L,
            'L\'':self.L_prime,
            'R': self.R,
            'R\'':self.R_prime,
            'F': self.F,
            'F\'':self.F_prime,
            'B': self.B,
            'B\'':self.B_prime
        }
        if move in move_map:
            move_map[move]()
        else:
            raise ValueError(f"Invalid move: {move}")

    def is_solved(self):
        #Check if the cube is already in solved state
        for face, grid in self.state.items():
            color=grid[0][0]
            if any(cell != color for row in grid for cell in row):
                return False
        return True

    def scramble(self, moves=6):
        #Scramble the cube with random valid moves only
        import random
        move_list=['U', 'U\'', 'D', 'D\'', 'L', 'L\'', 'R', 'R\'', 'F', 'F\'', 'B', 'B\'']
        scramble_moves=random.choices(move_list, k=moves)
        for move in scramble_moves:
            self.apply_move(move)
        return scramble_moves

    def __str__(self):
        #Printing the cube
        s = ""
        for face, grid in self.state.items():
            s +=f"{face}:\n"
            for row in grid:
                s += " ".join(row) + "\n"
            s +="\n"
        return s