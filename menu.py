import mysql.connector as db
from datetime import datetime
from user import veg_orders, nonveg_orders, cool_drinks, rotties 
date = datetime.now().strftime("%Y-%m-%d")
con = db.connect(user='root', password='2616',\
                 host='localhost', database='restaurant_management')
cur = con.cursor()
def admin_page():
    print('--'*5,'Admin Page','--'*5)
    while True:
        print('1. Add Items to the menu')
        print()
        print('2.Show  whole menu ')
        print()
        print('3.Add New Item to the menu')
        print()
        print('4. Modify items from menu')
        print()
        print('5. Delete items from menu')
        print()
        print('6. View all order details')
        print()
        print('7. Day wise profit')
        print()
        print('8.log out')
        print()
        choice =input("Enter your option: ")
        if choice=='1':
            add_menu()             
                    
        elif choice =='2':
            whole_menu()
                    
        elif choice=='3':
            add_new_item()
                    
        elif choice == '4':
            modify_menu()
                  
        elif choice=='5':
            delete_item()
        elif choice=='6':
            view_all_orders()
        elif choice =='7':
            day_wise_profit()
            
        else:
            print('-'*5,'logged Out from Admin','-'*5)
            print('--'*40)
            break


veg_items = [
    ('Spcl Veg Biryani', 180),
    ('Spcl Paneer Biryani', 170),
    ('Kaju Paneer Biryani', 290),
    ('Mixed Veg Biryani', 180),
    ('Mushroom Biryani', 250),
    ('Paneer 65', 130),
    ('Mushroom 65', 130),
    ('Gobi Manchurian', 120),
    ('Baby Corn 65', 100),
    ('Paneer Butter Masala', 120),
    ('Palak Paneer', 120),
    ('Mixed Veg Curry', 100),
    ('Cashew Paneer', 160)
    ]

nonveg_items = [
    ('Chicken Biryani', 210),
    ('Chicken Dum Biryani', 290),
    ('Mutton Biryani', 400),
    ('Fish Biryani', 350),
    ('Prawns Biryani', 400),
    ('Chilli Chicken', 180),
    ('Chicken 65', 180),
    ('Chicken Manchurian', 190),
    ('Chilli Fish', 190),
    ('Chicken Curry', 170),
    ('Chicken Liver Fry', 150),
    ('Boneless Chicken Curry', 190),
    ('Gongura Chicken', 180)
    ]

cool_drinks = [
    ('Thumbs-up', 20),
    ('Sprite', 20),
    ('Coca-Cola', 20),
    ('Pepsi', 20)
    ]
rotties_menu = [
    ('Butter Naan', 30),
    ('Plain Naan', 25),
    ('Paratha', 30),
    ('Butter Roti', 20)
    ]

menu_tables = {
    "1": ("Veg Menu", "veg_menu"),
    "2": ("Non-Veg Menu", "nonveg_menu"),
    "3": ("Cool Drinks", "cool_drinks"),
    "4": ("Rotties", "rotties_menu")
}


menu_items = {
    "veg_menu": veg_items,
    "nonveg_menu": nonveg_items,
    "cool_drinks": cool_drinks,
    "rotties_menu": rotties_menu
    }

# Add default menu
def add_menu():
    for table_name, items in menu_items.items():
        for item_name, item_price in items:
            # Check if the item already exists
            cur.execute(f"SELECT item_name FROM {table_name} WHERE item_name=%s AND item_price=%s", (item_name, item_price))
            if not cur.fetchone():
                cur.execute(f"INSERT INTO {table_name} (item_name, item_price) VALUES (%s, %s)", (item_name, item_price))
                print(f"{item_name} added to {table_name}")
    con.commit()
    print("already item exits")
    


