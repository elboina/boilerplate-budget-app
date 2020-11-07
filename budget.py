class Category:
    
    def __init__(self, name: str = '') -> None:
        self.name = name
        self.ledger = []
    
    def deposit(self, amount, description = '') -> None:
        """
        adds an amount and its description to the ledger
        """
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description = '') -> bool:
        """
        withdraws the specified amount if the funds are sufficient
        """
        if self.check_funds(amount):
            self.ledger.append({"amount": - abs(amount), "description": description})
            return True
        return False

    def get_balance(self) -> float:
        return sum(line["amount"] for line in self.ledger)

    def transfer(self, amount: float, budget_category)-> bool:
        if self.check_funds(amount):
            self.withdraw(amount, 'Transfer to ' + budget_category.name.capitalize())
            budget_category.deposit(amount, 'Transfer from ' + self.name.capitalize())
            return True
        return False

    def check_funds(self, amount: float):
        return abs(amount) <= self.get_balance()

    def __str__(self) -> str:
        symbols = ((30 - len(self.name)) // 2) * '*'
        category_representation: str = symbols + self.name + symbols + '\n'
        for line in self.ledger:
            description: str = line["description"][:23]
            amount: str = f'{line["amount"]:.2f}'
            nb_spaces: int = 30 - (len(description) + len(amount))
            category_representation += description + nb_spaces * ' ' + amount + '\n'
        
        category_representation += 'Total: ' +  f'{self.get_balance():.2f}'

        return category_representation



def create_spend_chart(categories):
    spend_chart ="Percentage spent by category\n"
    for i in range(100, -10, -10):
        lead_char = ' ' if i != 100 else ''
        second_leading_space = ' ' if i == 0 else ''
        spend_chart+= lead_char + second_leading_space + str(i) + '|'
        total_spendings = sum(category.ledger[0]["amount"] - category.get_balance() for category in categories)
        for category in categories:
            nb_spaces = 1 if category is categories[0] else 2
            spend_chart+= nb_spaces * ' ' 
            spendings = category.ledger[0]["amount"] - category.get_balance()              
            spend_chart+= 'o' if(round(spendings/total_spendings, 2) * 100 >= i) else ' '
    
        spend_chart+= 2* ' ' + '\n'
    spend_chart+= 4* ' ' + (len(categories) * 3 + 1) * '-'
    legend_height = max(len(category.name) for category in categories)
    for j in range(legend_height):
        spend_chart+= '\n'
        for category in categories:
            nb_spaces = 5 if category is categories[0] else 2
            character = category.name[j] if len(category.name) > j else ' '
            spend_chart+= nb_spaces * ' ' + character       
        spend_chart += 2 * ' '
    return spend_chart
       