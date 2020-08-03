def print_board(arr):
    arr_copy = arr.replace('_', ' ')
    print('---------')
    for i in range(0, len(arr), 3):
        print('|', ' '.join(arr_copy[i:i + 3]), '|')
    print('---------')


def check_status(arr):
    case_0 = abs(arr.count('X') - arr.count('O')) > 1
    case_1 = arr[0] == arr[1] == arr[2] != '_'
    case_2 = arr[3] == arr[4] == arr[5] != '_'
    case_3 = arr[6] == arr[7] == arr[8] != '_'
    case_4 = arr[0] == arr[3] == arr[6] != '_'
    case_5 = arr[1] == arr[4] == arr[7] != '_'
    case_6 = arr[2] == arr[5] == arr[8] != '_'
    case_7 = arr[0] == arr[4] == arr[8] != '_'
    case_8 = arr[2] == arr[4] == arr[6] != '_'

    if case_0 or (case_1 and case_2) or (case_2 and case_3) or (case_1 and case_3) or (case_4 and case_5) or (case_5 and case_6) or (case_4 and case_6):
        print('Impossible')
        return True
    elif case_1:
        print_winner(arr[0])
        return True
    elif case_2:
        print_winner(arr[3])
        return True
    elif case_3:
        print_winner(arr[6])
        return True
    elif case_4:
        print_winner(arr[0])
        return True
    elif case_5:
        print_winner(arr[1])
        return True
    elif case_6:
        print_winner(arr[2])
        return True
    elif case_7:
        print_winner(arr[0])
        return True
    elif case_8:
        print_winner(arr[2])
        return True
    # elif '_' in arr:
    #     print('Game not finished')
    elif '_' not in arr:
        print('Draw')
        return True
    return False


def play(arr, S):
    poss_choice = [1, 2, 3]
    new_arr = [[i for i in arr[6::-3]], [i for i in arr[7:0:-3]], [i for i in arr[8:1:-3]]]
    while True:
        coor = input('Enter the coordinates: ').split()
        try:
            coor[0] = int(coor[0])
            coor[1] = int(coor[1])
        except (ValueError, IndexError):
            print('You should enter numbers!')
            continue
        if coor[0] not in poss_choice or coor[1] not in poss_choice:
            print('Coordinates should be from 1 to 3!')
        else:
            if new_arr[coor[0] - 1][coor[1] - 1] == '_':
                new_arr[coor[0] - 1][coor[1] - 1] = S
                break
            else:
                print('This cell is occupied! Choose another one')
    re_arr = []
    for i in reversed(range(3)):
        for j in range(3):
            re_arr.append(new_arr[j][i])
    print_board(''.join(re_arr))
    return re_arr


def print_winner(S):
    print(f'{S} wins')


def start_game():
    # i = input('Enter cells: ')
    arr = '_________'
    print_board(arr)
    S = 'X'
    while not check_status(arr):
        arr = play(arr, S)
        if S == 'X':
            S = 'O'
        else:
            S = 'X'


start_game()
