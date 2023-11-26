# main.py
import string
import copy


# Get lowercase and uppercase letters
LOWERCASE_LETTERS = list(string.ascii_lowercase)
UPPERCASE_LETTERS = list(string.ascii_uppercase)

# Combine them into a single list
LETTERS_LIST = LOWERCASE_LETTERS + UPPERCASE_LETTERS

#Sample boards:
'''
WWWW/XXXX/YYYY/ZZZZ
WWWW/XX2XX/Y2YYY/ZZZZ


'''

# Make tests?
# Remember to keep track of coordinatse of words for doubling - i can incrememnet a counter if it is the same

#use my own sorting algoirhm for practice?
def main():
    raw_board = get_board()
    parsed_board_with_doubles = parse_board(raw_board)
    diamensions = get_diamensions(parsed_board_with_doubles)
    double_coords, parsed_board_no_doubles = find_double_coords(parsed_board_with_doubles, diamensions)
    all_letter_combos = find_all_letter_combos(parsed_board_no_doubles)
    words = find_words(all_letter_combos)
    points = count_points(parsed_board_no_doubles, double_squares, words)
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
    """Obtains the coordinates of double points locations and returns them as a list of tuples"""
    
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


def find_all_letter_combos(parsed_board_no_doubles):
    return NotImplementedError


def find_words(board):
    with open("safedict_full.txt", "r") as words:
        words_list = words.readlines()
        return NotImplementedError
        

def count_points(parsed_board, double_squares, words):
    return NotImplementedError

if __name__ == "__main__":
    main()
