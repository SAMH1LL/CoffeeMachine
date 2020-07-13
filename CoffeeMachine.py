class CoffeeMachine:
    def __init__(self):
        self.ml_water = 400
        self.ml_milk = 540
        self.g_beans = 120
        self.disposable_cups = 9
        self.money = 550

    def remaining(self):
        print("The coffee machine has")
        print(self.ml_water, "of water")
        print(self.ml_milk, "of milk")
        print(self.g_beans, "of coffee beans")
        print(self.disposable_cups, "of disposable cups")
        print(self.money, "of money")
        print()

    def buy(self):
        what_to_buy = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu: ")
        if what_to_buy == "1":
            self.buy_drink(250, 0, 16, 4)
        elif what_to_buy == "2":
            self.buy_drink(350, 75, 20, 7)
        elif what_to_buy == "3":
            self.buy_drink(200, 100, 12, 6)
        elif what_to_buy == "back":
            pass

    def buy_drink(self, water_required, milk_required, beans_required, cost):
        if self.ml_water >= water_required and self.ml_milk >= milk_required and self.g_beans >= beans_required and self.disposable_cups > 0:
            self.ml_water = self.ml_water - water_required
            self.ml_milk = self.ml_milk - milk_required
            self.g_beans = self.g_beans - beans_required
            self.disposable_cups = self.disposable_cups - 1
            self.money += cost
        else:
            print("Sorry, can't make anything")

    def fill(self):
        self.ml_water += (int(input("Write how many ml of water do you want to add: ")))
        self.ml_milk += (int(input("Write how many ml of milk do you want to add: ")))
        self.g_beans += (int(input("Write how many grams of coffee beans do you want to add: ")))
        self.disposable_cups += (int(input("Write how many disposable cups of coffee do you want to add: ")))

    def take(self):
        print("I gave you $", self.money)
        self.money = 0

    def run(self):
        while True:
            action_to_take = input("Write action (buy, fill, take, remaining, exit): ")
            if action_to_take == "buy":
                self.buy()
            elif action_to_take == "fill":
                self.fill()
            elif action_to_take == "take":
                self.take()
            elif action_to_take == "remaining":
                self.remaining()
            elif action_to_take == "exit":
                break


coffee_machine = CoffeeMachine()
coffee_machine.run()
