import os
import pandas as pd
import random
import uuid
from pathlib import Path

CATEGORIES = {
    "бытовая химия": ["полiроль", "пральний порошок", "мило", "рідке мило", "ополіскувач"],
    "текстиль": ["рушник", "подушка", "покривало", "скатертина"],
    "посуда": ["тарілка", "філіжанка", "ложка", "сковорода"],
    "кухонні прилади": ["чайник", "тертка", "ложка для салату"],
    "інше": ["лампочка", "свічка", "ремонтний набір"]
}

def make_doc_id(shop, cash):
    return f"{shop}-{cash}-{uuid.uuid4().hex[:8]}"

def random_price():
    return round(random.uniform(5, 500), 2)

def random_discount(price, amount):
    if random.random() < 0.6:
        return 0.0
    max_disc = price * amount * 0.3
    return round(random.uniform(0, max_disc), 2)

def generate_receipt_rows(doc_id):
    rows = []
    num_positions = random.randint(1, 5)
    for _ in range(num_positions):
        category = random.choice(list(CATEGORIES.keys()))
        item = random.choice(CATEGORIES[category])
        amount = random.randint(1, 4)
        price = random_price()
        discount = random_discount(price, amount)
        rows.append({
            "doc_id": doc_id,
            "item": item,
            "category": category,
            "amount": amount,
            "price": price,
            "discount": discount
        })
    return rows

def generate_file(shop, cash, receipts_count, outdir):
    rows = []
    for _ in range(receipts_count):
        doc_id = make_doc_id(shop, cash)
        rows.extend(generate_receipt_rows(doc_id))
    df = pd.DataFrame(rows)
    fname = Path(outdir) / f"{shop}_{cash}.csv"
    df.to_csv(fname, index=False, encoding="utf-8")
    print(f"Згенеровано {fname} ({receipts_count} чеків)")

def main():
    outdir = Path("./data")
    outdir.mkdir(parents=True, exist_ok=True)

    shops = 5
    max_cashes = 3
    for shop in range(1, shops + 1):
        cash_count = random.randint(1, max_cashes)
        for cash in range(1, cash_count + 1):
            receipts = random.randint(10, 50)
            generate_file(shop, cash, receipts, outdir)

if __name__ == "__main__":
    main()
