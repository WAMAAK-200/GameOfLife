# An enhanced version of Conway's Game of Life by Warith Kolawole
# Completed as part of a mini project after expanding from a tutorial on how to make Conway's Game of Life

import random
import json
import os
import time

def random_state(width, height):

    board_state = []
    for y in range(height):
        row = []
        for x in range(width):

            random_num = random.random()

            if random_num >= 0.5:
                cell_state= 0
            else:
                cell_state = 1
            row.append(cell_state)
        board_state.append(row)
    return board_state


def dead_state(width, height):

    return [[0 for _ in range(width)] for _ in range(height)]

def render(board_state):

    for row in board_state:
        line = ""
        for cell in row:
            if cell == 1:
                line += "#"
            else:
                line += " "
        print(line)

def next_board_state(initial_board_state):
    height = len(initial_board_state)
    width = len(initial_board_state[0])
    next_state = dead_state(width, height)

    for y in range(height):
        for x in range(width):
            # Count live neighbors (with wrap-around)
            live_neighbors = 0

            # Check all 8 neighbors
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue  # Skip the cell itself

                    # Wrap around edges
                    ny = (y + dy) % height
                    nx = (x + dx) % width

                    if initial_board_state[ny][nx] == 1:
                        live_neighbors += 1

            # Apply Conway's Game of Life rules
            current_cell = initial_board_state[y][x]

            if current_cell == 1:  # Cell is alive
                if live_neighbors < 2 or live_neighbors > 3:
                    next_state[y][x] = 0  # Dies
                else:
                    next_state[y][x] = 1  # Lives on
            else:  # Cell is dead
                if live_neighbors == 3:
                    next_state[y][x] = 1  # Reproduction
                else:
                    next_state[y][x] = 0  # Stays dead

    return next_state

