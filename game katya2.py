import json
import os
import random


class Player:
    def __init__(self, username):
        self.username = username
        self.reputation = 10  # начальная репутация
        self.exams = {
            "матан": "не сдан",
            "информатика": "не сдан"
        }
        self.artifacts = ["Телефон", "Умные часы", "Шпаргалка"]  # артефакты игрока
        self.story_progress = []  # пройденные ветки
        self.scholarship = True  # стипендия сохранена
        self.lives = 2  # количество попыток на пересдачу

    def add_artifact(self, artifact):
        self.artifacts.append(artifact)

    def add_story_progress(self, branch):
        self.story_progress.append(branch)

    def check_scholarship(self):
        """Проверка сохранения стипендии"""
        if self.exams["матан"] == "3" or self.exams["информатика"] == "3":
            self.scholarship = False
        elif self.exams["матан"] == "не сдан" and self.exams["информатика"] == "4":
            self.scholarship = False
        elif self.exams["матан"] == "4" and self.exams["информатика"] == "3":
            self.scholarship = False
        return self.scholarship

    def to_dict(self):
        """Конвертация в словарь для сохранения"""
        return {
            "username": self.username,
            "reputation": self.reputation,
            "exams": self.exams,
            "artifacts": self.artifacts,
            "story_progress": self.story_progress,
            "scholarship": self.scholarship,
            "lives": self.lives
        }

    @classmethod
    def from_dict(cls, data):
        """Создание объекта из словаря"""
        player = cls(data["username"])
        player.reputation = data["reputation"]
        player.exams = data["exams"]
        player.artifacts = data["artifacts"]
        player.story_progress = data["story_progress"]
        player.scholarship = data["scholarship"]
        player.lives = data["lives"]
        return player


class ArtifactVault:
    """Копилка артефактов"""

    def __init__(self, filename="artifacts.json"):
        self.filename = filename
        self.artifacts = self.load_artifacts()

    def load_artifacts(self):
        """Загрузка артефактов из файла"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Начальный набор артефактов
            default_artifacts = [
                "Зачетка",
                "Конспект по матану",
                "Шпаргалка по информатике",
                "Счастливый билет",
            ]
            self.save_artifacts(default_artifacts)
            return default_artifacts

    def save_artifacts(self, artifacts_list):
        """Сохранение артефактов в файл"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(artifacts_list, f, ensure_ascii=False, indent=2)

    def take_artifact(self, player):
        """Взять артефакт из копилки"""
        if self.artifacts:
            artifact = self.artifacts.pop(0)
            player.add_artifact(artifact)
            self.save_artifacts(self.artifacts)
            print(f"\n Вы получили артефакт: {artifact}")
            print(f" Ваши артефакты: {', '.join(player.artifacts) if player.artifacts else 'нет'}")
            return True
        return False

    def return_artifacts(self, player):
        """Вернуть артефакты в копилку"""
        if player.artifacts:
            self.artifacts.extend(player.artifacts)
            player.artifacts.clear()
            self.save_artifacts(self.artifacts)

    def generate_new_artifacts(self):
        """Генерация новых артефактов если все забраны"""
        if not self.artifacts:
            new_artifacts = [
                "Новый зачетный лист",
                "Экзаменационные билеты",
                "Справка о болезни",
                "Пересдача",
            ]
            self.artifacts = new_artifacts
            self.save_artifacts(new_artifacts)
            print("\n В копилке сгенерированы новые артефакты!")


