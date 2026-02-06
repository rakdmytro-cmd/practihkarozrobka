# Завдання 1: Клас Character
class Character:
    def __init__(self, name, hp):
        self.name = name  # Ім'я персонажа
        self.hp = hp      # Здоров'я персонажа

    def attack(self):
        """Метод для атаки"""
        print(f"{self.name} атакує!")

    def take_damage(self, damage):
        """Метод для отримання шкоди"""
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        print(f"{self.name} отримав {damage} шкоди, залишилось HP: {self.hp}")

    def is_alive(self):
        """Перевірка, чи персонаж живий"""
        return self.hp > 0


# Завдання 2: Клас Player
class Player(Character):
    def __init__(self, name, hp, level):
        super().__init__(name, hp)
        self.level = level  # Рівень гравця

    def level_up(self):
        """Підвищення рівня"""
        self.level += 1
        print(f"{self.name} підвищив рівень до {self.level}")


# Завдання 3: Клас Enemy
class Enemy(Character):
    def __init__(self, name, hp, damage):
        super().__init__(name, hp)
        self.damage = damage  # Шкода ворога

    def attack(self):
        """Атака ворога"""
        print(f"{self.name} атакує і завдає {self.damage} шкоди!")


# Завдання 4: Клас Item
class Item:
    def __init__(self, name, item_type):
        self.name = name           # Назва предмета
        self.item_type = item_type # Тип предмета

    def use(self):
        """Використання предмета"""
        print(f"{self.name} використано!")


# Завдання 5: Механіка взаємодії
player = Player("Селянин", 100, 1)
enemy = Enemy("Зомбі", 50, 15)
item = Item("Зілля", "зілля")

while True:
    print("\n1 - Атакувати")
    print("2 - Використати предмет")
    print("3 - Підвищити рівень")
    print("0 - Вийти")

    choice = input("Виберіть дію: ")

    if choice == "1":
        player.attack()
        enemy.take_damage(10)

        # Якщо ворог помер — гра завершується
        if not enemy.is_alive():
            print("Ви перемогли ворога!")
            break

        enemy.attack()
        player.take_damage(enemy.damage)

        # Якщо гравець помер — гра завершується
        if not player.is_alive():
            print("Ви програли!")
            break

    elif choice == "2":
        item.use()

    elif choice == "3":
        player.level_up()

    elif choice == "0":
        print("Кінець гри")
        break

    else:
        print("Невірний вибір")
