
from menu import admin_page, add_menu,whole_menu,add_new_item,modify_menu,delete_item,view_all_orders, day_wise_profit
from user import veg_orders, nonveg_orders, cool_drinks, rotties, add_to_cart,view_cart,modify_cart,generate_bill
 
import re   
import mysql.connector as db
con=db.connect(user='root',password='2616',host='localhost',database='restaurant_management')
cur=con.cursor()
space='=='
print(space*15,'VCUBE RESTAURANT',space*15)

def admin_login():
    ad_name=input("Enter your Name : ")
    ad_mail=input("Enter your Admin_mail : ")
    pw=input("Enter your password : ")
    cur.execute('select * from admin where admin_name=%s and admin_mail=%s and admin_Password=%s',(ad_name,ad_mail,pw))
    result=cur.fetchone()
    if result:
       print('-'*5,"login successfully",'-'*5)
       admin_page()
    else:
       print('-'*5,"invalid credentials",'-'*5)


def user_register():
    print(space*10, 'USER REGISTRATION', space*10)

    # Validate username (only alphabets)
    while True:
        user_name = input("Enter your Name: ")
        if re.match(r'^[A-Za-z]+$', user_name):
            break
        else:
            print(' Error: Name must contain only letters. Try again.')

    # Validate mobile number (only digits, exactly 10 digits)
    while True:
        user_mobileno = input("Enter your Mobile Number: ")
        if re.match(r'^[0-9]{10}$', user_mobileno):
            user_mobileno = int(user_mobileno)
            break
        else:
            print("Error: Mobile number must be 10 digits. Try again.")

    # Check if user already exists
    cur.execute("SELECT user_id FROM user WHERE user_name=%s AND user_mobileno=%s",
                (user_name, user_mobileno))
    result = cur.fetchone()

    if result:
        print('-' * 5, "User already exists", '-' * 5)
    else:
        cur.execute("INSERT INTO user(user_name, user_mobileno) VALUES (%s, %s)",
                     (user_name, user_mobileno))
        con.commit()

        print('-' * 5, "Registration completed", '-' * 5)
        
        cur.execute("SELECT user_id FROM user WHERE user_name=%s AND user_mobileno=%s",
                    (user_name, user_mobileno))
        new_id = cur.fetchone()[0]
        print(f" Your user_id is: {new_id}")

#------------------ user login -------------------------------------------------  
def user_login():
    print(space*10,'User Login',space*10)
    user_name=input("Enter Name: ")
    user_mobileno=int(input('Enter Mobile: '))
    cur.execute('select * from user where user_name=%s and user_mobileno=%s',(user_name,user_mobileno))
    user=cur.fetchone()
    
    if user:
        
        print(f' Welcome {user_name}')
        return user[0]
        
    else:
        print('-'*5,"Invalid credentials",'-'*5)
        

#---------------menu--------------------------#
        
while True:
    print('1. Admin login')
    print()
    print('2. User Registration')
    print()
    print('3.User Login')
    print()
    print('4.Exit')
    print()
    choice=input('choose the option : ')
    
    if choice=='1':
        admin_login()
        
    elif choice=='2':
        user_register()
        
    elif choice=='3':
        user_id = user_login()
        if user_id:
             while True:
                print('-'*6,'User Menu','-'*6)
                print("1. Add to Cart")
                print("2. View Cart")
                print("3. Modify Cart")
                print("4. Generate Bill")
                print("5. Exit")
                choice = input("Choose option: ")

                if choice == '1':
                    while True:
                        print('-'*20, 'Menu','-'*20)
                        menu_type=input("Enter your menu type (veg/nonveg/drinks/rotties) or exit: ")
                        if menu_type=='exit':
                            break
                        elif menu_type in ['veg','nonveg','drinks','rotties']:
                            if menu_type=='veg':
                                veg_orders()
                                add_to_cart(user_id,menu_type)
                            elif menu_type=='nonveg':
                                
                                nonveg_orders()
                                add_to_cart(user_id,menu_type)
                            elif menu_type=='drinks':
                                
                                cool_drinks()
                                add_to_cart(user_id,menu_type)
                            elif menu_type=='rotties':
                                
                                rotties()
                                add_to_cart(user_id,menu_type)
                                                        
                        else:
                            print('-'*5,"Invalid menu type",'-'*5)
                        
                        
                elif choice == '2':
                    view_cart(user_id)
                elif choice =='3':
                    modify_cart(user_id)
                elif choice =='4':
                    generate_bill(user_id)
                elif choice == '5':
                    print('-'*5," Exiting... Have a nice day!",'-'*5)
                    break

                  
cur.close()
con.close()


#cur.execute('desc admin')
#data=cur.fetchall()
#print(data)



