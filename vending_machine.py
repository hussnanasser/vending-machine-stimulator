import csv # For generating receipt CSV files
import math  
from datetime import datetime # For timestamping receipts


# Items with prices (in pence) and stock levels.
items = {
    "water":     {"price": 120, "stock": 10},
    "soda":      {"price": 150, "stock": 12},
    "chocolate": {"price": 250, "stock": 15},
    "crisps":    {"price": 140, "stock": 12},
    "sandwich":  {"price": 380, "stock": 8},
    "protein bar":   {"price": 300, "stock": 2}, 
    "protein shake": {"price": 450, "stock": 8}, 
    "flapjack": {"price": 240, "stock": 9}
}

#List of accepted coins in pence - will be converted later.
accepted_coins = [200, 100, 50, 20] # £2, £1, 50p, 20p 
order_num = 1 # First order number


# Conversion of pence to £ currency (£x.xx string)
def price_str(pence):
    """ Formats price in pence into UK currency string, 2 d.p. and £ (£x.xx). """
    return f"£{pence/100:.2f}"

#  Vending Machine Functions:
def insert_coins(starting_balance):
    """ Allows user to insert accepted coins only and returns the total balance. """
   
    balance = starting_balance
    print("\n------ Insert Money ------") # Header for coin insertion section


    while True:
    
        coin = input("Please insert coin(s) (£2, £1, 50p, 20p) or type 'Done' to finish: ").lower().strip() #Allowing user to type done in any font case when completed with inserting coins.

        if coin == "done": 
            break # Exititing loop of coin insertion 
        
        # The system accommodates various input formats for coins. For instance, £1 inputs may include 1, 1£, £1.00, 1.00, 100, or 100p."
        coin_values = {
        #  £2.00 (200p) 
         "£2.00": 200, 
         "2.00": 200, 
         "£2": 200, 
         "2£": 200, 
         "200p": 200, 
         "200": 200, 
         "2": 200, 

        # £1.00 (100p) 
        "£1.00": 100, 
        "1.00": 100, 
        "£1": 100, 
        "1£": 100, 
        "100p": 100, 
        "100": 100, 
        "1": 100,

        # 50p 
        "£0.50": 50, 
        "0.50": 50, 
        "50p": 50, 
        "50": 50, 
 
        #  20p 
        "£0.20": 20, 
        "0.20": 20, 
        "20p": 20, 
        "20": 20, }

        if coin in coin_values:
            balance += coin_values[coin]
            #  Current balance displayed after every coin insertion
            print(f"Current Balance: {price_str(balance)}")
        else:
            print("Invalid coin. Please try again!")

    return balance # Returns total balance after user has completed entering coins 


def show_menu():
    """ Prints current list of items, prices, and stock."""
    print("\n------ Main Menu -------") # Menu Header
    
    # Menu index (1, 2, 3...)
    for index, (name, data) in zip(range(1, len(items) + 1), items.items()):
        price = price_str(data['price'])
        stock = data['stock']
        # Format for the menu display.
        print(f"{index}. {name.capitalize():10} - {price:<5} ({stock} in stock)")
        
    print("--------------------------------------\n") # End of menu display


def select_item(balance, subtotal):
    """Allows user to select an item from the menu, checks for any constraints, and returns the name of the item(s)."""
    
    # Shows the current menu and balance before asking for item selection
    show_menu()
    print(f"Current balance: {price_str(balance)}")

    choice = input("Select an item from menu or type 'Done' to finish: ").lower().strip() # Allowing user to type done in any font case when completed with selecting items.
    
    if choice == "done":
        return None
    
    # Validation Checks:
    
    # Invalid item
    if choice not in items:
        print(f"\nInvalid item: '{choice}'. Please select an item from the menu!") # Informs user about invalid item
        return "invalid" # Returns invalid to indicate an error
    
    item_data = items[choice]
    
    # Out of stock
    if item_data["stock"] <= 0:
        print(f"\n{choice.capitalize()} is currently out of stock! Please select another item.") # Informs user about out of stock item
        return "invalid" # Returns invalid to indicate an error
    
    # Insufficient funds
    if item_data["price"] > balance:
        needed = price_str(item_data["price"] - balance)
        print(f"\nInsufficient funds for {choice.capitalize()}! You need {needed} more.") # Informs user about insufficient funds
        return "invalid" # Returns invalid to indicate an error

    return choice # Returns the valid item name


def apply_discounts(subtotal, item_count):
    """Calculates highest discount percentage."""
 
    discount_percent = 0
    
    # 3 items = 5%
    if item_count >= 3:
        discount_percent = max(discount_percent, 5)
        
    # More than £5 (500 pence) = 10%
    if subtotal > 500:
        discount_percent = max(discount_percent, 10)
        
    # More than £7 (700 pence) = 15%
    if subtotal > 700:
        discount_percent = max(discount_percent, 15)
        
    # Max() function - allowing only highest discount to be applied.
    return discount_percent


def calculate_change(change):
    """ Calculates returning change - using accepted coins; machine keeps remaining amount which cannot be returned."""
    
    change_given = []
    remaining = change # Amount left to give as change

    for coin in sorted(accepted_coins, reverse=True): # Ensure we start with largest coin
        if remaining >= coin:
            count = remaining // coin # How many of this coin we can give
            change_given.extend([coin] * count)
            remaining -= (coin * count)

    return change_given, remaining


