# ---------- Дані ----------
inventory = {"зілля": 2, "яблуко": 5}
store = {"меч": 50, "щит": 40, "зілля": 10, "лук": 35}

balance = int(input("Введіть ваш баланс: "))

# ---------- Функції ----------
def view_inventory(inv):
    print("\nІнвентар:")
    if not inv:
        print("Інвентар порожній")
    else:
        for item, count in inv.items():
            print(f"{item} — {count} шт.")

def view_store(store):
    print("\nМагазин:")
    for item, price in store.items():
        print(f"{item} — {price} монет")

def buy_item(item_name, inventory, store, balance):
    # Перевірка наявності предмета
    if item_name not in store:
        raise ValueError("Такого предмета немає в магазині")

    price = store[item_name]

    # Перевірка балансу
    if balance < price:
        raise ValueError("Недостатньо монет для покупки")

    # Покупка
    inventory[item_name] = inventory.get(item_name, 0) + 1
    balance -= price

    return balance

# ---------- Головне меню ----------
while True:
    print("\n====== МЕНЮ ======")
    print("1. Переглянути інвентар")
    print("2. Переглянути магазин")
    print("3. Купити предмет")
    print("4. Перевірити баланс")
    print("0. Вийти")

    choice = input("Оберіть дію: ")

    if choice == "1":
        view_inventory(inventory)

    elif choice == "2":
        view_store(store)

    elif choice == "3":
        item = input("Введіть назву предмета: ")
        try:
            balance = buy_item(item, inventory, store, balance)
            print(f"Ви купили '{item}'. Баланс: {balance} монет")
        except ValueError as e:
            print(f"Помилка: {e}")

    elif choice == "4":
        print(f"Ваш баланс: {balance} монет")

    elif choice == "0":
        print("Вихід з програми")
        break

    else:
        print("Невірний вибір, спробуйте ще раз")
