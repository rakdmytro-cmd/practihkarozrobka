from storage import save_state, load_state


def show_state(state):
    print("\n=== GAME STATE ===")
    for key, value in state.items():
        print(f"{key}: {value}")
    print("=================\n")


def main():
    default_state = {
        "player_name": "Player",
        "level": 1,
        "coins": 0,
        "inventory": {},
        "settings": {
            "volume": 50,
            "difficulty": "normal"
        }
    }

    game_state = load_state("save.json", default_state)

    while True:
        print("1) Показати стан")
        print("2) Додати монети")
        print("3) Додати предмет")
        print("4) Зберегти")
        print("5) Вийти")

        choice = input("Ваш вибір: ")

        if choice == "1":
            show_state(game_state)

        elif choice == "2":
            try:
                amount = int(input("Скільки монет додати? "))
                if amount >= 0:
                    game_state["coins"] += amount
                else:
                    print("Число має бути додатним!")
            except ValueError:
                print("Введіть ціле число!")

        elif choice == "3":
            name = input("Назва предмета: ")
            try:
                qty = int(input("Кількість: "))
                if qty < 0:
                    print("Кількість має бути додатною!")
                    continue

                inv = game_state["inventory"]
                inv[name] = inv.get(name, 0) + qty
            except ValueError:
                print("Введіть ціле число!")

        elif choice == "4":
            if save_state("save.json", game_state):
                print("Збережено успішно!")
            else:
                print("Помилка збереження!")

        elif choice == "5":
            ans = input("Зберегти перед виходом? (так/ні): ").lower()
            if ans == "так":
                save_state("save.json", game_state)
            print("До побачення!")
            break

        else:
            print("Невірний пункт меню!")


if __name__ == "__main__":
    main()