class Game:
    def __init__(self):
        self.vault = ArtifactVault()
        self.current_player = None
        self.players_file = "players.json"
        self.credentials_file = "users.txt"

    def save_credentials(self, username, password):
        """Сохранение логина и пароля в открытом виде"""
        with open(self.credentials_file, 'a', encoding='utf-8') as f:
            f.write(f"{username}:{password}\n")

    def check_credentials(self, username, password):
        """Проверка логина и пароля"""
        if not os.path.exists(self.credentials_file):
            return False

        with open(self.credentials_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    stored_user, stored_pass = line.strip().split(':')
                    if stored_user == username and stored_pass == password:
                        return True
        return False

    def save_game(self, player):
        """Сохранение игры"""
        if os.path.exists(self.players_file):
            with open(self.players_file, 'r', encoding='utf-8') as f:
                players = json.load(f)
        else:
            players = {}

        players[player.username] = player.to_dict()

        with open(self.players_file, 'w', encoding='utf-8') as f:
            json.dump(players, f, ensure_ascii=False, indent=2)
        print("\n Игра сохранена!")

    def load_game(self, username):
        """Загрузка игры"""
        if not os.path.exists(self.players_file):
            return None

        with open(self.players_file, 'r', encoding='utf-8') as f:
            players = json.load(f)

        if username in players:
            return Player.from_dict(players[username])
        return None

    def register(self):
        """Регистрация нового пользователя"""
        print("РЕГИСТРАЦИЯ НОВОГО ИГРОКА")


        while True:
            username = input("Придумайте логин: ").strip()
            if not username:
                print("Логин не может быть пустым!")
                continue

            # Проверяем, не занят ли логин
            if os.path.exists(self.credentials_file):
                with open(self.credentials_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip() and line.split(':')[0] == username:
                            print("Этот логин уже занят!")
                            break
                    else:
                        break
            else:
                break

        password = input("Придумайте пароль: ").strip()
        self.save_credentials(username, password)

        self.current_player = Player(username)
        print(f"\n Регистрация прошла успешно! Добро пожаловать, {username}!")
        return self.current_player

    def login(self):
        """Вход в систему"""
        print("ВХОД В ИГРУ")

        username = input("Логин: ").strip()
        password = input("Пароль: ").strip()

        if self.check_credentials(username, password):
            # Пробуем загрузить сохраненную игру
            player = self.load_game(username)
            if player:
                self.current_player = player
                print(f"\n Успешный вход! Загружена сохраненная игра.")
                print(f" Репутация: {player.reputation}")
                print(f" Экзамены: {player.exams}")
                print(f" Артефакты: {len(player.artifacts)} шт.")
            else:
                self.current_player = Player(username)
                print(f"\n Успешный вход! Создан новый персонаж.")
            return self.current_player
        else:
            print("\n Неверный логин или пароль!")
            return None

    def intro(self):
        """Вступление к игре"""
        print("ДОБРО ПОЖАЛОВАТЬ В ИГРУ 'СТИПЕНДИЯ В ОПАСНОСТИ!'")
        print("\nВнимание! Ваша главная цель - сохранить стипендию.")
        print("От ваших решений зависит, получите ли вы деньги на жизнь!")
        print("\nУ вас есть:", self.current_player.lives, "попытки на пересдачу")
        print("Текущая репутация:", self.current_player.reputation)

    def math_exam_branch(self):
        """Ветка экзамена по матану"""
        print("ЭКЗАМЕН ПО МАТЕМАТИЧЕСКОМУ АНАЛИЗУ")
        print("\nТы не готов к экзамену, поэтому надо списать.")
        print("Ты тянешь билет и идешь на максимально дальний ряд.")

        self.current_player.add_story_progress("Начало матана")

        if "Шпаргалка по информатике" in self.current_player.artifacts:
            print("\nУ тебя есть шпаргалка, но она по другому предмету...")

        choice = input("\nСписать с заготовленных билетов от одногруппников (1) или использовать Deepseek (2)? ")

        if choice == "1":
            print("РЕЗУЛЬТАТ:")
            print("\nМолодец! Одногруппники честно отнеслись к подготовке,")
            print("в отличие от тебя, поэтому ты сдал экзамен и сохранил стипендию!!")

            if self.vault.take_artifact(self.current_player):
                self.vault.generate_new_artifacts()

            self.current_player.exams["матан"] = "4"
            self.current_player.reputation += 3
            self.current_player.add_story_progress("Списал у одногруппников")

        elif choice == "2":
            print("РЕЗУЛЬТАТ:")
            print("\nДипсик подвел тебя. Преподаватель спрашивает откуда ты это взял,")
            print("пришлось соврать. Отправлен на пересдачу!")

            self.current_player.exams["матан"] = "не сдан"
            self.current_player.reputation -= 5
            self.current_player.lives -= 1
            self.current_player.add_story_progress("Использовал Deepseek")

        else:
            print("\nТы так долго думал, что время вышло! Экзамен не сдан.")
            self.current_player.exams["матан"] = "не сдан"
            self.current_player.lives -= 1

    def cs_exam_branch(self):
        """Ветка экзамена по информатике"""
        print("ЭКЗАМЕН ПО ИНФОРМАТИКЕ")
        print("\nНа трясущихся ногах заходишь в кабинет, где тянешь билет.")
        print("Билет средней сложности, но ты не силен в программировании, надо выкрутиться.")
        print("К Светлане Сергеевне идут ученики, претендующие на пять. Нужна 4.")

        self.current_player.add_story_progress("Начало информатики")

        if "Конспект по матану" in self.current_player.artifacts:
            print("\nУ тебя есть конспект, но это не совсем то...")

        print("\nГотовишься к билету и подходишь к Алексею Владимировичу.")
        print("О нет, Алексей смотрит подозрительно.")
        print("Ответ идет неплохо, но вдруг он вспоминает про не сданные практические задания.")

        choice = input("\nЧто делать: сказать правду (1) или соврать (2)? ")

        if choice == "1":
            print("РЕЗУЛЬТАТ:")
            print("\nАлексею Владимировичу понравилась твоя честность,")
            print("четверка в кармане и плюс 5 к репутации!!")

            if self.vault.take_artifact(self.current_player):
                self.vault.generate_new_artifacts()

            self.current_player.exams["информатика"] = "4"
            self.current_player.reputation += 5
            self.current_player.add_story_progress("Сказал правду")

        elif choice == "2":
            print("РЕЗУЛЬТАТ:")
            print("\nАлексею Владимировичу не показалось правдоподобным твоя речь,")
            print("поэтому он ставит три. Минус 5 к репутации и ты лишился стипендии(")

            self.current_player.exams["информатика"] = "3"
            self.current_player.reputation -= 5
            self.current_player.add_story_progress("Соврал")

        else:
            print("\nТы начал мямлить и не смог ответить. Получаешь 3.")
            self.current_player.exams["информатика"] = "3"
            self.current_player.reputation -= 3

    def retake_exam(self):
        """Процедура пересдачи"""
        print("ПЕРЕСДАЧА!")

        if self.current_player.lives <= 0:
            print("У тебя закончились попытки! Игра окончена.")
            return False

        failed_exams = []
        for exam, status in self.current_player.exams.items():
            if status == "не сдан":
                failed_exams.append(exam)

        if not failed_exams:
            print("У тебя нет несданных экзаменов для пересдачи.")
            return True

        print(f"У тебя осталось {self.current_player.lives} попыток")
        print(f"Экзамены для пересдачи: {', '.join(failed_exams)}")

        if len(failed_exams) > 1:
            choice = input("\nКакой экзамен пересдаем? (матан/информатика): ").lower()
        else:
            choice = failed_exams[0]

        if choice in failed_exams:
            print(f"\nПересдача {choice}...")
            # Шанс 50/50 на успех
            if random.choice([True, False]):
                print("Ура! Пересдача сдана на 4!")
                self.current_player.exams[choice] = "4"
                self.current_player.reputation += 2
            else:
                print("Увы... Пересдача не сдана.")
                self.current_player.lives -= 1
        else:
            print("Такого экзамена нет в списке несданных.")

        return True

    def battle_class(self):
        """Битва классов (дополнительная механика)"""
        print("БИТВА КЛАССОВ: ТЕХНАРИ vs ГУМАНИТАРИИ")

        print("\nВыберите класс за который будете играть:")
        print("1. Технарь (силен в точных науках, +5 к сдаче матана)")
        print("2. Гуманитарий (умеет красиво говорить, +5 к репутации)")

        choice = input("\nВаш выбор (1/2): ")

        if choice == "1":
            print("\n Вы выбрали класс Технарь!")
            print("Вы получаете бонус +5 к сдаче экзамена по матану!")
            self.current_player.artifacts.append("Диплом технаря")

        elif choice == "2":
            print("\n Вы выбрали класс Гуманитарий!")
            print("Вы получаете бонус +5 к репутации!")
            self.current_player.reputation += 5
            self.current_player.artifacts.append("Диплом гуманитария")

        self.current_player.add_story_progress("Выбрал класс")

    def game_loop(self):
        """Основной игровой цикл"""
        self.intro()

        # Битва классов в начале игры
        if "Выбрал класс" not in self.current_player.story_progress:
            self.battle_class()

        # Проверяем, какие экзамены еще не сданы
        exams_to_take = []
        for exam, status in self.current_player.exams.items():
            if status == "не сдан":
                exams_to_take.append(exam)

        if not exams_to_take:
            print("\nВсе экзамены уже сданы!")
            return

        # Выбор первого экзамена
        print("СЕССИЯ НАЧИНАЕТСЯ!")
        print(f"\nКакие экзамены осталось сдать: {', '.join(exams_to_take)}")

        if len(exams_to_take) > 1:
            choice = input("\nКакой экзамен будет первый? (матан/информатика): ").lower()
            while choice not in exams_to_take:
                print("Этот экзамен уже сдан или такого нет!")
                choice = input("Выберите экзамен из списка: ").lower()
        else:
            choice = exams_to_take[0]
            print(f"\nОстался только один экзамен: {choice}")

        # Прохождение выбранной ветки
        if choice == "матан":
            self.math_exam_branch()
        elif choice == "информатика":
            self.cs_exam_branch()

        # Проверяем, нужно ли продолжать
        self.current_player.check_scholarship()

        # Показываем текущий статус
        print("ТЕКУЩИЙ СТАТУС")
        print(f"Репутация: {self.current_player.reputation}")
        print(f"Стипендия: {'сохранена' if self.current_player.scholarship else 'потеряна'}")
        print(f"Экзамены: {self.current_player.exams}")
        print(f"Артефакты: {len(self.current_player.artifacts)} шт.")
        print(f"Попыток на пересдачу: {self.current_player.lives}")

        # Предложение сохраниться
        save_choice = input("\n Хотите сохранить игру? (да/нет): ").lower()
        if save_choice == "да":
            self.save_game(self.current_player)
        else:
            print("\n Прогресс не сохранен! Артефакты возвращаются в копилку.")
            self.vault.return_artifacts(self.current_player)

        # Проверка условий окончания игры
        if not self.current_player.scholarship:
            print("ИГРА ОКОНЧЕНА")
            print("\n Вы потеряли стипендию!")
            print("Попробуйте еще раз, возможно в следующий раз повезет больше.")
            return

        # Проверка на пересдачу
        if "не сдан" in self.current_player.exams.values() and self.current_player.lives > 0:
            retake = input("\nХотите попробовать пересдать? (да/нет): ").lower()
            if retake == "да":
                if self.retake_exam():
                    # Показываем финальный статус
                    print("ФИНАЛЬНЫЙ РЕЗУЛЬТАТ")
                    print(f"Репутация: {self.current_player.reputation}")
                    print(f"Стипендия: {'сохранена' if self.current_player.check_scholarship() else 'потеряна'}")
                    print(f"Экзамены: {self.current_player.exams}")

                    if self.current_player.scholarship:
                        print("\n ПОЗДРАВЛЯЕМ! ВЫ СОХРАНИЛИ СТИПЕНДИЮ! ")
                    else:
                        print("\n Вы не смогли сохранить стипендию. Попробуйте еще раз!")
            else:
                print("\nВы решили не пересдавать. Игра завершена.")
        else:
            # Показываем финальный статус
            print("ФИНАЛЬНЫЙ РЕЗУЛЬТАТ")
            if self.current_player.check_scholarship():
                print("\n ПОЗДРАВЛЯЕМ! ВЫ СОХРАНИЛИ СТИПЕНДИЮ! ")
            else:
                print("\n Вы не смогли сохранить стипендию. Попробуйте еще раз!")

    def main_menu(self):
        """Главное меню"""
        while True:
            print("ГЛАВНОЕ МЕНЮ")
            print("1. Новая игра")
            print("2. Загрузить игру")
            print("3. Выход")

            choice = input("\nВыберите действие: ")

            if choice == "1":
                player = self.register()
                if player:
                    self.game_loop()

                    # Предложение сыграть еще раз
                    again = input("\nХотите сыграть еще раз? (да/нет): ").lower()
                    if again != "да":
                        break

            elif choice == "2":
                player = self.login()
                if player:
                    self.game_loop()

                    # Предложение сыграть еще раз
                    again = input("\nХотите сыграть еще раз? (да/нет): ").lower()
                    if again != "да":
                        break

            elif choice == "3":
                print("\nСпасибо за игру! До свидания!")
                break

            else:
                print("Неверный выбор. Попробуйте еще раз.")


def main():
    """Запуск игры"""
    game = Game()
    game.main_menu()


if __name__ == "__main__":

    main()

