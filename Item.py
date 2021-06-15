class Item:
    def __init__(self,  id, value, weight, strong_correlation: bool = False, R: int = 10000):
        self.id = id
        self.weight = weight
        if strong_correlation:
            self.value = weight + R / 10
        else:
            self.value = value

    def __repr__(self):
        return f'Item {self.id}'

    def __str__(self):
        return f'Item {self.id}'

    def __hash__(self):
        return hash((self.id, self.value, self.weight))

    def __eq__(self, other):
        return self.id == other.id and self.value == other.value and self.weight == other.weight

    def __ne__(self, other):
        return self.id != other.id or self.value != other.value or self.weight != other.weight

    def __le__(self, other):
        return self.value / self.weight <= other.value / other.weight

    def __lt__(self, other):
        return self.value / self.weight < other.value / other.weight

    def __ge__(self, other):
        return self.value / self.weight >= other.value / other.weight

    def __gt__(self, other):
        return self.value / self.weight > other.value / other.weight