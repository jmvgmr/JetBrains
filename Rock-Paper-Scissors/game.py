import random


class Game:
    def __init__(self):
        self.players = []
        self.game_list = ['rock', 'paper', 'scissors']

    def set_game_list(self, lst):
        self.game_list = lst

    def check_player(self, name):
        for player in self.players:
            if player.name == name:
                return player
        new_player = Player(name)
        self.players.append(new_player)
        return new_player

    def play(self, player):
        rival = random.choice(self.game_list)
        idx_player = self.game_list.index(player)
        length = len(self.game_list)
        start_idx = (idx_player + 1) % length
        end_idx = (idx_player + length // 2) % length + 1
        if start_idx >= end_idx:
            lose_to = self.game_list[start_idx:] + self.game_list[:end_idx]
        else:
            lose_to = self.game_list[start_idx: end_idx]
        if rival in lose_to:
            print(f'Sorry, but computer chose {rival}')
            return 0
        elif player == rival:
            print(f'There is a draw ({rival})')
            return 50
        else:
            print(f'Well done. Computer chose {rival} and failed')
            return 100


class Player:
    def __init__(self, name, score=0):
        self.name = name
        self.score = score

    def rating(self):
        print(f'Your rating: {self.score}')

    def update_score(self, points):
        self.score += points


game = Game()

try:
    with open('rating.txt') as file:
        for line in file.readlines():
            user = Player(line.split()[0], int(line.split()[1]))
            game.players.append(user)
except FileNotFoundError:
    pass

name_player = input('Enter your name: ')
user = game.check_player(name_player)
print(f'Hello, {user.name}')

game_type = input().split(',')
if game_type != ['']:
    game.game_list = game_type
print('Okay, let\'s start')
while True:
    inp = input()
    if inp == '!exit':
        print('Bye!')
        break
    elif inp == '!rating':
        user.rating()
    elif inp in game.game_list:
        user.update_score(game.play(inp))
    else:
        print('Invalid input')

with open('rating.txt', 'w') as file:
    for user in game.players:
        file.write(f'{user.name} {user.score}\n')
