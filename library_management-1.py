import datetime


###################
## Book class

class Book:
    def __init__(self, book_id, title, author, genre, availability=True):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.availability = availability
        self.borrow_count = 0  # To track borrow count
        self.due_date = None  # To store due date

    def __str__(self):
        # Display 'N/A' if due_date is None, otherwise display the due date
        due_date_str = self.due_date.strftime("%Y-%m-%d") if self.due_date else "N/A"
        return f"{self.book_id}: {self.title} by {self.author} (Due: {due_date_str})"


###################
## Member class

class Member:
    def __init__(self, member_id, name, borrowed_books=None):
        if borrowed_books is None:
            borrowed_books = []
        self.member_id = member_id
        self.name = name
        self.borrowed_books = borrowed_books

    def borrow_book(self, book):
        self.borrowed_books.append(book)
        book.borrow_count += 1  # Increment borrow count

    def return_book(self, book):
        self.borrowed_books.remove(book)

    def __str__(self):
        borrowed_books_str = ', '.join([book.book_id for book in self.borrowed_books])
        return f"{self.member_id},{self.name},{borrowed_books_str}"


###################
## Library class to manage operations

class Library:
    def __init__(self):
        self.books = {}
        self.members = {}
        self.member_id_counter = 1
        self.book_id_counter = 1

    ###################
    ## Book Management

    def load_books(self, book_data_file='books.txt'):
        try:
            with open(book_data_file, 'r') as file:
                for line in file:
                    book_id, title, author, genre, availability = line.strip().split(',')
                    availability = availability == 'True'
                    self.books[book_id] = Book(book_id, title, author, genre, availability)
            print("Books loaded successfully.")
        except FileNotFoundError:
            print(f"Error: {book_data_file} not found.")
        except Exception as e:
            print(f"Error loading books: {e}")

    def save_books(self, book_data_file='books.txt'):
        try:
            with open(book_data_file, 'w') as file:
                for book in self.books.values():
                    file.write(f"{book.book_id},{book.title},{book.author},{book.genre},{book.availability}\n")
            print("Books saved successfully.")
        except Exception as e:
            print(f"Error saving books: {e}")

    def generate_unique_book_id(self):
        while True:
            new_id = f"B{self.book_id_counter:03d}"
            if new_id not in self.books:
                return new_id
            self.book_id_counter += 1

    def add_book(self, title, author, genre):
        new_book_id = self.generate_unique_book_id()
        new_book = Book(new_book_id, title, author, genre)
        self.books[new_book_id] = new_book
        self.book_id_counter += 1
        print(f"Book '{new_book.title}' added successfully with ID: {new_book_id}.")

    def update_book(self, book_id, title=None, author=None, genre=None):
        book = self.books.get(book_id)
        if book:
            if title:
                book.title = title
            if author:
                book.author = author
            if genre:
                book.genre = genre
            print(f"Book '{book_id}' updated successfully.")
        else:
            print("Error: Book not found.")

    def remove_book(self, book_id):
        if book_id in self.books:
            removed_book = self.books.pop(book_id)
            print(f"Book '{removed_book.title}' removed from the library.")
        else:
            print("Error: Book not found.")

    def show_available_books(self):
        available_books = [book for book in self.books.values() if book.availability]
        if available_books:
            print("\nAvailable Books:")
            for book in available_books:
                print(f"{book}")
        else:
            print("No books available for borrowing.")

    def show_unavailable_books(self):
        unavailable_books = [book for book in self.books.values() if not book.availability]
        if unavailable_books:
            print("\nUnavailable (Borrowed) Books:")
            for book in unavailable_books:
                print(f"{book}")
        else:
            print("All books are available.")

    ###################
    ## Member Management

    def load_members(self, member_data_file='members.txt'):
        try:
            with open(member_data_file, 'r') as file:
                for line in file:
                    # Split by comma but limit to 3 splits (ID, Name, Borrowed Books)
                    parts = line.strip().split(',', 2)

                    # Ensure we have exactly 3 parts: ID, Name, and Borrowed Books
                    if len(parts) != 3:
                        print(f"Error: Incorrect format in member data: {line}")
                        continue

                    member_id, name, borrowed_books_str = parts
                    borrowed_books_list = borrowed_books_str.split(',') if borrowed_books_str else []

                    # Create a new Member object
                    member_obj = Member(member_id, name)

                    # Add borrowed books to the member if any
                    for book_id in borrowed_books_list:
                        if book_id in self.books:
                            member_obj.borrow_book(self.books[book_id])

                    # Add the member to the members dictionary
                    self.members[member_id] = member_obj

            print("Members loaded successfully.")
        except FileNotFoundError:
            print(f"Error: {member_data_file} not found.")
        except Exception as e:
            print(f"Error loading members: {e}")

    def save_members(self, member_data_file='members.txt'):
        try:
            with open(member_data_file, 'w') as file:
                for member in self.members.values():
                    file.write(f"{member}\n")
            print("Members saved successfully.")
        except Exception as e:
            print(f"Error saving members: {e}")

    def generate_unique_member_id(self):
        while True:
            new_id = f"M{self.member_id_counter:03d}"
            if new_id not in self.members:
                return new_id
            self.member_id_counter += 1

    def register_new_member(self, name):
        new_member_id = self.generate_unique_member_id()
        new_member = Member(new_member_id, name)
        self.members[new_member_id] = new_member
        self.member_id_counter += 1
        print(f"Member '{name}' registered successfully with ID: {new_member_id}.")

    def update_member(self, member_id, name=None):
        member = self.members.get(member_id)
        if member:
            if name:
                member.name = name
            print(f"Member '{member_id}' updated successfully.")
        else:
            print("Error: Member not found.")

    def remove_member(self, member_id):
        if member_id in self.members:
            removed_member = self.members.pop(member_id)
            print(f"Member '{removed_member.name}' removed from the library.")
        else:
            print("Error: Member not found.")

    ###################
    ## Borrowing and Returning Books

    def borrow_book(self, member_id, book_id):
        member = self.members.get(member_id)
        book = self.books.get(book_id)

        if not member:
            print("Error: Member not found.")
            return

        if not book:
            print("Error: Book not found.")
            return

        if not book.availability:
            print(f"Book '{book.title}' is currently unavailable.")
            return

        # Set the book as unavailable and calculate the due date
        book.availability = False
        book.due_date = datetime.datetime.now() + datetime.timedelta(days=2)  # Set due date for 2 weeks
        member.borrow_book(book)
        print(f"Member '{member.name}' borrowed book '{book.title}'. Due date is {book.due_date.strftime('%Y-%m-%d')}.")

    def return_book(self, member_id, book_id):
        # Print out the member IDs to verify if the member exists
        print(f"Current Members: {list(self.members.keys())}")

        member = self.members.get(member_id)
        book = self.books.get(book_id)

        if not member:
            print("Error: Member not found.")
            return

        if not book:
            print("Error: Book not found.")
            return

        if book not in member.borrowed_books:
            print(f"Error: Member '{member.name}' did not borrow book '{book.title}'.")
            return

        # Set the book as available and reset the due date upon return
        book.availability = True
        book.due_date = None  # Reset due date
        member.return_book(book)
        print(f"Member '{member.name}' returned book '{book.title}'.")

    ###################
    ## Reporting

    def list_borrowed_books(self):
        print("\nBorrowed Books with Due Dates:")
        for member in self.members.values():
            for book in member.borrowed_books:
                print(f"{book}")

    def list_overdue_books(self):
        print("\nOverdue Books:")
        today = datetime.datetime.now()
        overdue_books = [book for book in self.books.values() if not book.availability and book.due_date < today]

        if overdue_books:
            for book in overdue_books:
                print(f"{book.title} by {book.author} (Due: {book.due_date.strftime('%Y-%m-%d')})")
        else:
            print("No overdue books.")

    def most_popular_books(self):
        if not self.books:
            print("No books available.")
            return

        most_common = [(book, book.borrow_count) for book in self.books.values() if book.borrow_count > 0]
        most_common.sort(key=lambda x: x[1], reverse=True)

        if not most_common:
            print("No books have been borrowed yet.")
            return

        print("\nMost Popular Books:")
        for book, count in most_common[:5]:  # Display top 5
            print(f"{book.title} by {book.author} (Borrowed: {count} times)")


