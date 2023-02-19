# This program allows the user to manage an inventory of books at a bookstore. 
# It uses the spaCy library for language models that enable the user to search the database for similar books.
# It use SQLite to store the invnetory in a database. 


import spacy, sqlite3
nlp = spacy.load('en_core_web_md')
db = sqlite3.connect('./ebookstore')
cursor = db.cursor()


#==========Functions==============
def create_db():    # sets up the db as per assignment 
    try:
        cursor.execute('''DROP TABLE books''')
    except Exception:
        pass

    # create table with ID and Title as primary key 
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        Title TEXT,
        Author TEXT,
        Qty INTEGER
        )
    ''')
    db.commit()

    books_ = [(3001, 'A Tale of Two Cities', 'Charles Dickens', 30), 
        (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40), 
        (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25), 
        (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37), 
        (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)]

    # uppercase for text values in table
    for book in books_:
        book_list = list(book)
        book_list[1] = str(book_list[1]).upper()
        book_list[2] = str(book_list[2]).upper()
        books_[books_.index(book)] = tuple(book_list)


    cursor.executemany('''INSERT INTO books
        VALUES (?,?,?,?)
        ''', books_
    )
    db.commit()
    return


def enter_book():
    # user to enter name of author
    author = input("Enter the author's full name: ").upper()
    
    # brings up table of books by author last name if it exists
    cursor.execute('''SELECT * FROM books WHERE Author = ?''', (author,))
    
    if cursor.fetchone() is not None:
        print("Book(s) by this author are in the database:")
        cursor.execute('''SELECT * FROM books WHERE Author = ?''', (author,))
        for row in cursor:
            print('id {0} - "{1}" by {2}. Qty: {3}'.format(row[0],row[1],row[2],row[3]))
        
        # user to confirm if entry continues
        add = 99 
        while add == 99:
            carry_on = input("Continue to add new book? Y/N").upper()
            if carry_on == 'Y':
                add = 1
            elif carry_on == 'N':
                add = 0
            else:
                print("Invalid input. Try again.")
    else:
        add = 1

    if add == 1:
        # user inputs for new record 
        carry_on = True
        while carry_on:
            try:
                new_id = int(input("Enter new id: "))
                # check if id already exists
                cursor.execute('''SELECT * FROM books WHERE id = ?''', (new_id,))
                if cursor.fetchone() is not None:
                    print("Id already exists. Use a different id.")
                else:
                    carry_on = False
            except ValueError:
                print("Input not an integer. Try again.")
        
        carry_on = True
        while carry_on:
            try:
                qty = int(input("Enter quantity of book(s): "))
                carry_on = False
            except ValueError:
                print("Input not an integer. Try again.")

        title = input("Enter new title: ").upper()

        # adding to db
        cursor.execute('''INSERT INTO books (id, Title, Author, Qty) VALUES (?,?,?,?)''', (new_id, title, author, qty))
        db.commit()
        print("New record added!")
    return


def update_book():
    print("--- Books in the database ---")
    cursor.execute('''SELECT * FROM books''')
    for row in cursor:
            print('id {0} - "{1}" by {2}. Qty: {3}'.format(row[0],row[1],row[2],row[3]))
    
    # select id to update
    carry_on = True
    while carry_on:
        try:
            id = int(input("Enter id of book to update: "))
            cursor.execute('''SELECT * FROM books WHERE id = ?''', (id,))
            if cursor.fetchone() is None:
                print("Id does not exist. Try again.")
            else:
                carry_on = False
        except ValueError:
            print("Input not an integer. Try again.")

    # select field to update
    loop = True
    while loop:
        field = input('''Select field to update:
            i - Id
            t - Title
            a - Author
            q - Quantity
            e - Exit
        ''').lower()

        if field == 'i':
            carry_on = True
            while carry_on:
                try:
                    new_id = int(input("Enter new id: "))
                    # check if id already exists
                    cursor.execute('''SELECT * FROM books WHERE id = ?''', (new_id,))
                    if cursor.fetchone() is not None:
                        print("Id already exists. Use a different id.")
                    else:
                        carry_on = False
                except ValueError:
                    print("Input not an integer. Try again.")
            cursor.execute('''UPDATE books SET id = ? WHERE id = ?''', (new_id, id))
            db.commit()

            print("Id updated!")
            loop = False

        elif field == 't':
            new_title = input("Enter new title: ").upper()
            cursor.execute('''UPDATE books SET Title = ? WHERE id = ?''', (new_title, id))
            db.commit()

            print("Title updated!")
            loop = False
        elif field == 'a':
            new_author = input("Enter new author: ").upper()
            cursor.execute('''UPDATE books SET Author = ? WHERE id = ?''', (new_author, id))
            db.commit()

            print("Author updated!")
            loop = False
        elif field == 'q':
            carry_on = True
            while carry_on:
                try:
                    new_qty = int(input("Enter new quantity: "))
                    carry_on = False
                except ValueError:
                    print("Input not an integer. Try again.")
            cursor.execute('''UPDATE books SET Qty = ? WHERE id = ?''', (new_qty, id))
            db.commit()

            print("Quantity updated!")
            loop = False
        elif field == 'e':
            loop = False
        else:
            print('Invalid entry. Try again')
    return


def delete_book():
    print("--- Books in the database ---")
    cursor.execute('''SELECT * FROM books''')
    for row in cursor:
            print('id {0} - "{1}" by {2}. Qty: {3}'.format(row[0],row[1],row[2],row[3]))
    
    # select id to delete
    carry_on = True
    while carry_on:
        try:
            id = int(input("Enter id of book to delete: "))
            cursor.execute('''SELECT * FROM books WHERE id = ?''', (id,))
            if cursor.fetchone() is None:
                print("Id does not exist. Try again.")
            else:
                carry_on = False
        except ValueError:
            print("Input not an integer. Try again.")

    cursor.execute('''DELETE FROM books WHERE id =?''', (id,))
    db.commit()
    print("Record deleted!")
    return


def search_books():
    # search description by title and author
    title_input = input("Enter book title: ").upper()
    author_input = input("Enter author's full name: ").upper()
    input_tuple = (title_input, author_input)
    search_desc = title_input + ' ' + author_input 

    # database extract into list
    book_list = []
    cursor.execute('''SELECT Title, Author FROM books''')
    for row in cursor:
        book_list.append(row)

    if input_tuple in book_list:
        print("The book is in the database.")

    else:
        # change tuples into string items in list
        book_str = []
        for book in book_list:
            book_L = list(book)
            book_L = ' '.join(book_L)
            book_str.append(book_L)

        # use nlp to find highest similarity match
        similarity_list = []
        search_desc = nlp(search_desc)
        for book in book_str:
            book_desc = nlp(book)
            similarity_list.append(search_desc.similarity(book_desc))

        # search result
        book_index = similarity_list.index(max(similarity_list))   # book description with the highest similarity
        searched_book = book_list[book_index]
        print(f"The book is not in the database. The closest search was \"{searched_book[0]}\" by {searched_book[1]}.")
    return


#==========Main Menu=============

create_db()

choice = ""

while choice != "0":
    choice = input(f'''
    What would you like to do:
        1. Enter book
        2. Update book 
        3. Delete book 
        4. Search books 
        0. Exit
    ''').strip().lower()

    if choice == "1":
        enter_book()
    
    elif choice == "2":
        update_book()

    elif choice == "3":
        delete_book()

    elif choice == "4":
        search_books()

    elif choice == "0":
        db.close()
        print("Goodbye!")
        exit()

    else:
        print("Invalid entry. Try again.")
