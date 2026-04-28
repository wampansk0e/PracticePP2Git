import psycopg2
import os
import json

def setup_database(conn):
    # This ensures we get the folder where THIS script is currently sitting (TSIS1)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    sql_files = ['functions.sql', 'procedures.sql']
    
    for file_name in sql_files:
        file_path = os.path.join(current_dir, file_name)
        
        with conn.cursor() as cur:
            try:
                # errors='replace' handles that 0xc2 byte from your Russian comments
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    sql_content = f.read()
                    
                    # Log the path so you can see it in the console
                    print(f"Reading: {file_path}")
                    
                    cur.execute(sql_content)
                conn.commit()
                print(f"✅ Successfully updated database with logic from: {file_name}")
            except Exception as e:
                # CRITICAL: This resets the connection so you don't get 'transaction aborted' errors
                conn.rollback()
                print(f"❌ Failed to update {file_name}: {e}")

def main():
    # Update with your local connection details
    db_config = {
        "host": "localhost",
        "database": "suppliers",
        "user": "postgres",
        "password": "password"
    }

    try:
        conn = psycopg2.connect(**db_config)
        
        # Apply the encoding fix immediately on startup
        setup_database(conn)

        while True:
            print("\n--- PHONEBOOK CONSOLE ---")
            print("1. View Contacts (Paginated)")
            print("2. Search (Pattern Match)")
            print("3. Upsert (Add or Update)")
            print("4. Delete Contact")
            print("5. Filter by Group")
            print("6. Export all to JSON")
            print("7. Import from JSON")
            print("8. Update Phone for Existing Contact")
            print("9. Move a Contact to Another Group")
            print("q. Quit")
            
            choice = input("Select an option: ").strip().lower()

            if choice == '1':
                # Uses: get_contacts_paginated(p_limit, p_offset)
                run_pagination(conn)
            elif choice == '2':
                # Uses: get_contacts_by_pattern(search_pattern)
                run_search(conn)
            elif choice == '3':
                # Uses: upsert_contact(p_name, p_phone)
                run_upsert(conn)
            elif choice == '4':
                # Uses: delete_contact_by_data(p_identifier)
                run_delete(conn)
            elif choice == '5':
                run_group_filter(conn)
            elif choice == '6':
                export_to_json(conn)
            elif choice == '7':
                import_from_json(conn)
            elif choice == '8':
                run_add_phone(conn)
            elif choice == '9':
                run_move_group(conn)
            elif choice == 'q':
                break
        
        conn.close()
    except Exception as e:
        print(f"Connection Error: {e}")

def run_pagination(conn):
    limit = 5
    offset = 0
    while True:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
            rows = cur.fetchall()
            print(f"\n--- Page (Offset: {offset}) ---")
            for r in rows:
                print(f"ID: {r[0]} | Name: {r[1]} | Phone: {r[2]}")
            
            nav = input("\n[n] Next | [p] Previous | [b] Back: ").lower()
            if nav == 'n' and len(rows) == limit: offset += limit
            elif nav == 'p' and offset >= limit: offset -= limit
            elif nav == 'b': break

def run_search(conn):
    pattern = input("Enter name or phone pattern: ")
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM get_contacts_by_pattern(%s);", (pattern,))
        for r in cur.fetchall():
            print(f"Found -> ID: {r[0]} | Name: {r[1]} | Phone: {r[2]}")

def run_upsert(conn):
    name = input("Enter Name: ")
    phone = input("Enter Phone: ")
    with conn.cursor() as cur:
        cur.execute("CALL upsert_contact(%s, %s);", (name, phone))
        conn.commit()
        print("Upsert complete.")

def run_delete(conn):
    val = input("Enter Name or Phone to delete: ")
    with conn.cursor() as cur:
        cur.execute("CALL delete_contact_by_data(%s);", (val,))
        conn.commit()
        print("Delete command sent.")

def run_group_filter(conn):
    try:
        group_id = input("Enter Group ID to filter by (e.g., 1 for Family, 2 for Work): ")
        # Ensure input is a number
        group_id = int(group_id)
        
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_by_group(%s);", (group_id,))
            results = cur.fetchall()
            
            print(f"\n--- Contacts in Group {group_id} ---")
            if not results:
                print("No contacts found in this category.")
            else:
                for r in results:
                    print(f"ID: {r[0]} | Name: {r[1]} | Phone: {r[2]} | Email: {r[3] or 'N/A'}")
    except ValueError:
        print("Invalid input. Please enter a numeric Group ID.")
    except Exception as e:
        conn.rollback() # Fix for the 'aborted transaction' error
        print(f"Filter Error: {e}")