class PatternLibrary:
    def __init__(self):
        self.patterns = {
            # Still Lifes
            'block': [[1, 1], [1, 1]],
            'beehive': [[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]],
            'loaf': [[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 0]],
            'boat': [[1, 1, 0], [1, 0, 1], [0, 1, 0]],

            # Oscillators
            'blinker': [[1, 1, 1]],
            'toad': [[0, 1, 1, 1], [1, 1, 1, 0]],
            'beacon': [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]],
            'pulsar': [
                [0,0,1,1,1,0,0,0,1,1,1,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0],
                [1,0,0,0,0,1,0,1,0,0,0,0,1],
                [1,0,0,0,0,1,0,1,0,0,0,0,1],
                [1,0,0,0,0,1,0,1,0,0,0,0,1],
                [0,0,1,1,1,0,0,0,1,1,1,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,1,1,1,0,0,0,1,1,1,0,0],
                [1,0,0,0,0,1,0,1,0,0,0,0,1],
                [1,0,0,0,0,1,0,1,0,0,0,0,1],
                [1,0,0,0,0,1,0,1,0,0,0,0,1],
                [0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,1,1,1,0,0,0,1,1,1,0,0]
            ],

            # Spaceships
            'glider': [[0, 1, 0], [0, 0, 1], [1, 1, 1]],
            'lwss': [  # Light-weight spaceship
                [0, 1, 0, 0, 1],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 1],
                [1, 1, 1, 1, 0]
            ],
            'mwss': [  # Middle-weight spaceship
                [0,0,1,0,0,0],
                [1,0,0,0,1,0],
                [0,0,0,0,0,1],
                [1,0,0,0,0,1],
                [0,1,1,1,1,1]
            ],

            # Methuselahs (long-lived patterns)
            'r_pentomino': [[0, 1, 1], [1, 1, 0], [0, 1, 0]],
            'diehard': [
                [0,0,0,0,0,0,1,0],
                [1,1,0,0,0,0,0,0],
                [0,1,0,0,0,1,1,1]
            ],

            # Guns
            'glider_gun': [  # Gosper's Glider Gun
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
                [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
                [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            ]
        }

    def get_pattern(self, name):
        """Get a pattern by name"""
        return [row[:] for row in self.patterns.get(name, [[0]])]

    def list_patterns(self):
        """List all available patterns"""
        categories = {
            'still_lifes': ['block', 'beehive', 'loaf', 'boat'],
            'oscillators': ['blinker', 'toad', 'beacon', 'pulsar'],
            'spaceships': ['glider', 'lwss', 'mwss'],
            'methuselahs': ['r_pentomino', 'diehard'],
            'guns': ['glider_gun']
        }

        print("\n" + "="*50)
        print("PATTERN LIBRARY")
        print("="*50)

        for category, patterns in categories.items():
            print(f"\n{category.replace('_', ' ').title()}:")
            for pattern in patterns:
                size = f"{len(self.patterns[pattern])}x{len(self.patterns[pattern][0])}"
                print(f"  {pattern:15} ({size})")

    def save_pattern(self, name, pattern, custom_file="custom_patterns.json"):
        """Save a custom pattern"""
        if os.path.exists(custom_file):
            with open(custom_file, 'r') as f:
                custom_patterns = json.load(f)
        else:
            custom_patterns = {}

        custom_patterns[name] = pattern

        with open(custom_file, 'w') as f:
            json.dump(custom_patterns, f, indent=2)

        print(f"Pattern '{name}' saved to {custom_file}")

    def load_custom_patterns(self, custom_file="custom_patterns.json"):
        """Load custom patterns from file"""
        if os.path.exists(custom_file):
            with open(custom_file, 'r') as f:
                custom_patterns = json.load(f)
                self.patterns.update(custom_patterns)
                print(f"Loaded {len(custom_patterns)} custom patterns")

class PatternEditor:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.cursor_x = width // 2
        self.cursor_y = height // 2
        self.drawing = True
        self.pattern_lib = PatternLibrary()

    def clear_board(self):
        """Clear the entire board"""
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def toggle_cell(self, x, y):
        """Toggle a cell at position (x, y)"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.board[y][x] = 1 - self.board[y][x]

    def place_pattern(self, pattern_name, x, y, centered=True):
        """Place a pattern from the library at position (x, y)"""
        pattern = self.pattern_lib.get_pattern(pattern_name)
        if not pattern:
            print(f"Pattern '{pattern_name}' not found!")
            return False

        pattern_height = len(pattern)
        pattern_width = len(pattern[0])

        # Adjust position for centering
        if centered:
            x -= pattern_width // 2
            y -= pattern_height // 2

        # Place the pattern
        for py in range(pattern_height):
            for px in range(pattern_width):
                board_x = x + px
                board_y = y + py
                if 0 <= board_x < self.width and 0 <= board_y < self.height:
                    if pattern[py][px] == 1:
                        self.board[board_y][board_x] = 1

        return True

    def rotate_pattern(self, pattern, degrees=90):
        """Rotate a pattern by specified degrees"""
        if degrees == 90:
            return [[pattern[y][x] for y in range(len(pattern)-1, -1, -1)]
                    for x in range(len(pattern[0]))]
        elif degrees == 180:
            return [[pattern[-y-1][-x-1] for x in range(len(pattern[0]))]
                    for y in range(len(pattern))]
        elif degrees == 270:
            return [[pattern[y][x] for y in range(len(pattern))]
                    for x in range(len(pattern[0])-1, -1, -1)]
        return pattern

    def mirror_pattern(self, pattern, horizontal=True):
        """Mirror a pattern horizontally or vertically"""
        if horizontal:
            return [row[::-1] for row in pattern]
        else:
            return pattern[::-1]

    def extract_pattern(self, x, y, width, height):
        """Extract a pattern from the board"""
        pattern = []
        for py in range(height):
            row = []
            for px in range(width):
                board_x = x + px
                board_y = y + py
                if 0 <= board_x < self.width and 0 <= board_y < self.height:
                    row.append(self.board[board_y][board_x])
                else:
                    row.append(0)
            pattern.append(row)
        return pattern

    def render(self, show_cursor=True):
        """Render the editor board"""
        os.system('cls' if os.name == 'nt' else 'clear')

        print("="*50)
        print("PATTERN EDITOR")
        print("="*50)
        print("Commands: [SPACE] toggle cell, [P] place pattern, [S] save pattern")
        print("          [C] clear, [R] run simulation, [Q] quit")
        print("="*50)

        for y in range(self.height):
            line = ""
            for x in range(self.width):
                if show_cursor and x == self.cursor_x and y == self.cursor_y:
                    if self.board[y][x] == 1:
                        line += "◉"  # Cursor on live cell
                    else:
                        line += "○"  # Cursor on dead cell
                else:
                    if self.board[y][x] == 1:
                        line += "█"
                    else:
                        line += "·"
            print(line)

        # Show statistics
        live_cells = sum(sum(row) for row in self.board)
        print(f"\nLive cells: {live_cells} | Cursor: ({self.cursor_x}, {self.cursor_y})")

    def run_editor(self):
        """Main editor loop"""
        import keyboard

        print("Starting Pattern Editor...")
        print("Use arrow keys to move, SPACE to toggle cells")
        print("Press 'h' for help")

        self.render()

        while True:
            if keyboard.is_pressed('up'):
                self.cursor_y = max(0, self.cursor_y - 1)
                self.render()
                time.sleep(0.1)
            elif keyboard.is_pressed('down'):
                self.cursor_y = min(self.height - 1, self.cursor_y + 1)
                self.render()
                time.sleep(0.1)
            elif keyboard.is_pressed('left'):
                self.cursor_x = max(0, self.cursor_x - 1)
                self.render()
                time.sleep(0.1)
            elif keyboard.is_pressed('right'):
                self.cursor_x = min(self.width - 1, self.cursor_x + 1)
                self.render()
                time.sleep(0.1)
            elif keyboard.is_pressed('space'):
                self.toggle_cell(self.cursor_x, self.cursor_y)
                self.render()
                time.sleep(0.2)
            elif keyboard.is_pressed('p'):
                self.pattern_lib.list_patterns()
                pattern_name = input("\nEnter pattern name to place: ").strip()
                if pattern_name:
                    self.place_pattern(pattern_name, self.cursor_x, self.cursor_y)
                    self.render()
            elif keyboard.is_pressed('s'):
                pattern_name = input("Enter name for this pattern: ").strip()
                if pattern_name:
                    # Find bounding box of pattern
                    min_x, max_x = self.width, -1
                    min_y, max_y = self.height, -1

                    for y in range(self.height):
                        for x in range(self.width):
                            if self.board[y][x] == 1:
                                min_x = min(min_x, x)
                                max_x = max(max_x, x)
                                min_y = min(min_y, y)
                                max_y = max(max_y, y)

                    if min_x <= max_x and min_y <= max_y:
                        pattern_width = max_x - min_x + 1
                        pattern_height = max_y - min_y + 1
                        pattern = self.extract_pattern(min_x, min_y, pattern_width, pattern_height)
                        self.pattern_lib.save_pattern(pattern_name, pattern)
                    else:
                        print("No live cells to save!")
            elif keyboard.is_pressed('c'):
                self.clear_board()
                self.render()
            elif keyboard.is_pressed('r'):
                # Run simulation with current pattern
                from game_of_life import next_board_state, render
                print("\nRunning simulation... Press 'b' to go back to editor")

                sim_board = [row[:] for row in self.board]
                generation = 0

                while True:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f"Generation {generation}")
                    print("Press 'b' to return to editor")
                    render(sim_board)

                    if keyboard.is_pressed('b'):
                        break

                    sim_board = next_board_state(sim_board)
                    generation += 1
                    time.sleep(0.3)

                self.render()
            elif keyboard.is_pressed('h'):
                print("\n" + "="*50)
                print("EDITOR HELP")
                print("="*50)
                print("Arrow Keys: Move cursor")
                print("SPACE: Toggle cell at cursor")
                print("P: Place a pattern from library")
                print("S: Save current pattern")
                print("C: Clear board")
                print("R: Run simulation with current pattern")
                print("H: Show this help")
                print("Q: Quit editor")
                print("="*50)
                input("Press Enter to continue...")
                self.render()
            elif keyboard.is_pressed('q'):
                print("\nE")

# MAIN - Enhanced version of the Game of Life
def main():


    # Load custom patterns
    pattern_lib = PatternLibrary()
    pattern_lib.load_custom_patterns()

    print("CONWAY'S GAME OF LIFE")
    print("="*50)
    print("1. Run random simulation")
    print("2. Pattern Library Browser")
    print("3. Pattern Editor")
    print("4. Load and run specific pattern")
    print("Q. Quit")

    choice = input("\nSelect option: ").strip().lower()

    if choice == '1':
        # Original random simulation
        width = 40
        height = 30
        board = random_state(width, height)

        for generation in range(100):
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Generation {generation + 1}")
            render(board)
            next_board_state(board)
            time.sleep(0.1)

    elif choice == '2':
        pattern_lib.list_patterns()
        input("\nPress Enter to continue...")
        main()

    elif choice == '3':
        editor = PatternEditor(width=40, height=30)
        editor.run_editor()
        main()

    elif choice == '4':
        pattern_lib.list_patterns()
        pattern_name = input("\nEnter pattern name to run: ").strip()

        if pattern_name in pattern_lib.patterns:
            pattern = pattern_lib.get_pattern(pattern_name)

            # Create board with pattern centered
            width = 60
            height = 40
            board = dead_state(width, height)

            # Center the pattern
            start_x = (width - len(pattern[0])) // 2
            start_y = (height - len(pattern)) // 2

            for y in range(len(pattern)):
                for x in range(len(pattern[0])):
                    board[start_y + y][start_x + x] = pattern[y][x]

            print(f"\nRunning pattern: {pattern_name}")
            print("Press Ctrl+C to stop")
            time.sleep(2)

            for generation in range(200):
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"Pattern: {pattern_name} - Generation {generation + 1}")
                render(board)
                board = next_board_state(board)
                time.sleep(0.1)
        else:
            print(f"Pattern '{pattern_name}' not found!")
            time.sleep(2)
            main()

    elif choice == 'q':
        print("Goodbye!")
        return

if __name__ == "__main__":
    # You'll need to install the keyboard module for the editor: pip install keyboard
    # Or you can remove keyboard dependency and use an alternative input method

    try:
        main()
    except ImportError:
        print("Note: For full editor functionality, install: pip install keyboard")
        print("Running in basic mode...")

        # Create a basic version without keyboard dependency
        pattern_lib = PatternLibrary()
        pattern_lib.list_patterns()

        # Simple pattern placement example
        width = 30
        height = 20
        board = dead_state(width, height)

        # Place a glider in the center
        pattern = pattern_lib.get_pattern('glider')
        start_x = (width - len(pattern[0])) // 2
        start_y = (height - len(pattern)) // 2

        for y in range(len(pattern)):
            for x in range(len(pattern[0])):
                board[start_y + y][start_x + x] = pattern[y][x]

        print("\nRunning glider pattern...")
        for generation in range(50):
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Glider - Generation {generation + 1}")
            render(board)
            board = next_board_state(board)
            time.sleep(0.2)