# main.py
import string
import copy
import networkx as nx 
from itertools import product
import matplotlib.pyplot as plt
from progress.bar import Bar

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



'''
# Get input from an image?
# Make tests?
# Remember to keep track of coordinatse of words for doubling - i can incrememnet a counter if it is the same

#Get a better dictionary

#use my own sorting algoirhm for practice?

class Node():
    def __init__(self, letter: str, coords:tuple, double: bool):
        self.letter = letter
        self.coords = coords
        self.double = double


def main():
    raw_board = get_board()
    parsed_board_with_doubles = parse_board(raw_board)
    diamensions = get_diamensions(parsed_board_with_doubles)
    double_coords, parsed_board_no_doubles = find_double_coords(parsed_board_with_doubles, diamensions)
    parsed_board_oop = parse_board_into_oop(parsed_board_no_doubles, diamensions, double_coords)
    all_letter_combos_paths = find_all_letter_combos(parsed_board_oop)
    words = find_words(all_letter_combos_paths)
    points = count_points(parsed_board_oop, double_squares, words)
    print(words)
    print(points)



def get_board():
    """Gets the board from the user as input but does not format"""
    board = input("Board: ") # Board in format WWWW/XXXX/YYYY/ZZZZ where 2 is placed following the letter it doubles
    return board


def parse_board(raw_board):
    """Converts the raw board into a 2d list format"""

    parsed_board = []

    # Converts the board into a 2d list
    parsed_board = raw_board.split("/")
    for row in range(len(parsed_board)):
        parsed_board[row] = list(parsed_board[row])

    print(parsed_board)

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
    
    double_coords = []
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
                        double_coords.append(tuple((row, character_index))) # Adds it to the list
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
            new_board[row_index].append(Node(letter=letter, coords=coords, double=double))

    return new_board


def find_all_letter_combos(board):
    # 1. Find all combos of 2 positions (all start and end coords)
    all_nodes = []
    for row in board:
        for letter in row:
            all_nodes.append(letter)
    # print(all_nodes)
    # We now have all nodes
    # Getting all node combinations:
    all_start_and_end_nodes = list(product(all_nodes, all_nodes))
    #print(all_start_and_end_nodes)
    all_start_and_end_nodes_coords = []
    for node_pair in all_start_and_end_nodes:
        
        for node in node_pair:
            #print(node)
            node_pair_coords = []
            node_pair_coords += (node.coords)
        all_start_and_end_nodes_coords += node_pair_coords
    all_start_and_end_nodes_with_coords_dict = dict(zip(all_start_and_end_nodes, all_start_and_end_nodes_coords))
            

    # 2. Make a network of the board
    ## Loop thorugh the coords and create a list of links of node.coords(-1+1...) and do that for each node?
    edges = []
    # for node in all_nodes:
    #    print(node.letter)
    adjacent_coords = []
    for node in all_nodes:
        x = node.coords[0]
        y = node.coords[1]
        adjacent_coords += [
            (x + 1, y),  
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
            (x + 1, y + 1),
            (x - 1, y + 1),
            (x + 1, y - 1),
            (x - 1, y - 1)
        ]
        
    adjacent_nodes = []
    
    for coords in adjacent_coords:
        for node in all_nodes:
            if node.coords == coords:
                adjacent_nodes.append(node) 
                
    # Debugging Purposes
    edges_info = []
    for node in all_nodes:
        for adjacent_node in adjacent_nodes:
            if abs(node.coords[0] - adjacent_node.coords[0]) <= 1 and abs(node.coords[1] - adjacent_node.coords[1]) <= 1: #Dont need the inverses as their absolute values are the same
                #edges_info.append((node.letter, node.coords, adjacent_node.letter, adjacent_node.coords))
                edges.append((node, adjacent_node)) # MAKE THIS THE ACTUAL NODES< THE LETTERS ARE FOR DEBUGGING
                                                                # ALSO THE LETTERS CANT COPE WITH DUPED LETTERS
        
    edge_list = list(edges)
    G = nx.Graph()
    G.add_edges_from(edge_list)
    #nx.draw_spring(G, with_labels=True)
    #plt.show()
        
    # 3. Use the command to get all paths from start to end coords
    all_paths = []
    
    finding_paths_bar = Bar('Finding Paths', max=len(all_start_and_end_nodes))
    for node_pair in all_start_and_end_nodes:
        #print(node_pair)

        all_paths += nx.all_simple_paths(G, node_pair[0], node_pair[1])
        finding_paths_bar.next()
    finding_paths_bar.finish()
    # 4. Done?
    
    return all_paths
    
    



def find_words(all_letter_combos_paths):
    finding_potential_words_bar = Bar('Finding Potential Words', max=len(all_letter_combos_paths))
    potential_words = []
    for path in all_letter_combos_paths:
        finding_potential_words_bar.next()
        new_word = ""
        for node in path:
            #print(node.letter)
            new_word += node.letter
            #print(new_word)
        potential_words.append(new_word)
    #print(potential_words)
    finding_potential_words_bar.finish()
    
    with open("10000words.txt", "r") as words: 
        """This should be predone!!"""
        words_list = words.readlines()
        cleaning_dict_bar = Bar('Cleaning Dictionary', max=len(words_list))
        cleaned_words_list = []
        for word in words_list:
            cleaning_dict_bar.next()
            cleaned_word = ""
            cleaned_word += word[:-2]
            cleaned_word = cleaned_word.upper()
            cleaned_words_list.append(cleaned_word)
        cleaning_dict_bar.finish()

        finding_correct_words_bar = Bar("Finding Words", max= len(potential_words))
        all_words_in_board = []
        paths_used = []
        final_words =[]
        for potential_word in potential_words:
            finding_correct_words_bar.next()
            if str(potential_word) in cleaned_words_list:
                all_words_in_board.append(potential_word)
                #print(potential_word)
                #Deal with double points tagging here if i can be bothered
                
        for word in all_words_in_board:
            #print(word)
            if len(word) >= 3:
                final_words.append(word)
        finding_correct_words_bar.finish()
                
        print(f"Final words:{final_words}")
        return words, paths_used
        

def count_points(parsed_board, double_squares, words):
    return NotImplementedError

if __name__ == "__main__":
    main()
