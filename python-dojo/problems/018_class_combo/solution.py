class Cat:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def describe(self):
        return f"{self.name}は{self.age}歳です"


cats = [Cat("たま", 3), Cat("ミケ", 5), Cat("クロ", 1)]
ages = [cat.age for cat in cats]
average_age = sum(ages) / len(ages)
print(average_age)
