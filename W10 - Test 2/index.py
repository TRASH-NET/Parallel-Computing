import multiprocessing
import random
import os
import time

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
                elif action == 'withdraw' and self.balance.value >= amount:
                    self.balance.value -= amount


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

    def distribute_transactions(self, num_transactions, num_processes):
        """
        Distribute the transactions among multiple processes.
        
        :param num_transactions: Number of transactions to perform.
        :param num_processes: Number of processes to use.
        
        :return: List with the number of transactions per process.
        """
        if num_transactions <= num_processes:
            return [1] * num_transactions
        else:
            transactions_per_process = [num_transactions // num_processes] * num_processes
            remaining = num_transactions % num_processes

            for i in range(remaining):
                transactions_per_process[i] += 1

            return transactions_per_process

    def execute_transactions(self, num_transactions, num_processes):
        """
        Execute the transactions using multiple processes.
        
        :param num_transactions: Number of transactions to perform.
        :param num_processes: Number of processes to use.
        """
        transactions_per_process = self.distribute_transactions(num_transactions, num_processes)
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
        transaction_counts = [10_000, 100_000, 1_000_000]
        num_cpus = os.cpu_count()
        max_processes_options = [num_cpus * i for i in range(1, 4)]

        for num_transactions in transaction_counts:
            for max_processes in max_processes_options:
                print(f'\n\n--------------- Testing with {num_transactions} transactions using {max_processes} processes ---------------\n\n')

                account = BankAccount(initial_balance=10.0)
                transaction_manager = TransactionManager(account)

                start_time = time.time()
                transaction_manager.execute_transactions(num_transactions, max_processes)
                end_time = time.time()

                print(f'Final account balance: ${account.balance.value:.2f}')
                print(f'Execution time for {num_transactions} transactions with {max_processes} processes: {end_time - start_time:.2f} seconds.\n')

if __name__ == "__main__":
    BankAccountTest.run_tests()
