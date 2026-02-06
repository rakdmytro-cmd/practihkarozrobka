from storage import save_state, load_state


def print_state(state):
    print("\nПоточний стан гри:")
    print(f"Гравець: {state['player_name']}")
    print(f"Рівень: {state['level']}")
    print(f"Монети: {state['coins']}")
    print("Інвентар:")
    for item, count in state["inventory"].items():
        print(f"  {item}: {count}")
    print("Налаштування:", state["settings"])
    print()


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
        print("""
1) Показати стан
2) Додати монети
3) Додати предмет в інвентар
4) Зберегти
5) Вийти
""")
        choice = input("Обери дію: ")

        if choice == "1":
            print_state(game_state)

        elif choice == "2":
            try:
                amount = int(input("Скільки монет додати? "))
                if amount >= 0:
                    game_state["coins"] += amount
                else:
                    print("Число має бути додатне")
            except ValueError:
                print("Введи ціле число")

        elif choice == "3":
            name = input("Назва предмета: ")
            try:
                qty = int(input("Кількість: "))
                if qty >= 0:
                    game_state["inventory"][name] = game_state["inventory"].get(name, 0) + qty
                else:
                    print("Кількість має бути додатна")
            except ValueError:
                print("Введи ціле число")

        elif choice == "4":
            if save_state("save.json", game_state):
                print("Збережено")
            else:
                print("Помилка збереження")

        elif choice == "5":
            ans = input("Зберегти перед виходом? (так/ні): ").lower()
            if ans == "так":
                save_state("save.json", game_state)
            print("До побачення!")
            break

        else:
            print("Невірний вибір")


if __name__ == "__main__":
    main()
