import pyodbc
from datetime import datetime
#################################################################
# Connect to database
conn = pyodbc.connect('driver={SQL Server};Server=cypress.csil.sfu.ca;user=s_yixuy; password=LL6afNRYgF2mnNQE;Trusted_Connection=yes;')
# create a cursor
c = conn.cursor()
#create the table
print("Connection Successfully Established")
#################################################################
# Searching result
def search(minPrice,maxPrice,number,start,end,days):
    sqlselect =('''SELECT L.id, L.name,LEFT (L.description, 25), L.number_of_bedrooms, SUM(C.price)
                   FROM Calendar C, Listings L
                   WhERE L.id = C.listing_id
                       and C.available = 1
                       and C.price >= ?
                       and C.price <= ?
                       and L.number_of_bedrooms = ?
                       and C.date >= ?
                       and C.date < ?
                   GROUP BY L.id, L.name,LEFT (L.description, 25), L.number_of_bedrooms
                   Having COUNT(L.id) = ?''')
    searchValue = [minPrice,maxPrice,number,start,end,days]
    SearchList = [] 
    c.execute( sqlselect ,searchValue)
    row = c.fetchone()
    if not row :
        print("Nothing got searched")
        return
    print("\n________________________Result for Searching________________________")
    while row:
        SearchList.append(row[0])
        print  ("id: %d\nhotel name: %s\ndescription: %s             \nnumber_of_bedrooms: %d\ntotal price: %.2f\n" %(row[0], row [1], row[2], row[3], row[4]))
        print("--------------------------------------------------------------------")
        row = c.fetchone()
    print("_________________________Searching done_________________________\n")
                    
    goingtobooking= input("Would you like to book in the searching result(y/n)")
    if goingtobooking == 'y':
        booking(SearchList,start,end)
    else:
        print("Searching done but nothing booked\n")
        
    
  
##########################################  
#Booking 
def booking(SearchList,start,end):
    sqlinsert = ("INSERT INTO Bookings(id, listing_id, guest_name, stay_from, stay_to, number_of_guests) VALUES (?,?,?,?,?,?)") 
    sqlbooking = ('''SELECT COUNT (*)as bid FROM BookingS ''')

    value = 1
    while value:
        # book list id 
        listid = int(input ("Which id would you like to order:"))
        if listid not in SearchList:
            print ("Invalid input of list id, try another one\n")
        else:
            ans = input("Would you like to order this one(y/n)")
            if  ans =='n':
                print(" NOT Booking anything, thank you!")
                return
            # booking id
            c.execute(sqlbooking)
            bid = c.fetchone().bid+1
            # guest name
            guestname = input("please enter your name:")
            # number of guests
            guestnum = input("please enter how many people you have:")
            Book = [bid,listid,guestname,start,end,guestnum]
            c.execute(sqlinsert, Book)
            print("Booking complete! Thank you! \n")
            value = 0
            c.commit()
##########################################
#Writing a review
def writing ():
    sqlsearchingusername = ('''SELECT *
                               FROM Bookings B
                               WHERE B.guest_name = ?''')
    guestname = input("please enter your name to find your order:")
    c.execute(sqlsearchingusername,guestname)
    sList=[]
    row = c.fetchone()
    if not row :
        print("No Booking result for %s" %(guestname))
        return
    
    print("\n________________________Result for %s ________________________" %(guestname))
    while row:
        sList.append(row[0])
        print("id: %d\nlisting id: %d\n%s ----> %s\nnumber of guests: %d\n" %(row[0], row[1], row[3], row[4],row[5]))
        print("--------------------------------------------------------------------")
        row = c.fetchone()
    print("_________________________________________________________________")

    goingtoreview= input("Would you like to writing a review in the searching result(y/n)")
    if goingtoreview == 'y':
        review(sList, guestname) 
    else:
        print("Searching done but nothing to write a comment\n")
#################################################################
def review(sList, guestname):
    sqlcomment = ('''INSERT INTO Reviews(id, listing_id, comments,guest_name) VALUES (?,?,?,?)''')
    findListingID = ('''SELECT  listing_id FROM Bookings WHERE id = ? ''')
    
    
    c.execute("SELECT COUNT(*) AS rid FROM Reviews")
    rid = c.fetchone().rid + 1

    
    bid = int(input ("Which id  would you like to make a comment:"))
    if bid not in sList:
        print ("Invalid input of booking id, try another one\n")
    else:
        Lid = c.execute(findListingID, bid)
        Lid = c.fetchone()[0]

        comment = str(input ("Please enter a review :"))
        com = [rid,Lid,comment,guestname]
        try:
            c.execute(sqlcomment,com)
            c.commit()
            print("\nWriting review is completed")
        except pyodbc.Error as err:
            print(err)
            print("\nWriting review is not completed")
#################################################################
#main
print("Welcome to Airbnb! Order the room you want!")
print("1.Search Listings 2.Book Listing 3.Write Review 4.Quit")
fun=int(input("Which one would you like to do:"))
while fun != 4:
    if fun == 1:
        minPrice=input("Please Enter the min price(>=0):")
        maxPrice=input("Please Enter the max price(>0 and it should be bigger than min price):")
        if(int(minPrice) - int(maxPrice) > 0):
            print("Invalid price range, please try again!\n")
            break
        number  =input("Please Enter the number of bedroom(>0):")
        start= input("Please Enter the start date(yyyy-mm-dd):")
        end= input("Please Enter the end date(yyyy-mm-dd):")
        start_obj = datetime.strptime(start, '%Y-%m-%d')
        end_obj = datetime.strptime(end, '%Y-%m-%d')
        days =  (end_obj - start_obj ).days
        if(days < 0):
            print('Invalid input date')
            break 
        search(minPrice,maxPrice,number,start,end, days)
    if fun == 2:
        print("Sorry, you need to go the Search Listings first\n")
    if fun == 3:
        writing ()
    if fun == 4:
        break
    print("1.Search Listings 2.Book Listing 3.Write Review 4. Quit")
    fun=int(input("Which one would you like to do:"))

print("Thank you for using Airbnb :) Having a great day! ")

conn.close()
print("Connection closed")
# close connection



