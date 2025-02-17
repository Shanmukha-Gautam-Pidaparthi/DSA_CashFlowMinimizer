import datetime

class Bank:
    def _init_(self, name):
        self.name = name
        self.net_amount = 0
        self.types = set()
        

class MinHeap:
    def _init_(self):
        self.heap = []

    def push(self, item):
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def peek(self):
        return self.heap[0] if self.heap else None

    def _heapify_up(self, index):
        parent = (index - 1) // 2
        while index > 0 and self.heap[index][0] < self.heap[parent][0]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            parent = (index - 1) // 2

    def _heapify_down(self, index):
        size = len(self.heap)
        smallest = index
        left, right = 2 * index + 1, 2 * index + 2

        if left < size and self.heap[left][0] < self.heap[smallest][0]:
            smallest = left
        if right < size and self.heap[right][0] < self.heap[smallest][0]:
            smallest = right

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

class CashFlowMinimizer:
    def _init_(self):
        self.banks = {}
        self.adj_list = {}
        self.transaction_history = []

    def add_bank(self, name, types):
        if name in self.banks:
            print(f"Bank {name} already exists.")
            return
        bank = Bank(name)
        bank.types = types
        self.banks[name] = bank
        self.adj_list[name] = []
        print(f"Bank {name} added successfully.")

    def get_most_active_bank(self):
        transaction_count = {name: 0 for name in self.banks}
        for debtor, creditor, amount, timestamp in self.transaction_history:    
            transaction_count[debtor] += 1
            transaction_count[creditor] += 1
        if not transaction_count:
            print("No transactions recorded.")
            return None
        max_transactions = max(transaction_count.values())
        most_active_banks = [bank for bank, count in transaction_count.items() if count == max_transactions]
        if max_transactions == 0:
            print("No transactions recorded.")
            return None
        print(f"Most Active Banks: {', '.join(most_active_banks)} with {max_transactions} transactions.")

    def view_bank_details(self):
        print("\nBank Details:")
        for name, bank in self.banks.items():
            print(f"Bank: {name}, Balance: {bank.net_amount}, Types: {', '.join(bank.types)}")

    def view_transaction_history(self):
        print("\nTransaction History:")
        if not self.transaction_history:
            print("No transactions available.")
            return
        for debtor, creditor, amount, timestamp in self.transaction_history:
            print(f"{debtor} -> {creditor} : {amount} on {timestamp}")

    def get_bank_balance(self, bank_name):
        if bank_name not in self.banks:
            print(f"Bank {bank_name} does not exist.")
            return None
        net_amount = self.banks[bank_name].net_amount
        print(f"Balance for {bank_name}: {net_amount}")

    def add_transaction(self, debtor, creditor, amount):
        if debtor not in self.banks or creditor not in self.banks:
            print("Both debtor and creditor banks must be in the system.")
            return

        elif "credit" not in self.banks[debtor].types:
            print(f"Bank {debtor} is a credit bank and cannot act as a debtor.")
            return
        elif "debit" not in self.banks[debtor].types:
            print(f"Bank {creditor} is a debit bank and cannot act as a creditor.")
            return

        self.banks[debtor].net_amount -= amount
        self.banks[creditor].net_amount += amount
        self.adj_list[debtor].append((creditor, amount))
        timestamp = datetime.datetime.now()
        self.transaction_history.append((debtor, creditor, amount, timestamp))
        print(f"Transaction added: {debtor} -> {creditor} : {amount} at {timestamp}")


    def generate_monthly_summary(self, month, year):
        if month < 1 or month > 12:
            print("Invalid month. Please enter a month between 1 and 12.")
            return
        if year < 0:
            print("Invalid year. Please enter a valid year.")
            return
        print(f"\nMonthly Summary for {month}/{year}:")
        for name, bank in self.banks.items():
            total_incoming = sum(amount for debtor, creditor, amount, timestamp in self.transaction_history if creditor == name and timestamp.month == month and timestamp.year == year)
            total_outgoing = sum(amount for debtor, creditor, amount, timestamp in self.transaction_history if debtor == name and timestamp.month == month and timestamp.year == year)
            if total_incoming == 0 and total_outgoing == 0:
                print(f"Bank: {name}, No transactions found.")
            else:
                print(f"Bank: {name}, Incoming: {total_incoming}, Outgoing: {total_outgoing}")

    def generate_bank_statement(self, bank_name, start_date=None, end_date=None):
        if bank_name not in self.banks:
            print(f"Bank {bank_name} does not exist.")
            return
        print(f"\nBank Statement for {bank_name}:")
        transactions = [t for t in self.transaction_history if t[0] == bank_name or t[1] == bank_name]
        if start_date:
            transactions = [t for t in transactions if t[3] >= start_date]
        if end_date:
            transactions = [t for t in transactions if t[3] <= end_date]
        total_incoming = sum(amount for debtor, creditor, amount, timestamp in transactions if creditor == bank_name)
        total_outgoing = sum(amount for debtor, creditor, amount, timestamp in transactions if debtor == bank_name)
        print(f"Total Incoming: {total_incoming}, Total Outgoing: {total_outgoing}")
        for debtor, creditor, amount, timestamp in transactions:
            print(f"{debtor} -> {creditor} : {amount} on {timestamp}")
            
    def predict_cash_flow(self, bank_name, days=30):
        transactions = [t for t in self.transaction_history if t[0] == bank_name or t[1] == bank_name]
        if not transactions:
            print(f"No transaction data available for bank {bank_name}.")
            return
        incoming_transactions = [t for t in transactions if t[1] == bank_name]
        outgoing_transactions = [t for t in transactions if t[0] == bank_name]

        avg_incoming = sum(t[2] for t in incoming_transactions) / len(incoming_transactions) if incoming_transactions else 0
        avg_outgoing = sum(t[2] for t in outgoing_transactions) / len(outgoing_transactions) if outgoing_transactions else 0

        time_range_days = (max(t[3] for t in transactions) - min(t[3] for t in transactions)).days + 1
        avg_incoming_frequency = len(incoming_transactions) / time_range_days if incoming_transactions else 0
        avg_outgoing_frequency = len(outgoing_transactions) / time_range_days if outgoing_transactions else 0

        predicted_incoming = avg_incoming * avg_incoming_frequency * days
        predicted_outgoing = avg_outgoing * avg_outgoing_frequency * days
        net_predicted_flow = predicted_incoming - predicted_outgoing


        print(f"Predicted incoming cash flow for {bank_name} over the next {days} days: {predicted_incoming:.2f}")
        print(f"Predicted outgoing cash flow for {bank_name} over the next {days} days: {predicted_outgoing:.2f}")
        print(f"Net predicted cash flow for {bank_name} over the next {days} days: {net_predicted_flow:.2f}")


    def minimize_cash_flow(self):
        debtor_heap = MinHeap()
        creditor_heap = MinHeap()

        for bank_name, bank in self.banks.items():
            if bank.net_amount < 0:
                debtor_heap.push((abs(bank.net_amount), bank_name))
            elif bank.net_amount > 0:
                creditor_heap.push((bank.net_amount, bank_name))

        ans_graph = {debtor: {} for debtor in self.banks}

        while debtor_heap.heap and creditor_heap.heap:
            debtor_amount, debtor_name = debtor_heap.pop()
            creditor_amount, creditor_name = creditor_heap.pop()

            transaction_amount = min(debtor_amount, creditor_amount)
            ans_graph[debtor_name][creditor_name] = transaction_amount

            self.banks[debtor_name].net_amount += transaction_amount
            self.banks[creditor_name].net_amount -= transaction_amount

            if self.banks[debtor_name].net_amount < 0:
                debtor_heap.push((abs(self.banks[debtor_name].net_amount), debtor_name))
            if self.banks[creditor_name].net_amount > 0:
                creditor_heap.push((self.banks[creditor_name].net_amount, creditor_name))

        self._print_ans(ans_graph)
        print("Minimizing cash flow...")

    def _find_matching_creditor(self, debtor):
        debtor_types = self.banks[debtor].types
        for bank_name, bank in self.banks.items():
            if bank_name != debtor and bank.net_amount > 0 and not debtor_types.isdisjoint(bank.types):
                return bank_name
        return None

    def _update_net_amount(self, debtor, creditor, amount):
        self.banks[debtor].net_amount -= amount
        self.banks[creditor].net_amount += amount
    
    def _print_ans(self, ans_graph):
        print("\nMinimum transactions:")
        for debtor, creditors in ans_graph.items():
            for creditor, amount in creditors.items():
                print(f"{debtor} pays {amount} to {creditor}")

    def get_top_debtor_creditor(self):
        top_debtor = min(self.banks.items(), key=lambda x: x[1].net_amount)
        top_creditor = max(self.banks.items(), key=lambda x: x[1].net_amount)
        print(f"Top Debtor: {top_debtor[0]} with balance {top_debtor[1].net_amount}")
        print(f"Top Creditor: {top_creditor[0]} with balance {top_creditor[1].net_amount}")

    def clear_specific_transaction(self, index):
        if index < 0 or index >= len(self.transaction_history):
            print("Invalid transaction index.")
            return
        debtor, creditor, amount, _ = self.transaction_history.pop(index)
        self.banks[debtor].net_amount += amount
        self.banks[creditor].net_amount -= amount
        self.adj_list[debtor] = [(c, a) for c, a in self.adj_list[debtor] if c != creditor or a != amount]
        print(f"Transaction at index {index} cleared.")

    def calculate_interest(self, debtor, creditor, rate, days):
        if debtor not in self.banks or creditor not in self.banks:
            print("Both debtor and creditor banks must be in the system.")
            return
        outstanding_debt = sum(amount for c, amount in self.adj_list[debtor] if c == creditor)
        interest = outstanding_debt * (rate / 100) * (days / 365)
        print(f"Interest on debt from {debtor} to {creditor} over {days} days at {rate}% rate: {interest:.2f}")

    def filter_transaction_by_date_and_amount(self, start_date=None, end_date=None, min_amount=None, max_amount=None):
        filtered_transactions = self.transaction_history
        if start_date:
            filtered_transactions = [t for t in filtered_transactions if t[3] >= start_date]
        if end_date:
            filtered_transactions = [t for t in filtered_transactions if t[3] <= end_date]
        if min_amount:
            filtered_transactions = [t for t in filtered_transactions if t[2] >= min_amount]
        if max_amount:
            filtered_transactions = [t for t in filtered_transactions if t[2] <= max_amount]

        print("\nFiltered Transaction History by Date and Amount:")
        for debtor, creditor, amount, timestamp in filtered_transactions:
            print(f"{debtor} -> {creditor} : {amount} on {timestamp}")

    def filter_transaction_by_name(self, criteria):
        print(f"\nFiltering Transaction History by '{criteria}':")
        for debtor, creditor, amount, timestamp in self.transaction_history:
            if criteria in debtor or criteria in creditor:
                print(f"{debtor} -> {creditor} : {amount} on {timestamp}")

    def generate_transaction_report(self):
        print("\nTransaction Report:")
        for bank_name in self.banks:
            transactions = [t for t in self.transaction_history if t[0] == bank_name or t[1] == bank_name]
            total_transactions = len(transactions)
            total_amount = sum(t[2] for t in transactions)
            avg_amount = total_amount / total_transactions if total_transactions > 0 else 0
            print(f"Bank: {bank_name}, Total Transactions: {len(transactions)}, Total Amount: {total_amount}, Average Amount: {avg_amount:.2f}")