###################
## Main Function

def main():
    library_system = Library()

    # Load existing data
    library_system.load_books()
    library_system.load_members()

    # Main menu loop
    while True:
        print("\nLibrary Management Menu:")
        print("1. Add Book")
        print("2. Update Book")
        print("3. Remove Book")
        print("4. Register New Member")
        print("5. Update Member")
        print("6. Remove Member")
        print("7. Show Available Books")
        print("8. Show Unavailable Books")
        print("9. Borrow Book")
        print("10. Return Book")
        print("11. List Borrowed Books with Due Dates")
        print("12. List Overdue Books")
        print("13. Most Popular Books")
        print("14. Save and Exit")

        choice = input("Enter your choice (1-14): ")

        try:
            if choice == '1':
                title = input("Enter Book Title: ")
                author = input("Enter Book Author: ")
                genre = input("Enter Book Genre: ")
                library_system.add_book(title, author, genre)

            elif choice == '2':
                book_id = input("Enter Book ID to update: ")
                title = input("Enter new title (or leave blank): ")
                author = input("Enter new author (or leave blank): ")
                genre = input("Enter new genre (or leave blank): ")
                library_system.update_book(book_id, title or None, author or None, genre or None)

            elif choice == '3':
                book_id = input("Enter Book ID to remove: ")
                library_system.remove_book(book_id)

            elif choice == '4':
                name = input("Enter Member Name: ")
                library_system.register_new_member(name)

            elif choice == '5':
                member_id = input("Enter Member ID to update: ")
                name = input("Enter new member name (or leave blank): ")
                library_system.update_member(member_id, name or None)

            elif choice == '6':
                member_id = input("Enter Member ID to remove: ")
                library_system.remove_member(member_id)

            elif choice == '7':
                library_system.show_available_books()

            elif choice == '8':
                library_system.show_unavailable_books()

            elif choice == '9':
                member_id = input("Enter Member ID: ")
                book_id = input("Enter Book ID to borrow: ")
                library_system.borrow_book(member_id, book_id)

            elif choice == '10':
                member_id = input("Enter Member ID: ")
                book_id = input("Enter Book ID to return: ")
                library_system.return_book(member_id, book_id)

            elif choice == '11':
                library_system.list_borrowed_books()

            elif choice == '12':
                library_system.list_overdue_books()

            elif choice == '13':
                library_system.most_popular_books()

            elif choice == '14':
                library_system.save_books()
                library_system.save_members()
                print("Library data saved. Exiting the program.")
                break

            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            print(f"An error occurred: {e}")


# Run the main function when the script is executed
if __name__ == "__main__":
    main()
