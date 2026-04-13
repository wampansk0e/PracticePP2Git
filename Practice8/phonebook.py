from connect import connect
from config import load_config
import csv

config = load_config()
conn = connect(config)
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        phonenumber VARCHAR(50)
    )
    """)
conn.commit()



with open("contacts.csv", "r") as f:
    contacts = csv.reader(f)
    cursor.executemany(
            """
            INSERT INTO phonebook (name, phonenumber)
            VALUES (%s, %s)
            """, contacts
    )
    conn.commit()



def view_the_table():
    cursor.execute("SELECT * FROM phonebook")
    print(cursor.fetchall())



def add_contact(name, number):
    cursor.execute(
        """
        INSERT INTO phonebook (name, phonenumber)
        VALUES (%s, %s)
        """, (name, number)
    )
    conn.commit()
    return



def update_contact_by_name(name, number):
    cursor.execute(
        """
        UPDATE phonebook
        SET name = %s
        WHERE phonenumber = %s
        """, (name, number))
    conn.commit()
    return


def update_contact_by_number(name, number):
    cursor.execute(
        """
        UPDATE phonebook
        SET phonenumber = %s
        WHERE name = %s
        """, (number, name))
    conn.commit()
    return


def search_contacts(need_contact):
    cursor.execute(
        """
        SELECT * FROM phonebook 
        WHERE name = %s OR phonenumber LIKE %s
        """, (need_contact, need_contact+"%")
    )

    cont = cursor.fetchall()
    
    if not cont:
        print("No contact found")
    else:
        for row in cont:
            print(f"id: {row[0]}\nname: {row[1]}\nphone numebr: {row[2]}\n")
    return 



def delete_contact(need_contact):
    cursor.execute(
        """
        DELETE FROM phonebook
        WHERE name =%s OR phonenumber LIKE %s
        """, (need_contact, need_contact+"%")
    )
    conn.commit()
    num = cursor.rowcount
    if num ==0:
        print("No contacts deleted")
    else:
        print(f"Deleted contacts: {num}")



def menu():
    while True:
        print("\n------ cool phonebook ------")
        print("1. Add a contact")
        print("2. Find a contact")
        print("3. Update a contact by a name")
        print("4. Update a contact by a phone number")
        print("5. Delete a contact")
        print("6. View the table")
        print("7. Quit")

        choose = input("Choose what to do : ")

        if choose == '1':
            namee = input("Write a name: ")
            numberr = input("Write a phone number: ")
            add_contact(namee, numberr)
        elif choose == '2':
            need = input("What are you searching for? : ")
            search_contacts(need)
        elif choose == '3':
            required_name = input("Name whose number you want to change: ")
            numbr = input("What number do you want to replace it with?")
            update_contact_by_name(required_name, numbr)
        elif choose == '4':
            required_number = input("Number whose name you want to change: ")
            nme = input("What name do you want to replace it with?")
            update_contact_by_number(required_number, nme)
        elif choose == '5':
            required_contact = input("What number or name you want to delete?: ")
            delete_contact(required_contact)
        elif choose == '6':
            view_the_table()
        elif choose == '7':
            print("See you soon!")
            break

menu()

cursor.close()
conn.close()