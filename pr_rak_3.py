class Character():
    def __init__ (self, name, hp):
        self.name = name
        self.hp = hp
    
    def attack(self):
        print(f"{self.name} атакує")
    
    def take_damage(self, damage):
        self.hp -= damage
        print(f"{self.name} отримав {damage}")
        print(f"залишилося HP: {self.hp}")

    def __str__(self):
        return f"Персонаж: {self.name}, HP: {self.hp}"

class Player(Character):
    def __init__ (self, name, hp, level):
        super().__init__(name, hp)
        self.level = level
    
    def level_up(self):
        self.level +=1
        print(f"{self.name} підвищив рівень до {self.level}")

class Enemy(Character):
    def __init__ (self, name, hp, damage):
        super().__init__(name,hp)
        self.damage = damage
    
    def attack(self, shock):
        print (f"{self.name} атакує і завдає {self.damage} шкоди")
        shock.take_damage(self.damage)

class Item():
    def __init__ (self, name, item_type):
        self.name = name
        self.item_type = item_type
    
    def use(self, shock):
        pass

class Heal(Item):
    def __init__(self, name, heal_amount):
        super().__init__(name, "heal")
        self.heal_amount = heal_amount

    def use(self, shock):
        shock.hp += self.heal_amount
        print(f"{shock.name} використав {self.name} і відновив {self.heal_amount} HP")
        print(f"Поточне HP: {shock.hp}")

player = Player("Селянин", 100, 12)
enemy = Enemy("Зомби", 50, 20)

heal = Heal("зілля лікування", 30)

print(player)
print(enemy)

heal.use(player)
enemy.attack(player)

player.attack()

print(player)
print(enemy)