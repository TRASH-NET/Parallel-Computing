from bank_system import BankSystem
import threading
import time

def get_valid_input(prompt: str, min_val: int, max_val: int) -> int:
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            print(f"Please enter a value between {min_val} and {max_val}")
        except ValueError:
            print("Please enter a valid number")

def main():
    # Get user input with constraints
    n_accounts = get_valid_input("Enter number of accounts (2-10): ", 2, 10)
    n_threads = get_valid_input("Enter number of transfer threads (2-20): ", 2, 20)
    
    # Initialize accounts with random balances between 100 and 1000
    initial_balances = [500 for _ in range(n_accounts)]  # Start with equal balances for simplicity
    
    # Create bank system
    bank = BankSystem(initial_balances)
    
    print("\nInitial Account Balances:")
    for i, balance in enumerate(initial_balances):
        print(f"Account {i}: ${balance}")
    
    # Create and start transfer threads
    threads = []
    for i in range(n_threads):
        thread = threading.Thread(
            target=bank.random_transfer,
            name=f"TransferThread-{i}"
        )
        thread.daemon = True
        threads.append(thread)
        thread.start()
    
    # Let the system run for a few seconds
    time.sleep(5)
    
    # Signal threads to complete
    bank.transfer_complete.set()
    
    # Wait for all threads to finish
    for thread in threads:
        thread.join(timeout=1)
    
    # Print final status
    bank.print_status()

if __name__ == "__main__":
    main()