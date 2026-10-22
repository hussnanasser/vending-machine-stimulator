# Vending Machine Simulator

A command-line vending machine simulator written in Python. It was built for a university programming assignment and covers coin handling, stock management, discounts, a bonus rule, change calculation and CSV receipt generation.

## Features

- **Flexible coin input**: accepts £2, £1, 50p and 20p in several formats (e.g. `£1`, `1.00`, `100p`, `100`). Anything else is rejected as an invalid coin.
- **Stock tracking**: each item has a price and a stock level, and stock drops with every purchase. Out-of-stock items can't be bought.
- **Input validation**: handles invalid item names, out-of-stock items and insufficient funds with clear messages.
- **Multiple items per order**: customers can buy as many items as their balance allows before typing `done`.
- **Discounts**: only the single highest applicable discount is applied.

  | Condition | Discount |
  |---|---|
  | 3 or more items | 5% |
  | Subtotal over £5.00 | 10% |
  | Subtotal over £7.00 | 15% |

- **Bonus rule**: on odd-numbered orders with a subtotal over £2.00, the customer receives a £1.00 bonus added to their balance.
- **Change calculation**: change is returned using the largest accepted coins first. If an amount can't be made exactly from the accepted coins, the machine keeps the remainder.
- **CSV receipts**: every order generates a timestamped receipt file, e.g. `receipt_order_1_20261022_143015.csv`.
- **Multiple customers**: the machine keeps running, incrementing the order number, until `finished` is typed.

## Menu

| Item | Price | Starting stock |
|---|---|---|
| Water | £1.20 | 10 |
| Soda | £1.50 | 12 |
| Chocolate | £2.50 | 15 |
| Crisps | £1.40 | 12 |
| Sandwich | £3.80 | 8 |
| Protein bar | £3.00 | 2 |
| Protein shake | £4.50 | 8 |
| Flapjack | £2.40 | 9 |

## Requirements

- Python 3.6 or newer
- No external libraries (uses only `csv`, `math` and `datetime` from the standard library)

## How to Run

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
python vending_machine.py
```

## Example Session

```
======================================
            CUSTOMER ORDER #1
======================================
Current balance: £0.00

------ Insert Money ------
Please insert coin(s) (£2, £1, 50p, 20p) or type 'Done' to finish: £2
Current Balance: £2.00
Please insert coin(s) (£2, £1, 50p, 20p) or type 'Done' to finish: done

Select an item from menu or type 'Done' to finish: water
Purchased Water for £1.20.
Remaining balance: £0.80
```

## How It Works

- **Prices are stored in pence** (integers) to avoid floating-point rounding errors. They are only converted to `£x.xx` strings for display by `price_str()`.
- Discounts are rounded **down** to the nearest whole penny.
- Main functions:
  - `insert_coins()`: coin entry and validation
  - `show_menu()` / `select_item()`: menu display and purchase checks
  - `apply_discounts()`: works out the best discount
  - `calculate_change()`: greedy coin-based change
  - `receipt_csv()`: writes the receipt file
  - `vending_machine_session()` / `main()`: control the flow of an order and the machine

## Possible Improvements

- Store items and stock in an external file (JSON/CSV) so they persist between runs
- Add an admin mode for restocking and changing prices
- Track the machine's coin float so change is limited by what it actually holds
- Add unit tests for discounts, change calculation and input parsing

## Author

Created as part of a programming assignment.
