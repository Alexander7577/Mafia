import random


class PlayerSelectionError(Exception):
    pass


class InputError(Exception):
    pass


class Player:
    def __init__(self, name):
        self.name = name
        self.live = True
        self.age = random.randint(16, 40)
        self.gender = random.choice(["Мужчина", "Женщина"])
        self.intuition = random.choice(['Слабая', 'Стандартная', 'Повышенная'])
        self.speech = random.choice(['Малоразвитая', 'Стандартная', 'Развитая'])

    def user_choose_vote_target(self, players):
        target_name = input("Против кого будете голосовать? Введите имя игрока: ")
        for player in players:
            if player.name == target_name:
                return player

    def ai_choose_vote_target(self, players):
        valid_targets = [player for player in players if player.live and player != self]
        excluded = random.choice(valid_targets)
        return excluded

    def ai_choose_target(self, players):
        pass

    def user_choose_target(self, players):
        pass

    def __str__(self):
        return self.name


class Mafia(Player):
    def __init__(self, name):
        super().__init__(name)
        self.role = "Мафия"

    def ai_choose_target(self, players):
        valid_targets = [player for player in players if player.live and player.role != "Мафия"]
        return random.choice(valid_targets)

    def user_choose_target(self, players):
        target_name = input("Кого хотите убить? Введите имя игрока: ")
        for player in players:
            if player.name == target_name:
                return player


class Sheriff(Player):
    def __init__(self, name):
        super().__init__(name)
        self.role = 'Шериф'

    def ai_choose_target(self, players):
        valid_targets = [player for player in players if player.live and player.role != "Шериф"]
        return random.choice(valid_targets)

    def user_choose_target(self, players):
        target_name = input("Кого хотите раскрыть? Введите имя игрока: ")
        for player in players:
            if player.name == target_name:
                return player


class Doctor(Player):
    def __init__(self, name):
        super().__init__(name)
        self.role = 'Доктор'

    def ai_choose_target(self, players):
        valid_targets = [player for player in players if player.live]
        return random.choice(valid_targets)

    def user_choose_target(self, players):
        target_name = input("Кого хотите вылечить? Введите имя игрока: ")
        for player in players:
            if player.name == target_name:
                return player


class Civilian(Player):
    def __init__(self, name):
        super().__init__(name)
        self.role = 'Обитатель'


