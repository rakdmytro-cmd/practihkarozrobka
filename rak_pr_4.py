import logging

# ---------------- ЛОГУВАННЯ ----------------
logging.basicConfig(
    filename="shop.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
# ---------------- ДАНІ ----------------
inventory = {"зілля": 2, "ключ": 1}
store = {"меч": 50, "щит": 40, "зілля": 10, "амулет": 30}
balance = int(input("Введіть ваш баланс: "))

# ---------------- ФУНКЦІЇ ----------------
def view_inventory(inventory):
    print("\n Ваш інвентар:")
    if not inventory:
        print("Інвентар порожній")
    else:
        for item, count in inventory.items():
            print(f"- {item}: {count} шт.")


def view_store(store):
    print("\n Магазин:")
    for item, price in store.items():
        print(f"- {item}: {price} монет")


def buy_item(item_name, inventory, store, balance):
    if item_name not in store:
        logging.error(f"Спроба купити неіснуючий предмет: {item_name}")
        raise ValueError("Такого предмета немає в магазині")

    price = store[item_name]

    if balance < price:
        logging.error(
            f"Недостатньо монет для покупки {item_name}. Баланс: {balance}, ціна: {price}"
        )
        raise ValueError("Недостатньо монет для покупки")

    # покупка
    balance -= price
    inventory[item_name] = inventory.get(item_name, 0) + 1

    logging.info(f"Куплено предмет: {item_name} за {price} монет")
    return balance


# ---------------- ОСНОВНА ПРОГРАМА ----------------
while True:
    print("\n--- МЕНЮ ---")
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
            print(f"Предмет '{item}' успішно куплено!")
        except ValueError as e:
            print(f"Помилка: {e}")

    elif choice == "4":
        print(f"Ваш баланс: {balance} монет")

    elif choice == "0":
        print("Вихід з програми")
        break

    else:
        print("Невірний вибір")
