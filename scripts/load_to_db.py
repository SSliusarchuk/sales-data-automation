import os
import re
import logging
from pathlib import Path
from datetime import datetime
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values  # для пакетної вставки
from dotenv import load_dotenv

FNAME_RE = re.compile(r"^(\d+)_(\d+)\.csv$")

def main():
    data_dir = Path("./data")
    log_dir = Path("./logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    logfile = log_dir / f"load_{datetime.now().date()}.log"
    logging.basicConfig(level=logging.INFO,
                        handlers=[logging.FileHandler(logfile, encoding='utf-8'),
                                  logging.StreamHandler()],
                        format="%(asctime)s [%(levelname)s] %(message)s")

    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 5432))
    )
    conn.autocommit = False

    for entry in sorted(data_dir.iterdir()):
        if not entry.is_file():
            continue
        m = FNAME_RE.match(entry.name)
        if not m:
            logging.info(f"Пропускаю файл {entry.name}")
            continue
        shop_num = int(m.group(1))
        cash_num = int(m.group(2))

        try:
            df = pd.read_csv(entry)
            df["amount"] = df["amount"].fillna(0).astype(int)
            df["price"] = df["price"].fillna(0).astype(float).round(2)
            df["discount"] = df["discount"].fillna(0).astype(float).round(2)

            # Створюємо чекі
            receipts = pd.DataFrame({
                "doc_id": df["doc_id"].unique(),
                "shop_num": shop_num,
                "cash_num": cash_num
            })

            with conn.cursor() as cur:
                # Пакетна вставка чеків
                receipt_values = [(r["doc_id"], r["shop_num"], r["cash_num"]) for _, r in receipts.iterrows()]
                execute_values(
                    cur,
                    "INSERT INTO receipts (doc_id, shop_num, cash_num) VALUES %s ON CONFLICT (doc_id) DO NOTHING",
                    receipt_values
                )

                # Пакетна вставка товарів
                item_values = [
                    (row["doc_id"], row["item"], row["category"], row["amount"], row["price"], row["discount"])
                    for _, row in df.iterrows()
                ]
                execute_values(
                    cur,
                    "INSERT INTO items (doc_id, item, category, amount, price, discount) VALUES %s",
                    item_values
                )

                conn.commit()

            os.remove(entry)
            logging.info(f"Оброблено і видалено {entry.name}")

        except Exception as e:
            conn.rollback()
            logging.exception(f"Помилка у файлі {entry.name}: {e}")

    conn.close()

if __name__ == "__main__":
    main()