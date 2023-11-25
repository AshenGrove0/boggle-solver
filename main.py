# main.py


#use my own sorting algoirhm for practice?
def main():
    board = get_board()
    parsed_board = parse_board(board)
    all_letter_combos = find_all_letter_combos(parsed_board)
    words = find_words(all_letter_combos)
    points = count_points(board, words)
    print(words)
    print(points)



def get_board():
    board = input("Board: ") # Board in format WWWW/XXXX/YYYY/ZZZZ
    return board

def parse_board(board):
    parsed_board = []

    for line in range(4):
        parsed_board.append([])
        for letter in range(4):
            parsed_board[line].append(board[letter])
    print(parsed_board)
    


def find_words(board):
    with open("safedict_full.txt", "r") as words:
        words_list = words.readlines()
        if my_word in words_list:
            print("Found")


if __name__ == "__main__":
    main()
