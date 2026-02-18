import mysql.connector as db
from datetime import datetime

date = datetime.now().strftime("%Y-%m-%d")
con = db.connect(user='root', password='2616',\
                 host='localhost', database='restaurant_management')
cur = con.cursor()
def veg_orders():
    cur.execute('select * from veg_menu')
    result=cur.fetchall()
    print('*'*10 , 'Veg Menu' ,'*'*10)
    for item_id,item_name,item_price in result:
        
        print(f'{item_id : <5} {item_name : <30} - {item_price}')
def nonveg_orders():
    cur.execute('select * from nonveg_menu')
    result=cur.fetchall()
    print('*'*10 , 'Non Veg Menu' ,'*'*10)
    for item_id,item_name,item_price in result:
        
        print(f'{item_id : <5} {item_name : <30} - {item_price}')
def cool_drinks():
    cur.execute('select * from cool_drinks')
    result=cur.fetchall()
    print('*'*10 , 'Cool Drinks Menu' ,'*'*10)
    for item_id,item_name,item_price in result:
        print(f'{item_id : <5} {item_name : <30} - {item_price}')
def rotties():
    cur.execute('select * from rotties_menu')
    result=cur.fetchall()
    print('*'*10 , 'Rotties Menu' ,'*'*10)
    for item_id,item_name,item_price in result:
        print(f'{item_id : <5} {item_name : <30} - {item_price}')
#----------------------------cart---------------------------------#    
def add_to_cart(user_id,menu_type):
    if menu_type == 'veg':
        table = 'veg_menu'
    elif menu_type == 'nonveg':
        table = 'nonveg_menu'
    elif menu_type == 'drinks':
        table = 'cool_drinks'
    elif menu_type == 'rotties':
        table = 'rotties_menu'
    
    else:
        print('-'*5,"Invalid menu type",'-'*5)
        return

    while True:
        
        item_id=int(input("Enter the Item Id to add to cart: "))
        quantity=int(input("Enter the Quantity: "))
        cur.execute(f'select item_name,item_price from {table} where item_id=%s',(item_id,))
        item=cur.fetchone()
        if item:
            item_name,item_price=item
            total_price=item_price*quantity
            cur.execute('''insert into cart(user_id,item_name,item_price,quantity,total_price) values (%s,%s,%s,%s,%s)''',
                            (user_id,item_name,item_price,quantity,total_price))
            con.commit()
            print('-'*5,f'{item_name} (*{quantity}) added to cart successfully for user {user_id}','-'*5)
            break
            

                
        else:
            print('-'*5,'item not found. please check your id','-'*5)
        
def view_cart(user_id):
    cur.execute('''
         select cart_id,item_name,quantity,item_price,date_time from cart where user_id=%s and date(date_time)=%s
                    ''',(user_id,date)
                    )
    items = cur.fetchall()
    if not items:
        print("Your cart is empty.")
        return
    print('=='*10,'Your cart','=='*10)
    print("\n" + "+" + "-"*78 + "+")
    print(f"| {'Cart_id'.ljust(10)} | {'Item Name'.ljust(20)} | {'Qunatity'.ljust(8)} | {'Price'.ljust(10)} | {'Total'} ")
    print("+" + "-"*78 + "+")
    for cart_id, item_name, quantity, item_price,date_time in items:
        total = quantity * item_price
        print(f"| {str(cart_id).ljust(9)} | {item_name.ljust(22)}| {str(quantity).ljust(8)}| {str(item_price).ljust(10)} | {str(total).ljust(10)}")
    print("+" + "-"*78 + "+\n")
    cur.execute('''
                    select sum(quantity * item_price)
                    from cart
                    where user_id=%s and date(date_time)=%s
                    ''',(user_id,date))
    total_bill = cur.fetchone()[0]
    if total_bill is None:
        total_bill = 0
    total_bill=int(total_bill)
    print("Total Amount to Pay = ",total_bill)
def modify_cart(user_id):
    while True:
        print("\nOptions:")           
        print("1.Modify Item Quantity")
        print("2.Delete Item")
        print("3.Back")
        choice=input("Choose an option: ")
        if choice == '1':
            view_cart(user_id)
            cart_id = input("Enter Cart Id to modify: ")
            new_qty = int(input("Enter new quantity: "))
            if new_qty>=1:
                cur.execute("update cart set quantity=%s where cart_id=%s ",(new_qty,cart_id))
                con.commit() 
                print('=='*5,"Quantity updated successfully.",'='*10)
                
                    
        elif choice=='2':
            view_cart(user_id)
            cart_id = input("Enter Cart Id to delete: ")
            cur.execute("delete from cart where cart_id=%s ",(cart_id))
            con.commit()
            print('=='*5,"Item deleted successfully.",'='*10)
                
                
        elif choice=='3':
            print('--'*5,'Exited from the modify  cart','--'*5)
            break
        else:
            print('='*5,"Invalid option",'='*5)
            

        
def generate_bill(user_id):
    view_cart(user_id)
    
                  
   
    
if __name__=='__main__':
    user_id = int(input("Enter your user ID: "))
    veg_orders()
    nonveg_orders()
    cool_drinks()
    rotties()
    add_to_cart(user_id,menu_type)
    view_cart(user_id)
    modify_cart(user_id)
    generate_bill(user_id)

    cur.close()
    con.close()
    
       
 
    
    
    
            
        
            
            
        
