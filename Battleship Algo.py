import numpy as np

# Initialize empty lists to store shots and hits
shots_list = []
hit_list = []

# Create the game board
board_size = 10
board = [['-' for _ in range(board_size)] for _ in range(board_size)]
prob_board = np.zeros((board_size, board_size), dtype=int)
hit_board = np.zeros((board_size, board_size), dtype=int)


# Function to display the game board
def display_board():
    for row in board:
        print(" ".join(row))
    status()


# Function to display the probability board
def display_prob_board():
    combinations()
    print(prob_board)
    print(f"Mode:Hunt   Best Option: {hunt_best_option()}")


# Function to sort a list based on the sum of its elements
def sort_list(sort_list):
    return sorted(sort_list, key=lambda x: sum(x))


# Function to display the hit board
def display_hit_board():
    combinations()
    if sort_list(hit_list) in ship_cords and target_left() == 0:
        print("You sunk the last ship")
    elif sort_list(hit_list) in ship_cords:
        print("You sunk a ship. Back to hunt mode")
    else:
        print(hit_board)
        print(f"Mode:Sink   Best Option: {sink_best_option()}")


# Function to position a ship on the board
def position(x_cord, y_cord, ship, vertical):
    initial_ship_cords = []
    if vertical:
        for n in range(ship):
            board[x_cord + n][y_cord] = "X"
            initial_ship_cords.append((x_cord + n, y_cord))
    else:
        for n in range(ship):
            board[x_cord][y_cord + n] = "X"
            initial_ship_cords.append((x_cord, y_cord + n))
    return initial_ship_cords


# Function to check if ships are positioned properly without overlapping
def position_error():
    all_ship_cords = [cords for positions in ships.values() for cords in positions[1]]
    return len(all_ship_cords) != len(set(all_ship_cords))


# Function to count remaining target pieces on the board
def target_left():
    return sum(row.count("X") for row in board)


# Function to count total shots fired
def total_shots():
    return sum(row.count("#") + row.count("O") for row in board)


# Function to count hits
def hit_shots():
    return sum(row.count("O") for row in board)


# Function to count misses
def missed_shots():
    return sum(row.count("#") for row in board)


# Function to display game status
def status():
    print(f"Turns: {total_shots()} Hits: {hit_shots()}  Misses: {missed_shots()} Targets_left: {target_left()}")


# Dictionary containing ships and their positions on the board
ships = {
    "Aircraft_Carrier": [5, position(5, 2, 5, vertical=False)],
    "Battleship": [4, position(4, 9, 4, vertical=True)],
    "Submarine": [3, position(0, 0, 3, vertical=True)],
    "Cruiser": [3, position(8, 6, 3, vertical=False)],
    "Destroyer": [2, position(9, 2, 2, vertical=False)]
}

# List containing ship coordinates
ship_cords = [cords[1] for cords in ships.values()]


# Function to update probability and hit boards based on shots and hits
def combinations():
    hit_table_update = False
    empty_slot_counter = 0
    possible_hit_cords = []

    for list_values in ships.values():
        totalships = list_values[0]
        for x in range(0, board_size):
            for y in range(0, board_size + 1 - totalships):
                for n in range(y, y + totalships):
                    if (x, n) not in shots_list:
                        empty_slot_counter += 1
                        if (x, n) in hit_list:
                            possible_hit_cords.append((x, n))

                if sort_list(possible_hit_cords) == sort_list(hit_list):
                    hit_table_update = True

                if empty_slot_counter == totalships:
                    for n in range(y, y + totalships):
                        prob_board[x][n] += 1
                        if hit_table_update:
                            hit_board[x][n] += 1

                for current_hits in hit_list:
                    hit_board[current_hits] = 0
                empty_slot_counter = 0
                possible_hit_cords = []
                hit_table_update = False

        for y in range(0, board_size):
            for x in range(0, board_size + 1 - totalships):
                for n in range(x, x + totalships):
                    if (n, y) not in shots_list:
                        empty_slot_counter += 1
                        if (n, y) in hit_list:
                            possible_hit_cords.append((n, y))

                    if sort_list(possible_hit_cords) == sort_list(hit_list):
                        hit_table_update = True

                if empty_slot_counter == totalships:
                    for n in range(x, x + totalships):
                        prob_board[n][y] += 1
                        if hit_table_update:
                            hit_board[n][y] += 1

                for current_hits in hit_list:
                    hit_board[current_hits] = 0
                    possible_hit_cords = []
                empty_slot_counter = 0
                hit_table_update = False


# Function to find the best option in hunt mode
def hunt_best_option():
    highest_combo = 0
    best_cord = ()
    for y in range(0, board_size):
        for x in range(0, board_size):
            if highest_combo < prob_board[x][y]:
                highest_combo = prob_board[x][y]
                best_cord = (x, y)

    return best_cord


# Function to find the best option in sink mode
def sink_best_option():
    highest_combo = 0
    best_cord = ()
    for y in range(0, board_size):
        for x in range(0, board_size):
            if highest_combo < hit_board[x][y]:
                highest_combo = hit_board[x][y]
                best_cord = (x, y)
    return best_cord


# Main game loop
if not position_error():
    while target_left() > 0:
        prob_board = np.zeros((board_size, board_size), dtype=int)
        display_board()
        display_prob_board()
        x, y = hunt_best_option()

        if board[x][y] != "X":
            board[x][y] = "#"
            shots_list.append((x, y))
        elif board[x][y] == "X":
            board[x][y] = "O"
            hit_list = [(x, y)]
            hit_board = np.zeros((board_size, board_size), dtype=int)
            display_board()
            display_hit_board()
            while sort_list(hit_list) not in ship_cords:
                x_hit, y_hit = sink_best_option()

                if board[x_hit][y_hit] not in ("X", "0"):
                    board[x_hit][y_hit] = "#"
                    shots_list.append((x_hit, y_hit))
                    display_board()
                    display_hit_board()
                elif board[x_hit][y_hit] == "X":
                    board[x_hit][y_hit] = "O"
                    hit_list.append((x_hit, y_hit))
                    hit_board = np.zeros((board_size, board_size), dtype=int)
                    display_board()
                    display_hit_board()

            remove = "none"
            for s in ships:
                if ships[s][1] == sort_list(hit_list):
                    remove = s
            del ships[remove]

            for n in hit_list:
                shots_list.append(n)

            hit_list = []
else:
    print("The ships are not positioned properly. The pieces should not overlap")
    display_board()
