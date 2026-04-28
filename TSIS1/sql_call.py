import psycopg2            
import csv                 
from config import load_config  

def search_contacts(pattern):
    try:
        with psycopg2.connect(**load_config()) as conn:
            with conn.cursor() as cur:
                # Replace 'get_contacts_by_pattern' with your actual function name
                cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
                results = cur.fetchall()
                for row in results:
                    print(row)
    except Exception as e:
        print(f"Error calling function: {e}")

def run_upsert(name, phone):
    try:
        with psycopg2.connect(**load_config()) as conn:
            with conn.cursor() as cur:
                # Replace 'upsert_contact' with your actual procedure name
                cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
                conn.commit()
                print("Procedure executed and changes committed.")
    except Exception as e:
        print(f"Error calling procedure: {e}")

def bulk_insert(names, phones):
    try:
        with psycopg2.connect(**load_config()) as conn:
            with conn.cursor() as cur:
                # Python lists [a, b] are automatically converted to Postgres arrays {a, b}
                cur.execute("SELECT * FROM bulk_insert_with_validation(%s, %s)", (names, phones))
                errors = cur.fetchall()
                if errors:
                    print("Found invalid entries:", errors)
                conn.commit()
    except Exception as e:
        print(f"Bulk insert error: {e}")

if __name__ == '__main__':
    search_contacts("Ad")