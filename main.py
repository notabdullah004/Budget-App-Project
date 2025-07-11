class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        return False

    def get_balance(self):
        total = 0
        for item in self.ledger:
            total += item['amount']
        return total

    def transfer(self, amount, other_category):
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {other_category.name}')
            other_category.deposit(amount, f'Transfer from {self.name}')
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = ''
        for entry in self.ledger:
            desc = entry['description'][:23]
            amt = f"{entry['amount']:.2f}"
            # amount right-aligned, max 7 chars, description left-aligned max 23 chars
            items += f"{desc:<23}{amt:>7}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total


def create_spend_chart(categories):
    # Calculate spent amounts (withdrawals only)
    spent = []
    for cat in categories:
        total_spent = 0
        for item in cat.ledger:
            if item['amount'] < 0:
                total_spent += -item['amount']
        spent.append(total_spent)

    total_spent_all = sum(spent)
    percentages = [int((s / total_spent_all) * 10) * 10 for s in spent]  # rounded down to nearest 10

    chart = "Percentage spent by category\n"

    # y-axis labels from 100 to 0 step -10
    for y in range(100, -1, -10):
        chart += f"{y:>3}|"
        for p in percentages:
            chart += " o " if p >= y else "   "
        chart += " \n"

    # bottom line, 3 chars per category + 1 for initial space, then 1 extra space after last bar
    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    # category names vertically
    max_len = max(len(cat.name) for cat in categories)
    for i in range(max_len):
        line = "     "  # 5 spaces padding for left margin
        for cat in categories:
            if i < len(cat.name):
                line += cat.name[i] + "  "
            else:
                line += "   "
        if i < max_len - 1:
            line += "\n"
        chart += line

    return chart