def receipt_csv(order_number, timestamp, basket, subtotal, discount_amount, total_after_discount, amount_paid, change_given, kept):
    """Generates a CSV receipt file for the order.""" # Receipt filename with order number and timestamp
    
    filename = f"receipt_order_{order_number}_{timestamp.strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        
        writer.writerow(["VENDING MACHINE RECEIPT"]) # Receipt Header
        writer.writerow([]) # Empty line for spacing
        writer.writerow(["Order Number", order_number])
        writer.writerow(["Date/Time", timestamp.strftime("%Y-%m-%d %H:%M:%S")])
        writer.writerow([]) # Empty line for spacing
        
        writer.writerow(["Item", "Price"]) # Items Purchased
        for name, price in basket:
            writer.writerow([name.capitalize(), price_str(price)])

        writer.writerow([]) # Empty line for spacing
        writer.writerow(["Subtotal", price_str(subtotal)]) # Subtotal before discount
        writer.writerow(["Discount Applied", price_str(discount_amount)]) # Discount applied
        writer.writerow(["Total Spent (Final Cost)", price_str(total_after_discount)])  # Total after discount      
        writer.writerow(["Amount Paid (Coins Inserted)", price_str(amount_paid)]) # Amount paid by customer
        writer.writerow(["Change Returned", ", ".join(price_str(c) for c in change_given) if change_given else price_str(0)]) # Change returned
        writer.writerow(["Amount Kept by Machine", price_str(kept)]) # Amount machine keeps if it cannot return exact change

    print(f"\n*** Receipt generated: {filename} ***")


# Main Session


def vending_machine_session(order_num):
    """Completes a customer transaction successfully."""
    global items # Accesses and modifies stock levels 
    
    timestamp = datetime.now()
    
    print("\n" + "="*40)
    print(f"            CUSTOMER ORDER #{order_num}")    # Order Header
    print("="*40)

    # Initial Balance (0p) before coin insertion
    balance = 0
    print(f"Current balance: {price_str(balance)}")

    balance = insert_coins(balance)
    amount_paid = balance # Record how much was inserted before purchases start

    basket = []
    subtotal = 0

    # Purchase Loop
    while True:
        # Pass the current balance and subtotal to the select item function for checks
        choice = select_item(balance, subtotal) 
        
        if choice is None: # Customer typed 'done'
            break
        if choice == "invalid":
            continue

        # After Valid Item/s Selected - proceed with purchase
        
        price = items[choice]["price"]
        
        # Stock update, balance deduction, subtotal update, and adding item to basket
        items[choice]["stock"] -= 1
        balance -= price
        subtotal += price
        basket.append((choice, price))
        
        # Informing user of successful purchase
        print(f"\nPurchased {choice.capitalize()} for {price_str(price)}.")
        # Total spent and discount are shown at the end of the session
        print(f"Remaining balance: {price_str(balance)}")


    #  End of Purchases: Finance Calculations 

    item_count = len(basket)
    
    # Apply discount 
    discount_percent = apply_discounts(subtotal, item_count)
    
    # Discount amount rounded down to nearest whole pence
    discount_amount = math.floor((subtotal * discount_percent) / 100)
    total_after_discount = subtotal - discount_amount

    # Refund the discount to the customer's balance so it is reflected in their change
    balance += discount_amount

    # Bonus Rule 
    bonus = 0
    # Check for odd order number AND total spent > £2 (200 pence)
    if order_num % 2 == 1 and subtotal > 200:
        bonus = 100 # £1.00 bonus
        # The bonus is added to the balance
        balance += bonus
        print(f"\n*** BONUS APPLIED: +{price_str(bonus)} (Order #{order_num} and total > {price_str(200)}) ***")

    # Calculate Change
    change_due = balance
    change_given, kept = calculate_change(change_due)

    # Summary printout
    
    print("\n--- TRANSACTION SUMMARY ---")
    print(f"Subtotal (before discount): {price_str(subtotal)}")
    print(f"Discount applied: {discount_percent}% ({price_str(discount_amount)})")
    print(f"Total spent (after discount): {price_str(total_after_discount)}")
    
    if bonus > 0:
         print(f"Received bonus: {price_str(bonus)}")
    
    print(f"Change due: {price_str(change_due)}")
    print(f"Change returned: {', '.join(price_str(c) for c in change_given) if change_given else price_str(0)}")
    print(f"Change kept by machine: {price_str(kept)}")
    
    # Generate Receipt
    receipt_csv(order_num, timestamp, basket, subtotal, discount_amount, total_after_discount, amount_paid, change_given, kept)

    print("\nTransaction completed. Thank you! Have a great day!")
    print("="*40)


# Main page loops 


def main():
    """Starts and controls the vending machine flow."""
    global order_num
    print("-------- VENDING MACHINE STARTED -------") # Machine Start Header

    while True:
        # Run a session and pass the global order number
        vending_machine_session(order_num)
        
        # Increment the order number for the next customer
        order_num += 1

        again = input("Press ENTER for the next customer or type 'finished' to exit: ").strip().lower()
        if again == "finished":
            break # Exit the main loop if finished

    print("\n====== VENDING MACHINE CLOSING DOWN ======") # Machine Shutdown Header


if __name__ == "__main__": 
    main()
