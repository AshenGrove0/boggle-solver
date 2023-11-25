# main.py
import string

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


#use my own sorting algoirhm for practice?
def main():
    raw_board = get_board()
    parsed_board = parse_board(raw_board)
    diamensions = get_diamensions(parsed_board)
    double_coords, parsed_board_no_doubles = find_double_coords(parsed_board, diamensions)
    all_letter_combos = find_all_letter_combos(parsed_board_no_doubles)
    words = find_words(all_letter_combos)
    points = count_points(parsed_board, double_squares, words)
    print(words)
    print(points)



def get_board():
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
    print(line_length)

    return (line_count, line_length)



def find_double_coords(parsed_board, diamensions):
    
    double_coords = []

    for line in range(len(parsed_board)):
        if len(parsed_board[line]) != diamensions[1]: # Number of letters in a line
            for character in range(len(parsed_board[line])):
                if parsed_board[line][character] not in LETTERS_LIST:
                    if parsed_board[line][character] == 2 or parsed_board[line][character] == "2":
                        double_coords.append(tuple((line, character))) # Adds it to the list
                        parsed_board[line].remove(parsed_board[line][character]) # Formats the parsed list to get rid of it
                    else:
                        print("Your board is not possible. Please only use letters and the number 2. Check for spaces.")
    print("Coords of double tiles: "+ double_coords)

    return double_coords, parsed_board





def find_words(board):
    with open("safedict_full.txt", "r") as words:
        words_list = words.readlines()
        if my_word in words_list:
            print("Found")


if __name__ == "__main__":
    main()
