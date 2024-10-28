# Challenge: Bank Account Transfers with Deadlock Prevention

# Problem Statement

You are tasked with simulating a bank system where multiple accounts are involved in money transfers. Each account is represented by a thread, and each thread tries to transfer money to other accounts. Your goal is to ensure that all transfers occur without causing any deadlocks.

# Specifications

- Accounts and Balance:

    - There are N accounts, each with an initial balance.
    - Accounts are represented by an array of balances, e.g., accounts = [100, 200, 300, 400].

- Transfers:

    - Multiple threads are created, each representing a transfer between two accounts.

    - Each thread randomly selects two different accounts and attempts to transfer a random amount of money from one account to another.

    - Ensure that the transfer is only possible if the source account has sufficient funds.


- Deadlock Avoidance:

    - Implement a locking mechanism to avoid deadlocks during transfers.

    - Use Python’s threading.Lock for synchronizing access to accounts.

    - Consider using a strategy like resource ordering or a timeout to prevent deadlocks.


- Output:

    - After all transfers are complete, print the final balance of all accounts.

    - Ensure that the total amount of money remains consistent before and after the transfers.


- Edge Cases:

    - Handle cases where multiple threads are trying to access the same accounts simultaneously.

    - Ensure that no deadlocks occur, even under high contention.


- Constraints (asked to the user by CLI):

    - Number of accounts, N: 2 ≤ N ≤ 10

    - Number of transfer threads, T: 2 ≤ T ≤ 20

    - Transfer amount: 1 ≤ Amount ≤ 100


# Objective:

- Write a Python program to implement the above system.

- Demonstrate how your solution prevents deadlocks.

- Discuss the strategy you used to avoid deadlocks in the accompanying documentation.


# Evaluation Criteria:

- Correctness: The program should correctly simulate the bank transfers without causing any deadlocks.

- Deadlock Avoidance: The locking strategy should be clearly explained and effectively implemented.

- Code Quality: The code should be well-structured, commented, and adhere to best practices.

- Testing: Include test cases that demonstrate the deadlock avoidance mechanism under various conditions.

# Grading Criteria:

- Design and implementation (30 points): Does the program meet the requirements? Is the design efficient and effective?

- Writing and presentation (20 points): Is the written report clear, concise, and well-organized? Are the graphs and charts effective in communicating the results?

- Experimentation and data analysis (30 points): Are the experiments well-designed and executed? Is the data analysis thorough and insightful?

- Optimization and recommendations (20 points): Are the optimization recommendations based on sound analysis and evidence? Are the recommendations practical and feasible?