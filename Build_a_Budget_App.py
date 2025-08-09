class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        total = 0
        for item in self.ledger:
            total += item["amount"]
        return total

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = ""
        for item in self.ledger:
            desc = item["description"][:23].ljust(23)
            amt = f"{item['amount']:.2f}".rjust(7)
            items += f"{desc}{amt}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total


def create_spend_chart(categories):
    res = "Percentage spent by category\n"

    # Υπολογισμός των συνολικών εξόδων ανά κατηγορία
    spends = []
    total_spent = 0
    for cat in categories:
        spent = 0
        for item in cat.ledger:
            if item["amount"] < 0:
                spent += -item["amount"]
        spends.append(spent)
        total_spent += spent

    # Υπολογισμός ποσοστού (στρογγυλοποίηση στο πλησιέστερο 10 προς τα κάτω)
    percentages = [(int((sp / total_spent) * 10) * 10) for sp in spends]

    # Σχεδίαση του chart
    for i in range(100, -1, -10):
        line = str(i).rjust(3) + "|"
        for p in percentages:
            line += " o " if p >= i else "   "
        line += " "
        res += line + "\n"

    # Οριζόντια γραμμή
    res += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    # Ονόματα κατηγοριών (κάθετα)
    max_len = max(len(cat.name) for cat in categories)
    for i in range(max_len):
        line = "     "
        for cat in categories:
            line += (cat.name[i] if i < len(cat.name) else " ") + "  "
        res += line.rstrip() + "\n"

    return res.rstrip("\n")  # Χωρίς newline στο τέλος
