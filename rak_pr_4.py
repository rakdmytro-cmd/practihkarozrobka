inventory = {"зілля": 2, "меч": 1}

store = {"меч": 60, "щит": 70, "зілля": 15, "броня": 100}

balance = int(input("Введіть ваш баланс: "))
# Перегляд інвентарю
def view_inventory(inventory):
    print("Ваш інвентар:")
    if not inventory:
        print("Інвентар порожній")
    else:
        for item, count in inventory.items():
            print(f"{item} x{count}")

def view_store(store):
    print("Магазин:")
    for item, price in store.items():
        print(f"{item} - {price} монет")


def buy_item(item_name, inventory, store, balance):
    # 1. Перевірка наявності предмета
    if item_name not in store:
        raise ValueError("Такого предмета немає в магазині")

    price = store[item_name]

    # 2. Перевірка балансу
    if balance < price:
        raise ValueError("Недостатньо монет для покупки")

    # 3. Додавання предмета в інвентар
    if item_name in inventory:
        inventory[item_name] += 1
    else:
        inventory[item_name] = 1

    balance -= price
    print(f"Ви купили {item_name} за {price} монет")

    return balance

while True:
    print("\n=== МЕНЮ ===")
    print("1 - Переглянути інвентар")
    print("2 - Переглянути магазин")
    print("3 - Купити предмет")
    print("4 - Перевірити баланс")
    print("0 - Вийти")

    choice = input("Ваш вибір: ")

    if choice == "1":
        view_inventory(inventory)

    elif choice == "2":
        view_store(store)

    elif choice == "3":
        item = input("Введіть назву предмета: ")
        try:
            balance = buy_item(item, inventory, store, balance)
        except ValueError as e:
            print(f"Помилка: {e}")

    elif choice == "4":
        print(f"Ваш баланс: {balance} монет")

    elif choice == "0":
        print("До побачення!")
        break

    else:
        print("Невірний вибір!")
