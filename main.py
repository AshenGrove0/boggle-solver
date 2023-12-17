# main.py
import string
import copy
import networkx as nx 
from itertools import product
import matplotlib.pyplot as plt
from progress.bar import Bar
import time
import concurrent.futures

 
# Get lowercase and uppercase letters
LOWERCASE_LETTERS = list(string.ascii_lowercase)
UPPERCASE_LETTERS = list(string.ascii_uppercase)

# Combine them into a single list
LETTERS_LIST = LOWERCASE_LETTERS + UPPERCASE_LETTERS

#Sample boards:
'''
WWWW/XXXX/YYYY/ZZZZ
WWWW/XX2XX/Y2YYY/ZZZZ
AAAA/BBBB/CCCC/EEEE
ABCD/EFGH/IJKL/MNOP
EA/RT/ON/SL
FEOV/YIG2T/SNNW/AIHI
ABC/DEF/GHI
AAA/BBB/CCC/DDD

'''

class Node():
    def __init__(self, letter: str, coords:tuple, is_double: bool):
        self.letter = letter
        self.coords = coords
        self.is_double = is_double


def main():
    raw_board = get_board()
    start_time = time.time()
    parsed_board_with_doubles = parse_board(raw_board)
    diamensions = get_diamensions(parsed_board_with_doubles)
    double_coords, parsed_board_no_doubles = find_double_coords(parsed_board_with_doubles, diamensions)
    parsed_board_oop = parse_board_into_oop(parsed_board_no_doubles, diamensions, double_coords)
    all_letter_combos_paths = find_all_letter_combos(parsed_board_oop)
    words, double_words = find_words(all_letter_combos_paths)
    points = count_points(words, double_words)
    print(f"Words: {words}")
    print(f"Double words: {double_words}")
    print(f"Points (if no doubles): {points}")
    print(f"Time: {time.time() - start_time}")



def get_board():
    """Gets the board from the user as input but does not format"""
    board = input("Board: ") # Board in format WWWW/XXXX/YYYY/ZZZZ where 2 is placed following the letter it doubles
    return board


def parse_board(raw_board):
    """Converts the raw board into a 2d list format"""
    parsed_board = [list(row) for row in raw_board.split("/")]

    '''
    Format:
    [
        ["W", "W", "W", "W",],
        ["X", "X", "X", "X",],
        ["Y", "Y", "Y", "Y",],
        ["Z", "Z", "Z", "Z",],
    ]
    '''
    return parsed_board
    

def get_diamensions(parsed_board):
    '''Gets the diamensions for the board, allowing it to work as a rectangle'''

    # Gets line count
    line_count = len(parsed_board)

    # Gets line length
    line_length = 0
    
    for letter in parsed_board[0]:
        if letter in LETTERS_LIST:
            line_length += 1

    return (line_count, line_length)


def find_double_coords(parsed_board, diamensions):
    """Gets the coordinates of double points locations and returns them as a list of tuples"""

    double_coords = set()
    rows = diamensions[0]
    letters_per_row = diamensions[1]
    parsed_board_no_doubles = copy.deepcopy(parsed_board)  # need to deepcopy to not affect original, else index errors will occur

    for row in range(rows):
        current_row = parsed_board[row]
        current_row_length = len(current_row)
        if current_row_length != letters_per_row: # If there are non-letter characters in the row
            

            for character_index in range(current_row_length):
                character = parsed_board[row][character_index]

                if character not in LETTERS_LIST:

                    if character == 2 or character == "2":
                        double_coords.add(tuple((row, character_index-1))) # Adds it to the list
                        parsed_board_no_doubles[row].remove(character) # Formats the parsed list to get rid of it
                    else:
                        print("Your board is not possible. Please only use letters and the number 2. Check for spaces.")

    print("Coords of double tiles: ", double_coords)
    print("Clean Board: ", parsed_board_no_doubles)

    return double_coords, parsed_board_no_doubles

def parse_board_into_oop(original_board, diamensions, double_coords):
    new_board = []

    for row_index in range(len(original_board)):
        new_board.append([])
        for letter_index in range(len(original_board[row_index])):
            letter = original_board[row_index][letter_index]
            coords = (row_index, letter_index)
            double = coords in double_coords
            new_board[row_index].append(Node(letter=letter, coords=coords, is_double=double))

    return new_board


