import threading
import random
import time
from typing import List, Tuple
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(message)s'
)

class BankSystem:
    def __init__(self, initial_balances: List[int]):
        self.accounts = initial_balances
        self.locks = [threading.Lock() for _ in range(len(initial_balances))]
        self.total_initial_amount = sum(initial_balances)
        self.transfer_complete = threading.Event()
        self.transfer_count = 0
        self.transfer_lock = threading.Lock()

    def get_account_locks(self, acc1: int, acc2: int) -> Tuple[threading.Lock, threading.Lock]:
        """Return locks in a consistent order to prevent deadlocks."""
        if acc1 < acc2:
            return self.locks[acc1], self.locks[acc2]
        return self.locks[acc2], self.locks[acc1]

    def transfer_money(self, from_acc: int, to_acc: int, amount: int) -> bool:
        """Transfer money between accounts using ordered resource acquisition."""
        if from_acc == to_acc:
            return False

        lock1, lock2 = self.get_account_locks(from_acc, to_acc)
        
        try:
            # Attempt to acquire both locks with timeout to prevent deadlocks
            if not lock1.acquire(timeout=1):
                logging.warning(f"Timeout acquiring first lock for accounts {from_acc}->{to_acc}")
                return False
                
            if not lock2.acquire(timeout=1):
                logging.warning(f"Timeout acquiring second lock for accounts {from_acc}->{to_acc}")
                lock1.release()
                return False

            # Check if transfer is possible
            if self.accounts[from_acc] >= amount:
                self.accounts[from_acc] -= amount
                self.accounts[to_acc] += amount
                logging.info(f"Transferred ${amount} from Account {from_acc} to Account {to_acc}")
                return True
            else:
                logging.warning(f"Insufficient funds in Account {from_acc}")
                return False

        finally:
            # Release locks in reverse order
            if lock2.locked():
                lock2.release()
            if lock1.locked():
                lock1.release()

    def random_transfer(self):
        """Perform random transfers between accounts."""
        while not self.transfer_complete.is_set():
            from_acc = random.randint(0, len(self.accounts) - 1)
            to_acc = random.randint(0, len(self.accounts) - 1)
            amount = random.randint(1, 100)

            if self.transfer_money(from_acc, to_acc, amount):
                with self.transfer_lock:
                    self.transfer_count += 1

    def print_status(self):
        """Print current account balances and verify system consistency."""
        print("\nFinal Account Balances:")
        for i, balance in enumerate(self.accounts):
            print(f"Account {i}: ${balance}")
        
        current_total = sum(self.accounts)
        print(f"\nInitial Total: ${self.total_initial_amount}")
        print(f"Final Total: ${current_total}")
        print(f"Total Transfers Completed: {self.transfer_count}")
        
        if current_total == self.total_initial_amount:
            print("\nSystem Consistency: VERIFIED ✓")
        else:
            print("\nSystem Consistency: ERROR - Totals don't match!")