import pygame
from cube import RubiksCube
from solver import solve_with_heuristic
# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH=1200
SCREEN_HEIGHT=750
screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rhea Dmello")
clock=pygame.time.Clock()
FPS=30

# Colors
COLORS={
    'W':(255, 255,255), 'Y':(255,255,0),'R':(255,0,0),
    'O':(255, 165,0),'G': (0, 255, 0),'B': (0, 0, 255),
    'BLACK':(0, 0,0),'GRAY': (200,200,200),'LIGHT_GRAY': (240,240, 240),
    'RED':(220, 0,0), 'BLUE': (0,100, 200),'GREEN': (0, 150,0),
    'DARK_GRAY':(80, 80, 80),'PANEL_BG': (250, 250,255),}

SQUARE_SIZE = 45
GAP= 0

# Fonts
title_font= pygame.font.SysFont('Arial', 36, bold=True)
section_font=pygame.font.SysFont('Arial', 24, bold=True)
label_font =pygame.font.SysFont('Arial', 20)
small_font=pygame.font.SysFont('Arial', 18)
tiny_font=pygame.font.SysFont('Arial', 16)

# Test Cases
TEST_CASES =[
    ("Test Case 1: Simple Scramble",['F', 'R']),
    ("Test Case 2: Medium Scramble",['U', 'R', "F'", 'L']),
    ("Test Case 3: Random 6-Move Scramble", None),
    ("Test Case 4: Random 8-Move Scramble", None),
]

# State
selected_test_case = None
cube=RubiksCube()
scramble_moves =[]
solution_moves =[]
solve_step =0
phase="select"
show_solved_message = False


def draw_face(surface, face_grid, x, y, label):
    for i in range(3):
        for j in range(3):
            color=COLORS.get(face_grid[i][j],COLORS['GRAY'])
            rect=pygame.Rect(x+j*(SQUARE_SIZE+GAP), y + i*(SQUARE_SIZE+GAP), SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(surface,color,rect)
            pygame.draw.rect(surface,COLORS['BLACK'], rect, 1)
    surface.blit(label_font.render(label,True, COLORS['BLACK']), (x+SQUARE_SIZE, y-25))


def draw_cube_net(surface, cube):
    x,y=750,370
    draw_face(surface,cube.state['U'], x, y-3*SQUARE_SIZE,'U')
    draw_face(surface,cube.state['L'], x-3*SQUARE_SIZE, y,'L')
    draw_face(surface,cube.state['F'], x,y,'F')
    draw_face(surface,cube.state['R'], x+ 3*SQUARE_SIZE,y,'R')
    draw_face(surface,cube.state['B'], x+ 6*SQUARE_SIZE,y,'B')
    draw_face(surface,cube.state['D'], x,y+3*SQUARE_SIZE,'D')

    if phase == "solved":
        # 1. "CUBE SOLVED!" at the top
        surface.blit(title_font.render("CUBE SOLVED!", True,COLORS['GREEN']),(SCREEN_WIDTH//2-100,100))
        
        # 2. Solution steps below it
        solution_line = "Solution: " + " → ".join(solution_moves)
        surface.blit(section_font.render(solution_line, True, COLORS['DARK_GRAY']),(SCREEN_WIDTH//2-100,145))
        
        # 3. Instruction to select next test case at the bottom
        surface.blit(section_font.render("Select the next Test Case", True,COLORS['RED']),(SCREEN_WIDTH//2-100,180))


def draw_ui(surface):
    global phase
    pygame.draw.rect(surface,COLORS['PANEL_BG'], (15, 15, 450,SCREEN_HEIGHT-30))
    pygame.draw.rect(surface, COLORS['BLUE'], (15, 15, 450,SCREEN_HEIGHT-30), 3)
    y=25
    surface.blit(title_font.render("Rubik's Solver", True, COLORS['BLUE']),(25, y))
    y+=60

    if phase in ["select", "solved"]:
        surface.blit(section_font.render("Select Test Case",True,COLORS['DARK_GRAY']),(25, y))
        y +=35
        for i, (name, _) in enumerate(TEST_CASES):
            surface.blit(label_font.render(f"Press {i+1}:{name}",True,COLORS['BLACK']),(30, y))
            y+= 30

    if phase=="scramble":
        surface.blit(section_font.render("Ready to Scramble",True, COLORS['GREEN']),(25, y))
        y+= 35
        surface.blit(small_font.render(f"Selected:{TEST_CASES[selected_test_case][0]}",True,COLORS['BLUE']),(25, y))
        y +=25
        surface.blit(small_font.render("Press S to apply scramble",True, COLORS['BLACK']),(25, y))
        y+=25

    elif phase=="solving":
        surface.blit(section_font.render("Solving Step-by-Step",True,COLORS['GREEN']),(25, y))
        y+=35
        if solve_step > 0:
            surface.blit(small_font.render("Applied Moves:",True,COLORS['DARK_GRAY']),(25, y))
            y+= 25
            applied =" → ".join(solution_moves[:solve_step])[:47] + "..." if len(solution_moves) >5 else " → ".join(solution_moves[:solve_step])
            surface.blit(tiny_font.render(applied,True, COLORS['BLACK']),(30, y))
            y+=30
        if solve_step<len(solution_moves):
            surface.blit(small_font.render(f"Next Move:{solution_moves[solve_step]}", True, COLORS['GREEN']), (25, y))
            y+=25
            surface.blit(small_font.render("Press SPACE to apply",True, COLORS['DARK_GRAY']), (25, y))


def apply_move(cube, move_str):
    move_map ={
        'U': cube.U,'U\'': cube.U_prime, 'D': cube.D,'D\'':cube.D_prime,
        'L': cube.L, 'L\'': cube.L_prime, 'R': cube.R,'R\'':cube.R_prime,
        'F': cube.F,'F\'': cube.F_prime, 'B': cube.B, 'B\'': cube.B_prime
        }
    if move_str in move_map:
        move_map[move_str]()


def main():
    global selected_test_case,scramble_moves,solution_moves,solve_step,phase,cube
    running =True
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            elif event.type==pygame.KEYDOWN:
                if pygame.K_1<= event.key <=pygame.K_4:
                    idx= event.key -pygame.K_1
                    selected_test_case= idx
                    scramble_moves = RubiksCube().scramble(6 if idx==2 else 8) if idx>1 else TEST_CASES[idx][1]
                    TEST_CASES[idx] =(TEST_CASES[idx][0], scramble_moves)
                    phase ="scramble"
                elif phase=="scramble" and event.key==pygame.K_s:
                    cube =RubiksCube()
                    for move in scramble_moves:
                        apply_move(cube, move)
                    solution_moves =solve_with_heuristic(cube.copy(),max_depth=10) or []
                    solve_step=0
                    phase="solving"
                elif phase=="solving" and event.key==pygame.K_SPACE:
                    if solve_step < len(solution_moves):
                        apply_move(cube, solution_moves[solve_step])
                        solve_step +=1
                        if solve_step==len(solution_moves):
                            phase ="solved"
                elif phase=="solved" and event.key==pygame.K_SPACE:
                    phase= "select"
        screen.fill(COLORS['LIGHT_GRAY'])
        draw_cube_net(screen, cube)
        draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ =="__main__":
    main()
