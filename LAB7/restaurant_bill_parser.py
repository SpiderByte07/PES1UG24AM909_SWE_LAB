def clean_dish_name(name):
    """Remove special markers and title-case a dish name."""
    if not isinstance(name, str):
        return ""

    name = name.strip()
    for marker in ("*", "#", "~"):
        name = name.replace(marker, "")
    return name.title()


def parse_item_prices(text):
    """Parse valid non-negative whole-number prices from comma-separated text."""
    if not isinstance(text, str):
        return []

    prices = []
    for value in text.split(","):
        try:
            price = int(value.strip())
        except (ValueError, TypeError):
            continue

        if price >= 0:
            prices.append(price)

    return prices


def split_amount(text):
    """Return each person's share, or None when the input is invalid."""
    if not isinstance(text, str):
        return None

    parts = text.split("/")
    if len(parts) != 2:
        return None

    try:
        total = int(parts[0].strip())
        people = int(parts[1].strip())
    except (ValueError, TypeError):
        return None

    if total < 0 or people <= 0:
        return None

    return total // people

def main():
    print("==== Running clean_dish_name ====")
    value = input("Enter a dish name from the menu (e.g. *paneer tikka*): ")
    print("Dish name:", clean_dish_name(value))

    print("\n==== Running parse_item_prices ====")
    value = input("Enter item prices separated by commas (e.g. 250,180,320): ")
    print("Item prices:", parse_item_prices(value))

    print("\n==== Running split_amount ====")
    value = input("Enter the bill and number of people as TOTAL/PEOPLE (e.g. 1200/4): ")
    print("Each person pays:", split_amount(value))


if __name__ == "__main__":
    main()