class MafiaGame:
    def __init__(self, player_name, num_bots, player_role=None):
        self.__players = self.__create_players(player_name, num_bots, player_role)

    def __create_players(self, player_name, num_bots, player_role=None):
        roles = [Mafia, Sheriff, Doctor]
        roles += [Civilian] * num_bots
        random.shuffle(roles)
        players = []

        # Создание роли для игрока
        if player_role is None:
            player_role = roles.pop()(player_name)
            print(f'Вам выпала роль {player_role.role}!')
            players.append(player_role)
        elif player_role is not None:
            roles.remove(player_role)
            player_role = player_role(player_name)
            print(f'Поздравляем, вы теперь {player_role.role}!')
            players.append(player_role)


        # Создание ролей для ботов
        for _ in range(len(roles)):
            bot_name = f'Бот {len(players)}'
            bot_role = roles.pop()(bot_name)
            players.append(bot_role)

        return players

    def play(self):
        print('Игра началась')
        print('Список игроков:')
        for player in self.__players:
            if isinstance(player, Player) and player.live:
                print(f"{player}")

        while True:
            print("\n--- Ночь ---")

            killed = []

            for player in self.__players:
                if player.live and player.role == 'Мафия' and player.name == player_name:
                    print(f"\nВы ходите!")
                    while True:
                        try:
                            target = player.user_choose_target(self.__players)
                            if target.live and target != player:
                                killed.append(target)
                                break
                            else:
                                raise PlayerSelectionError('Вы пытаетесь убить мёртвого/исключенного игрока или себя')
                        except PlayerSelectionError as e:
                            print(print(f'{e}, Повторите попытку!'))

                        except AttributeError:
                            print('Такого игрока не существует')

                if player.live and player.role == 'Мафия' and player.name != player_name:
                    print(f"\nМафия выбирает цель!")
                    target = player.ai_choose_target(self.__players)
                    if target.live and target != player:
                        killed.append(target)
                    else:
                        raise PlayerSelectionError('Нельзя убить этого игрока!')

            for player in self.__players:
                if player.live and player.role == 'Шериф' and player.name == player_name:
                    print(f"\nВы ходите!")
                    while True:
                        try:
                            target = player.user_choose_target(self.__players)
                            if target.live and target != player:
                                if target.role == 'Мафия':
                                    print(f'Этот игрок мафия, скоре исключайте его!!!')
                                    break
                                else:
                                    print('Этот игрок не мафия!')
                                    break
                            else:
                                raise PlayerSelectionError('Вы пытаетесь раскрыть мёртвого игрока или себя')

                        except PlayerSelectionError as e:
                            print(f'{e}, Повторите попытку!')
                        except AttributeError:
                            print('Такого игрока не существует')

                if player.live and player.role == 'Шериф' and player.name != player_name:
                    print(f"\nШериф ищет мафию!")
                    target = player.ai_choose_target(self.__players)
                    if target and target.live and target != player:
                        pass
                    else:
                        raise PlayerSelectionError('Нельзя раскрыть этого игрока!')

            for player in self.__players:
                if player.live and player.role == 'Доктор' and player.name == player_name:
                    print(f"\nВы ходите!")
                    while True:
                        try:
                            target = player.user_choose_target(self.__players)
                            if target in killed:
                                killed.remove(target)
                                break

                            if not target.live:
                                raise PlayerSelectionError('Нельзя вылечить мёртвого игрока!')
                            break
                        except PlayerSelectionError as e:
                            print(f'{e}, повторите попытку')
                        except AttributeError:
                            print('Такого игрока не существует')

                if player.live and player.role == 'Доктор' and player.name != player_name:
                    print(f"\nДоктор кого-то лечит!")
                    target = player.ai_choose_target(self.__players)
                    if target in killed:
                        killed.remove(target)

            if killed:
                killed[0].live = False

            print("\n--- Утро ---")
            eliminated_player = None

            if killed:
                print(f'Этой ночью был убит игрок {killed[0]}')
            else:
                print('этой ночью никто не умер')

            for player in self.__players:
                if isinstance(player, Player):
                    print(f"{player}: {'жив' if player.live else 'мертв'}")

            while True:
                try:
                    alive_players = [player for player in self.__players if player.live]
                    if len(alive_players) == 2:
                        break

                    print("\n--- Голосование ---")
                    votes = {}
                    eliminated_player = None

                    for player in self.__players:
                        votes[player] = 0

                    for player in self.__players:
                        if player.live and player.name == player_name:
                            vote_target = player.user_choose_vote_target(self.__players)
                            if not vote_target.live:
                                raise PlayerSelectionError('Вы голосуете против мёртвого игрока')

                            if vote_target:
                                print('---------------------------------------------')
                                print(f'игрок {player} голосует против {vote_target}')
                                votes[vote_target] += 1

                        if player.live and player.name != player_name:
                            vote_target = player.ai_choose_vote_target(self.__players)

                            if vote_target:
                                print('---------------------------------------------')
                                print(f'игрок {player} голосует против {vote_target}')
                                votes[vote_target] += 1

                    max_votes = max(votes.values())
                    players_with_max_votes = [player for player, vote_count in votes.items() if vote_count == max_votes]

                    if len(players_with_max_votes) > 1:
                        print("\nИгроки", ", ".join(str(player) for player in players_with_max_votes),
                              "набрали одинаковое количество голосов.")
                        print('Голосование начинается заново!')
                        continue

                    eliminated_player = players_with_max_votes[0]
                    print('---------------------------------------------')
                    print('Игроки проголосовали')
                    for key, value in votes.items():
                        if key.live:
                            print(f'против {key} проголосвали: {value}')

                    if eliminated_player:
                        eliminated_player.live = False
                        print(f"\nПо результатам голосования {eliminated_player} был исключен.")
                    break
                except PlayerSelectionError as e:
                    print(f'{e}, повторите попытку')
                except AttributeError:
                    print('Такого игрока не существует')

            winner = self.__check_win()
            if winner == 'Мафия':
                print("\nИгра окончена. Тьма накрывает город, мафиози взяли верх, закатывая город во мрак. Победа Мафии!")
                break
            if winner == 'Мирные жители':
                print("\nИгра окончена. Свет восторжествовал! Город освобожден от теней мафии. Победа мирных жителей!")
                break

    def __check_win(self):
        mafia_count = 0
        civilian_count = 0

        for player in self.__players:
            if isinstance(player, Mafia) and player.live:
                mafia_count += 1
            elif isinstance(player, (Sheriff, Doctor, Civilian)) and player.live:
                civilian_count += 1

        if civilian_count <= mafia_count:
            return "Мафия"
        elif mafia_count == 0:
            return "Мирные жители"


if __name__ == '__main__':
    player_name = input("Введите ваше имя: ")
    while True:
        try:
            num_bots = int(input("Введите количество ботов (от 3 до 9): ")) - 2
            if (num_bots + 2) < 3 or (num_bots + 2) > 9:
                raise InputError('Вы указали недопустимое количество ботов')
            role_choice = input("Выберите роль (1 - Мафия, 2 - Шериф, 3 - Доктор, 4 - Обитатель, 5 - Случайно): ")
            if role_choice.isdigit() and 1 <= int(role_choice) <= 5:
                if int(role_choice) == 1:
                    player_role = Mafia
                elif int(role_choice) == 2:
                    player_role = Sheriff
                elif int(role_choice) == 3:
                    player_role = Doctor
                elif int(role_choice) == 4:
                    player_role = Civilian
                else:
                    player_role = None
                break
            else:
                raise InputError("Некорректный выбор роли.")

        except InputError as e:
            print(f'{e}, Повторите попытку!')

        except ValueError:
            print(f'Вы ввели не число, Повторите попытку!')

    game = MafiaGame(player_name, num_bots, player_role)
    game.play()
