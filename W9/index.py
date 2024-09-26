import multiprocessing
import random
import os
import sys
import time

RESET = '\033[0m'
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'


class BankAccount:
    """
    Represent a bank account with fund and withdraw operations.
    Use shared memory for the balance and a lock for synchronization.
    """

    def __init__(self, initial_balance=0.0):
        """
        Construct a BankAccount object with an initial balance.
        
        :param initial_balance: Initial balance of the account. Default is 0.0.
        """
        self.balance = multiprocessing.Value('d', initial_balance)
        self.lock = multiprocessing.Lock()

    def perform_transaction(self, num_transactions, process_id):
        """
        Make a number of transactions in the account.
        
        :param num_transactions: Number of transactions to perform.
        :param process_id: Identifier of the process.

        """
        for _ in range(num_transactions):
            amount = random.uniform(1, 100)
            action = random.choice(['fund', 'withdraw'])

            with self.lock:
                if action == 'fund':
                    self.balance.value += amount
                    print(f'{GREEN}Process {process_id}: Fund: ${amount:.2f}, Balance: ${self.balance.value:.2f}{RESET}\n')
                elif action == 'withdraw' and self.balance.value >= amount:
                    self.balance.value -= amount
                    print(f'{RED}Process {process_id}: Withdraw: ${amount:.2f}, Balance: ${self.balance.value:.2f}\n{RESET}')
                else:
                    print(f'{YELLOW}Process {process_id}: Failed Withdraw: ${amount:.2f} Insufficient Balance for this transaction.,  Balance: ${self.balance.value:.2f}\n{RESET}')


class TransactionManager:
    """
    Manage the transactions for a BankAccount using multiple processes.
    """

    def __init__(self, account):
        """
        Constructor of the TransactionManager class.
        
        :param account: Represent the account to perform the transactions, it is an instance of BankAccount class.
        """
        self.account = account
        self.max_num_processes = os.cpu_count()

    def distribute_transactions(self, num_transactions):
        """
        Distribute the transactions among multiple processes.
        
        :param num_transactions: Number of transactions to perform.
        
        :return: List with the number of transactions per process.
        """
        if num_transactions <= self.max_num_processes:
            return [1] * num_transactions
        else:
            transactions_per_process = [num_transactions // self.max_num_processes] * self.max_num_processes
            remaining = num_transactions % self.max_num_processes

            for i in range(remaining):
                transactions_per_process[i] += 1

            return transactions_per_process

    def execute_transactions(self, num_transactions):
        """
        Execture the transactions using multiple processes.
        
        :param num_transactions: Number of transactions to perform.

        """
        transactions_per_process = self.distribute_transactions(num_transactions)
        processes = []

        for i, num in enumerate(transactions_per_process, 1):
            process = multiprocessing.Process(target=self.account.perform_transaction, args=(num, i))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()


class BankAccountTest:
    """
    Test class for BankAccount and TransactionManager classes.
    """

    @staticmethod
    def run_tests():
        """
        Execute test for BankAccount and TransactionManager classes.
        """
        print("Iniciando pruebas...")

        account = BankAccount(initial_balance=10.0)
        transaction_manager = TransactionManager(account)

        print(f'\n\n--------------- Saldo inicial: ${account.balance.value:.2f} ---------------\n\n')
        
        while True:
            try:
                num_transactions = int(input('Ingrese el número de transacciones a realizar: '))
                if num_transactions > 0 and num_transactions < sys.maxsize:
                    break
                else:
                    print(f'\nPor favor, ingrese un número mayor que 0 y menor que {sys.maxsize}.')
            except ValueError:
                print('\nEntrada no válida. Debe ser un número entero.')
        start_time = time.time()
        transaction_manager.execute_transactions(num_transactions)
        end_time = time.time()

        print(f'\nFinal account balance: ${account.balance.value:.2f}')

        print(f'\nExecution time: {end_time - start_time:.2f} segundos.')

if __name__ == "__main__":
    
    BankAccountTest.run_tests()