# Decorator for menu selection
def select_menu(func):
    def wrapper():
        print("\n===== Select Menu Category =====")
        print("1. Veg Menu")
        print("2. Non-Veg Menu")
        print("3. Cool Drinks")
        print("4. Rotties")

        choice = input("Enter your choice: ")
        if choice not in menu_tables :
            print("Invalid choice!")
            return
            

        category,table_name = menu_tables[choice]
        cur.execute(f"SELECT item_id,item_name, item_price FROM {table_name}")
        rows = cur.fetchall()
        print(f"\n--- {category} ---")
        if rows:
            
            print("+" + "-"*40 + "+")
            for item_id,item_name, item_price in rows:
                print(f"{str(item_id).ljust(10)} | {item_name.ljust(25)} | Rs {str(item_price).ljust(10)}")
            print("+" + "-"*40 + "+")
        else:
            print(f"No items in {table_name} yet.")
        
        return func(table_name)
    return wrapper


def whole_menu():
    for _,(category, table_name) in menu_tables.items():
        print(f"\n--- {category} ---")
        cur.execute(f"SELECT item_name, item_price FROM {table_name}")
        items = cur.fetchall()
        if not items:
            print("No items in this menu")
           

        else:
            print("+" + "-"*40 + "+")
            for item_name, item_price in items:
                print(f"{item_name.ljust(25)} | Rs {str(item_price).ljust(10)}")
            print("+" + "-"*40 + "+")
@select_menu
def add_new_item(table_name):
    item_n = input('Enter the item name to add into menu: ')
    item_p =input("Enter the item price of the item : ")
    if not item_n.strip() or not item_p.strip():
        print("You didn't Enter any item name or price to add into menu")
    
    cur.execute(f"SELECT item_name FROM {table_name} WHERE item_name=%s AND item_price=%s", (item_n, item_p))
    if cur.fetchone():
        print(f"{item_name} already exists in {table_name}")
        
    else:
        cur.execute(f'INSERT INTO {table_name}(item_name, item_price) VALUES (%s, %s)',(item_n,item_p))
        con.commit()
        print("New Item added succesfully to the menu ") 

    

@select_menu
def modify_menu(table_name):
    item_id = input("Enter the Item ID to modify: ")
    new_name = input("Enter new name (leave blank if no change): ")
    new_price = input("Enter new price (leave blank if no change): ")

  
    if new_name:
        cur.execute(f"UPDATE {table_name} SET item_name=%s WHERE item_id=%s", (new_name, item_id))

    if new_price:
        cur.execute(f"UPDATE {table_name} SET item_price=%s WHERE item_id=%s", (new_price, item_id))

    con.commit()
    print("Item Updated Successfully!")
@select_menu
def  delete_item(table_name):
    item_id = input("Enter the Item ID to modify: ")
    if item_id:
        cur.execute(f"delete from {table_name} WHERE item_id = %s", (item_id,))
        
        con.commit()
        print('--'*5,'items are deleted sucessfull','--'*5)
    

   
    
                         
def view_all_orders():
   
    cur.execute("""
    SELECT c.cart_id, u.user_name, c.item_name, c.item_price, 
           c.quantity, c.total_price, c.date_time
    FROM cart c
    JOIN user u ON c.user_id = u.user_id
    WHERE DATE(c.date_time) = current_date
    """)

    orders = cur.fetchall()

    print("\n------- ALL ORDER DETAILS -------\n")

    if not orders:
        print("No orders found for Today.")
    else:
        for order in orders:
            print(f"Order ID     : {order[0]}")
            print(f"User Name    : {order[1]}")  
            print(f"Item Name    : {order[2]}")
            print(f"Item Price   : {order[3]}")
            print(f"Quantity     : {order[4]}")
            print(f"Total Amount : ₹{order[5]}")
            print(f"Order Date   : {order[6]}")
            print("----------------------------------")
def day_wise_profit():
    cur.execute("""
        SELECT DATE(date_time), SUM(total_price)
        FROM cart
        GROUP BY DATE(date_time)
        ORDER BY DATE(date_time) asc
    """)
    result = cur.fetchall()

    print("\n-------------- DAY WISE PROFIT ----------------")
    if not result:
        print("No orders found.")
        return
    
    for day, profit in result:
        print(f"{day}  -->  {profit}")
    print("-----------------------------\n")

   



    
if __name__ == '__main__':
    admin_page()
    add_menu()
    whole_menu()
    add_new_item()
    modify_menu()
    delete_item()
    view_all_orders()
    day_wise_profit()
    cur.close()
    con.close()



        
    