def run_search(conn):
    pattern = input("Enter search term (name, phone, or email): ")
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT * FROM get_contacts_by_pattern(%s);", (pattern,))
            results = cur.fetchall()
            
            print(f"\n--- Search Results for '{pattern}' ---")
            if not results:
                print("No matches found.")
            else:
                for r in results:
                    # Results: id, name, email, group
                    print(f"ID: {r[0]} | Name: {r[1]} | Email: {r[2] or 'N/A'} | Group: {r[3] or 'None'}")
        except Exception as e:
            conn.rollback() # Fix for transaction aborts
            print(f"Search Error: {e}")

def export_to_json(conn):
    # Determine the path based on the script's location (TSIS1)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_dir, 'contacts.json')
    
    try:
        with conn.cursor() as cur:
            # We select everything to ensure we include phone and group
            cur.execute("""
                SELECT id, first_name, phone_number, email, group_id, birthday 
                FROM phonebook 
                ORDER BY id
            """)
            rows = cur.fetchall()
            
            # Convert the list of tuples into a list of dictionaries
            contacts_list = []
            for r in rows:
                contacts_list.append({
                    "id": r[0],
                    "name": r[1],
                    "phone": r[2],
                    "email": r[3],
                    "group_id": r[4],
                    "birthday": str(r[5]) if r[5] else None  # Dates must be strings for JSON
                })
            
            # Write to the file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(contacts_list, f, indent=4, ensure_ascii=False)
                
            print(f"✅ Successfully exported {len(contacts_list)} contacts to {filename}")
            
    except Exception as e:
        conn.rollback() # Fix for transaction aborts
        print(f"Export Error: {e}")

def import_from_json(conn):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_dir, 'contacts.json')
    
    if not os.path.exists(filename):
        print(f"❌ Error: {filename} not found.")
        return

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            contacts = json.load(f)
            
        for c in contacts:
            name = c.get('name')
            phone = c.get('phone')
            email = c.get('email')
            group = c.get('group_id')
            
            with conn.cursor() as cur:
                # Check if the name already exists
                cur.execute("SELECT id FROM phonebook WHERE first_name = %s", (name,))
                exists = cur.fetchone()
                
                if exists:
                    print(f"\n⚠️ Duplicate found: '{name}'")
                    choice = input(f"Do you want to [o]verwrite or [s]kip this contact? ").lower()
                    
                    if choice == 'o':
                        cur.execute("""
                            UPDATE phonebook 
                            SET phone_number = %s, email = %s, group_id = %s 
                            WHERE first_name = %s
                        """, (phone, email, group, name))
                        print(f"✅ Updated '{name}'")
                    else:
                        print(f"⏩ Skipped '{name}'")
                else:
                    # New contact, just insert
                    cur.execute("""
                        INSERT INTO phonebook (first_name, phone_number, email, group_id) 
                        VALUES (%s, %s, %s, %s)
                    """, (name, phone, email, group))
                    print(f"✨ Added '{name}'")
            
            conn.commit()
            
    except Exception as e:
        conn.rollback()
        print(f"Import Error: {e}")

def run_add_phone(conn):
    name = input("Enter contact name: ")
    new_phone = input("Enter new phone number: ")
    phone_type = input("Enter phone type (e.g., Work, Home, Mobile): ")
    
    with conn.cursor() as cur:
        try:
            # Calling the procedure using the 'CALL' keyword
            cur.execute("CALL add_phone(%s, %s, %s);", (name, new_phone, phone_type))
            conn.commit()
            print(f"✅ Procedure executed for {name}.")
        except Exception as e:
            conn.rollback()
            print(f"❌ Error adding phone: {e}")

def run_move_group(conn):
    contact = input("Enter contact name: ")
    group = input("Enter target group name: ")
    
    with conn.cursor() as cur:
        try:
            cur.execute("CALL move_to_group(%s, %s);", (contact, group))
            conn.commit()
            print(f"✅ {contact} has been moved to group '{group}'.")
        except Exception as e:
            conn.rollback()
            print(f"❌ Error moving contact: {e}")


if __name__ == "__main__":
    main()