def main():
    cash_flow = CashFlowMinimizer()

    while True:
        print("\nOptions:")
        print("1. Add Bank")
        print("2. Add Transaction")
        print("3. Predict Cash Flow")
        print("4. Get Bank Balance")
        print("5. View Bank Details")
        print("6. View Transaction History")
        print("7. Minimize Cash Flow")
        print("8. Get Top Debtor and Creditor")
        print("9. Clear Specific Transaction")
        print("10. Calculate Interest")
        print("11. Filter Transaction History by date and amount")
        print("12. Filter Transaction History by name")
        print("13. Generate Transaction Report")
        print("14. Get Most Active Bank")
        print("15. Generate Monthly Transaction Summary")
        print("16. Generate Bank Statement")
        print("17. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter bank name: ")
            types = set(input(f"Enter payment types for {name} (comma-separated): ").split(","))
            cash_flow.add_bank(name, types)
        elif choice == "2":
            debtor = input("Enter debtor bank: ")
            creditor = input("Enter creditor bank: ")
            amount = int(input("Enter transaction amount: "))
            cash_flow.add_transaction(debtor, creditor, amount)
        elif choice == "3":
            bank_name = input("Enter bank name for prediction: ")
            days = int(input("Enter number of days for prediction: "))
            cash_flow.predict_cash_flow(bank_name, days)
        elif choice == "4":
            bank_name = input("Enter bank name to check balance: ")
            cash_flow.get_bank_balance(bank_name)
        elif choice == "5":
            cash_flow.view_bank_details()
        elif choice == "6":
            cash_flow.view_transaction_history()
        elif choice == "7":
            cash_flow.minimize_cash_flow()
        elif choice == "8":
            cash_flow.get_top_debtor_creditor()
        elif choice == "9":
            index = int(input("Enter transaction index to clear: "))
            cash_flow.clear_specific_transaction(index)
        elif choice == "10":
            debtor = input("Enter debtor bank: ")
            creditor = input("Enter creditor bank: ")
            rate = float(input("Enter interest rate (%): "))
            days = int(input("Enter number of days for interest calculation: "))
            cash_flow.calculate_interest(debtor, creditor, rate, days)
        elif choice == "11":
            start_date = input("Enter start date (YYYY-MM-DD) or leave blank: ")
            end_date = input("Enter end date (YYYY-MM-DD) or leave blank: ")
            min_amount = input("Enter minimum transaction amount or leave blank: ")
            max_amount = input("Enter maximum transaction amount or leave blank: ")
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
            min_amount = int(min_amount) if min_amount else None
            max_amount = int(max_amount) if max_amount else None
            cash_flow.filter_transaction_by_date_and_amount(start_date, end_date, min_amount, max_amount)
        elif choice == "12":
            criteria = input("Enter criteria to filter transactions: ")
            cash_flow.filter_transaction_by_name(criteria)
        elif choice == "13":
            cash_flow.generate_transaction_report()
        elif choice == "14":
            cash_flow.get_most_active_bank()
        elif choice == "15":
            month = int(input("Enter month: "))
            year = int(input("Enter year: "))
            cash_flow.generate_monthly_summary(month, year)
        elif choice == "16":
            bank_name = input("Enter bank name: ")
            start_date_str = input("Enter start date (YYYY-MM-DD) or leave empty: ")
            end_date_str = input("Enter end date (YYYY-MM-DD) or leave empty: ")
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None
            cash_flow.generate_bank_statement(bank_name, start_date, end_date)
        elif choice == "17":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if _name_ == "_main_":
    main()