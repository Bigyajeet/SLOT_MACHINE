import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_counts = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_values = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

def deposit():
    while True:
        amount = input("Enter the deposit amount: $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than zero.")
        else:
            print("Please enter a valid number.")
    return amount

def get_number_of_lines():
    while True:
        lines = input(f"Enter the number of lines to bet on (1-{MAX_LINES}): ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a valid number.")
    return lines

def get_bet():
    while True:
        amount = input(f"Enter your bet per line (${MIN_BET}-${MAX_BET}): $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${MIN_BET} and ${MAX_BET}.")
        else:
            print("Please enter a valid number.")
    return amount

def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines
        if total_bet > balance:
            print(f"You do not have enough to bet that amount. Your current balance is: ${balance}")
        else:
            break
    print(f"You are betting ${bet} on {lines} lines. Total bet is: ${total_bet}")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_counts)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_values)
    print(f"You won ${winnings}.")
    print(f"You won on lines:", *winning_lines)
    return winnings - total_bet

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, count in symbols.items():
        all_symbols.extend([symbol] * count)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]  # Create a copy to avoid modifying the original
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns

def print_slot_machine(columns):
    print("\n")
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")
        print()
    print("\n")

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    rows = len(columns[0])
    symbols_per_line = []
    for row in range(rows):
        line_symbols = []
        for column in columns:
            line_symbols.append(column[row])
        symbols_per_line.append(line_symbols)

    for line in range(lines):
        symbols = symbols_per_line[line]
        if all(symbol == symbols[0] for symbol in symbols):
            winnings += bet * values[symbols[0]]
            winning_lines.append(line + 1)
    return winnings, winning_lines

def game(initial_balance=None):
    if initial_balance is None:
        balance = deposit()
    else:
        balance = initial_balance
        print(f"Your current balance is: ${balance}")

    while True:
        print(f"Current balance: ${balance}")
        play = input("Press enter to spin (q to quit): ")
        if play.lower() == "q":
            break
        balance += spin(balance)

    print(f"You left with a balance of: ${balance}")
    return balance

def save_game(balance, filename="slot_machine_save.txt"):
    try:
        with open(filename, "w") as f:
            f.write(str(balance))
        print("Game saved successfully!")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game(filename="slot_machine_save.txt"):
    try:
        with open(filename, "r") as f:
            balance = int(f.readline())
        print("Game loaded successfully!")
        return balance
    except FileNotFoundError:
        print("No saved game found. Starting a new game.")
        return None
    except Exception as e:
        print(f"Error loading game: {e}")
        return None

def main():
    print("Welcome to the Python Slot Machine! 🎰")

    load_option = input("Load saved game? (y/n): ").lower()
    if load_option == "y":
        initial_balance = load_game()
        final_balance = game(initial_balance)
    else:
        final_balance = game()

    save_option = input("Save game before quitting? (y/n): ").lower()
    if save_option == "y":
        save_game(final_balance)
    print("Thanks for playing!")

if __name__ == "__main__":
    main()