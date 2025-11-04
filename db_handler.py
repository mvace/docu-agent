import json

# Define the filename as a constant, so it's easy to change in one place
DB_FILENAME = "appliance_db.json"


def _read_db():
    try:
        with open(DB_FILENAME, "r") as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty/corrupt,
        # return an empty dictionary.
        return {}
    except Exception as e:
        print(f"An unexpected error occurred while reading {DB_FILENAME}: {e}")
        return {}


def _write_db(data):
    try:
        with open(DB_FILENAME, "w") as f:
            json.dump(data, f, indent=4)
            return True
    except Exception as e:
        print(f"An error occurred while writing to {DB_FILENAME}: {e}")
        return False


def get_appliance_list():
    data = _read_db()
    return list(data.keys())


def add_appliance(appliance_name, faiss_index_path):
    print(f"Attempting to add/update: {appliance_name}...")

    # --- 1. READ ---
    data = _read_db()

    # --- 2. MODIFY ---
    data[appliance_name] = faiss_index_path

    # --- 3. WRITE ---
    if _write_db(data):
        print(f"Successfully added/updated '{appliance_name}' in {DB_FILENAME}")
    else:
        print(f"Failed to write update for '{appliance_name}'")