def find_all_letter_combos(board):
    """Turns board into network & Finds all letter combos using concurrency magic"""
    edges = []
    all_nodes = [node for row in board for node in row]
    
    all_start_and_end_nodes = list(product(all_nodes, repeat=2))
    all_start_and_end_nodes_bar = Bar('Finding Start and end nodes', max=len(all_start_and_end_nodes)/16)
    for i, node in enumerate(all_nodes):
        all_start_and_end_nodes_bar.next()
        x, y = node.coords
        adjacent_coords = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
            (x + 1, y + 1),
            (x - 1, y + 1),
            (x + 1, y - 1),
            (x - 1, y - 1)
        ]

        adjacent_nodes = [n for n in all_nodes if n.coords in adjacent_coords]
        edges.extend((node, adj_node) for adj_node in adjacent_nodes)
    all_start_and_end_nodes_bar.finish()
    edge_list = list(edges)
    G = nx.Graph()
    G.add_edges_from(edge_list)

    all_adjacent_nodes = [list(G.neighbors(node)) for node in all_nodes]
    
    for node in all_nodes:
        for adjacent_node in adjacent_nodes:
            if abs(node.coords[0] - adjacent_node.coords[0]) <= 1 and abs(node.coords[1] - adjacent_node.coords[1]) <= 1:
                edges.append((node, adjacent_node))
    
    edge_list = list(edges)
    G = nx.Graph()
    G.add_edges_from(edge_list)
    
    # Use concurrent.futures for parallel execution
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(find_paths_for_node_pair, node_pair, G) for node_pair in all_start_and_end_nodes]
        all_paths = [future.result() for future in concurrent.futures.as_completed(futures)]

    return all_paths

def find_paths_for_node_pair(node_pair, G):
    return list(nx.all_simple_paths(G, node_pair[0], node_pair[1]))
    
    



def find_words(all_letter_combos_paths):
    """This crashes with a real board so i should make it slightly more efficient """
    finding_potential_words_bar = Bar('Finding Potential Words', max=len(all_letter_combos_paths))
    potential_words = set()
    words_with_double_points = set()
    for path_collection in all_letter_combos_paths:
        finding_potential_words_bar.next()
        for path in path_collection:
            new_word = ''.join(node.letter for node in path)
            potential_words.add(new_word)
            if any(node.is_double for node in path):
                words_with_double_points.add(new_word)
    finding_potential_words_bar.finish()

    
    with open("safedict_full.txt", "r") as words_1:
        with open("safedict_complex.txt", "r") as words_2:
            """This should be predone!! and also remove all words less than 3 letters long"""
            words_list = set(words_1.readlines() + words_2.readlines())
            cleaned_words_list = {word.strip().upper() for word in words_list if len(word) >= 3}

        letter_combos_longer_than_three = []
        print("Don't worry, it's not hanging its going great :)")
        letter_combos_longer_than_three = potential_words.intersection(cleaned_words_list) #OMG this is so fast
        print("Don't worry, it's not hanging its going great")
        
        
        finding_correct_words_bar_2 = Bar("Finding Words Check 2/2", max=len(letter_combos_longer_than_three))

        paths_used = []
        final_words =[]
        
        final_words = [word for word in letter_combos_longer_than_three if len(word) >= 3]
        double_words = []
        for word in words_with_double_points:
            if word in final_words:
                double_words.append(word)
        finding_correct_words_bar_2.finish()     
        return final_words, double_words
    

def count_points(words, double_words):
    points = 0
    for word in words:
        this_word_points = 0
        match len(word):
            case 3:
                this_word_points += 1
            case 4:
                this_word_points += 1
            case 5:
                this_word_points += 2
            case 6:
                this_word_points += 3
            case 7:
                this_word_points += 5
            case _:  # 8 or higher as all below 3 have been filtered out
                this_word_points += 11
        if word in double_words:
            this_word_points *= (2*double_words.count(word))
        print(this_word_points)
        # There is some issue with doubles being deleted if they are duplicated
        points += this_word_points
    return points
                
            




if __name__ == "__main__":
    main()
