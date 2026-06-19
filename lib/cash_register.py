#!/usr/bin/env python3

class CashRegister:
    '''A simple cash register that tracks a running total, the items rung up,
    a record of every transaction, and an optional percentage discount.'''

    def __init__(self, discount=0):
        # `discount` is an optional percentage (e.g. 20 => 20% off). It runs
        # through the property setter below so it is validated on creation.
        self.discount = discount
        # Running total of everything rung up so far.
        self.total = 0
        # Flat list of every item title that has been added (one entry per unit).
        self.items = []
        # A record of each add_item call so transactions can be voided later.
        self.previous_transactions = []

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, value):
        # A discount must be a whole number between 0 and 100 (inclusive).
        if isinstance(value, int) and 0 <= value <= 100:
            self._discount = value
        else:
            print("Not valid discount")

    def add_item(self, item, price, quantity=1):
        '''Add `quantity` of `item` at `price` each to the register.'''
        # Increase the total by the cost of every unit added.
        self.total += price * quantity
        # Record one entry in the items list for each unit purchased.
        self.items.extend([item] * quantity)
        # Keep a record of the transaction so it can be voided if needed.
        self.previous_transactions.append({
            "item": item,
            "price": price,
            "quantity": quantity,
        })

    def apply_discount(self):
        '''Reduce the total by the register's discount percentage.'''
        if self.discount:
            # Subtract the discount percentage from the current total.
            self.total -= self.total * self.discount / 100
            # Display whole-dollar totals without a trailing ".0".
            display = int(self.total) if self.total == int(self.total) else self.total
            print(f"After the discount, the total comes to ${display}.")
        else:
            print("There is no discount to apply.")

    def void_last_transaction(self):
        '''Undo the most recent transaction, restoring the total and items.'''
        if not self.previous_transactions:
            print("There is no transaction to void.")
            return

        # Remove the most recent transaction from the history.
        last_transaction = self.previous_transactions.pop()
        # Subtract that transaction's cost from the running total.
        self.total -= last_transaction["price"] * last_transaction["quantity"]
        # Remove the corresponding item entries from the items list.
        for _ in range(last_transaction["quantity"]):
            if last_transaction["item"] in self.items:
                self.items.remove(last_transaction["item"])
