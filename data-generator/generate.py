from pathlib import Path
from datetime import datetime, timedelta
import random

import pandas as pd
from faker import Faker


fake = Faker()
random.seed(42)
Faker.seed(42)

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_customers(n=100):
    rows = []

    tiers = ["Standard", "Premium", "Enterprise"]
    regions = ["Northeast", "Southeast", "Midwest", "Southwest", "West"]

    for customer_id in range(1, n + 1):
        rows.append({
            "customer_id": customer_id,
            "customer_name": fake.company(),
            "region": random.choice(regions),
            "account_tier": random.choice(tiers),
            "created_at": fake.date_time_between(
                start_date="-3y",
                end_date="-30d"
            )
        })

    return pd.DataFrame(rows)


def generate_carriers():
    carriers = [
        {"carrier_id": 1, "carrier_name": "NorthLine Freight", "service_level": "Standard", "base_rate": 18.50},
        {"carrier_id": 2, "carrier_name": "Velocity Express", "service_level": "Express", "base_rate": 27.00},
        {"carrier_id": 3, "carrier_name": "Atlas Logistics", "service_level": "Standard", "base_rate": 20.00},
        {"carrier_id": 4, "carrier_name": "Summit Transport", "service_level": "Priority", "base_rate": 31.50},
    ]

    return pd.DataFrame(carriers)


def generate_shipments(customers_df, carriers_df, n=500):
    rows = []

    statuses = [
        "Created",
        "In Transit",
        "Delivered",
        "Delayed",
        "Cancelled"
    ]

    warehouses = ["WH001", "WH002", "WH003", "WH004"]

    start_date = datetime(2026, 9, 1)

    for shipment_id in range(1, n + 1):
        shipped_at = start_date + timedelta(
            days=random.randint(0, 20),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )

        promised_delivery_at = shipped_at + timedelta(
            days=random.randint(2, 5)
        )

        status = random.choice(statuses)

        actual_delivery_at = None
        if status == "Delivered":
            actual_delivery_at = promised_delivery_at + timedelta(
                hours=random.randint(-24, 48)
            )

        rows.append({
            "shipment_id": shipment_id,
            "customer_id": random.choice(customers_df["customer_id"].tolist()),
            "carrier_id": random.choice(carriers_df["carrier_id"].tolist()),
            "origin_warehouse_id": random.choice(warehouses),
            "destination_region": random.choice(
                ["Northeast", "Southeast", "Midwest", "Southwest", "West"]
            ),
            "shipped_at": shipped_at,
            "promised_delivery_at": promised_delivery_at,
            "actual_delivery_at": actual_delivery_at,
            "status": status,
            "shipping_cost": round(random.uniform(20, 250), 2),
            "updated_at": shipped_at + timedelta(
                hours=random.randint(1, 72)
            )
        })

    return pd.DataFrame(rows)


def generate_warehouse_events(shipments_df):
    rows = []
    event_id = 1

    event_types = [
        "Received",
        "Sorted",
        "Loaded",
        "Departed"
    ]

    for _, shipment in shipments_df.iterrows():
        event_count = random.randint(1, 4)

        for i in range(event_count):
            rows.append({
                "event_id": event_id,
                "shipment_id": shipment["shipment_id"],
                "warehouse_id": shipment["origin_warehouse_id"],
                "event_type": event_types[i],
                "event_timestamp": shipment["shipped_at"] + timedelta(
                    hours=i * random.randint(1, 5)
                )
            })

            event_id += 1

    return pd.DataFrame(rows)


def generate_delivery_updates(shipments_df):
    rows = []

    for _, shipment in shipments_df.iterrows():
        rows.append({
            "shipment_id": shipment["shipment_id"],
            "status": shipment["status"],
            "status_timestamp": shipment["updated_at"],
            "updated_at": shipment["updated_at"]
        })

    return pd.DataFrame(rows)


def main():
    customers = generate_customers()
    carriers = generate_carriers()
    shipments = generate_shipments(customers, carriers)
    warehouse_events = generate_warehouse_events(shipments)
    delivery_updates = generate_delivery_updates(shipments)

    customers.to_csv(OUTPUT_DIR / "customers.csv", index=False)
    carriers.to_csv(OUTPUT_DIR / "carriers.csv", index=False)
    shipments.to_csv(OUTPUT_DIR / "shipments.csv", index=False)
    warehouse_events.to_json(
        OUTPUT_DIR / "warehouse_events.json",
        orient="records",
        indent=2,
        date_format="iso"
    )
    delivery_updates.to_csv(
        OUTPUT_DIR / "delivery_updates.csv",
        index=False
    )

    print("Synthetic data generated successfully.")
    print(f"Customers: {len(customers)}")
    print(f"Carriers: {len(carriers)}")
    print(f"Shipments: {len(shipments)}")
    print(f"Warehouse events: {len(warehouse_events)}")
    print(f"Delivery updates: {len(delivery_updates)}")


if __name__ == "__main__":
    main()