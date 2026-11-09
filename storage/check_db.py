from storage.db_storage import  query_recorded_events


rows = query_recorded_events()
print(f"There are {len(rows)} rows")

for row in rows:
    print(row)
