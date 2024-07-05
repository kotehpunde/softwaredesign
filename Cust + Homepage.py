from tkinter import *
from tkinter import messagebox, filedialog
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
from tkinter import scrolledtext, font
from tkinter import messagebox
from fpdf import FPDF


def open_customer_login():
    root = Tk()
    root.title("Food Management System")
    root.geometry("1920x1080+0+0")
    root.config(bg="beige")

    # Database setup
    conn = sqlite3.connect('food_database.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                      user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT NOT NULL UNIQUE,
                      password TEXT NOT NULL,
                      firstname TEXT NOT NULL,
                      lastname TEXT NOT NULL,
                      photo BLOB)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS food (
                      food_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      food_name TEXT NOT NULL,
                      description TEXT NOT NULL,
                      price REAL NOT NULL)''')

    # Variables
    USERNAME_LOGIN = StringVar()
    PASSWORD_LOGIN = StringVar()
    USERNAME_REGISTER = StringVar()
    PASSWORD_REGISTER = StringVar()
    FIRSTNAME = StringVar()
    LASTNAME = StringVar()
    PHOTO_PATH = StringVar()

    # Functions
    def Login():
        username = USERNAME_LOGIN.get()
        password = PASSWORD_LOGIN.get()

        if username and password:
            cursor.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            if user:
                messagebox.showinfo("Success", f"Welcome {username}!")
                ShowFoodWindow()

            else:
                messagebox.showerror("Error", "Invalid username or password")
        else:
            messagebox.showerror("Error", "Please enter username and password")

    def Register():
        username = USERNAME_REGISTER.get()
        password = PASSWORD_REGISTER.get()
        firstname = FIRSTNAME.get()
        lastname = LASTNAME.get()
        photo_path = PHOTO_PATH.get()

        if username and password and firstname and lastname and photo_path:
            try:
                with open(photo_path, 'rb') as file:
                    photo = file.read()
                    if not photo:
                        raise ValueError("Photo file is empty or cannot be read")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read photo file: {e}")
                return

            try:
                cursor.execute(
                    "INSERT INTO user (username, password, firstname, lastname, photo) VALUES (?, ?, ?, ?, ?)",
                    (username, password, firstname, lastname, photo))
                conn.commit()
                messagebox.showinfo("Success", "Registration successful!")
                LoginForm()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already taken")
            except Exception as e:
                messagebox.showerror("Error", f"Database error: {e}")
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def upload_photo():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            PHOTO_PATH.set(file_path)
            messagebox.showinfo("Photo selected", f"Selected photo: {file_path}")

    def LoginForm():
        clear_frame()
        Label(root, text="Login", font=("Ink Free", 40), bg="beige").pack()
        Label(root, text="Username",font=("Times New Romans", 20), bg="beige").pack()
        Entry(root, textvariable=USERNAME_LOGIN, font=15).pack()
        Label(root, text="Password",font=("Times New Romans", 20), bg="beige").pack()
        Entry(root, textvariable=PASSWORD_LOGIN, font=15, show='*').pack()
        Button(root, text="Login",bg="Black", fg="White",font=("Times New Romans", 15), command=Login).pack()
        Button(root, text="Go to Register",bg="Black", fg="White",font=("Times New Romans", 15), command=RegisterForm).pack()

    def RegisterForm():
        clear_frame()
        Label(root, text="Register", font=("Ink Free", 40), bg="beige").pack()
        Label(root, text="Username",font=("Times New Romans", 20), bg="beige").pack()
        Entry(root, textvariable=USERNAME_REGISTER, font=15).pack()
        Label(root, text="Password",font=("Times New Romans", 20), bg="beige").pack()
        Entry(root, textvariable=PASSWORD_REGISTER, font=15, show='*').pack()
        Label(root, text="First Name",font=("Times New Romans", 20), bg="beige").pack()
        Entry(root, textvariable=FIRSTNAME,font=15).pack()
        Label(root, text="Last Name",font=("Times New Romans", 20), bg="beige").pack()
        Entry(root, textvariable=LASTNAME, font=15).pack()
        Label(root, text="Photo",font=("Times New Romans", 20), bg="beige").pack()
        Button(root, text="Upload Photo",bg="Black", fg="White",font=("Times New Romans", 15), command=upload_photo).pack()
        Label(root, textvariable=PHOTO_PATH,font=("Times New Romans", 20), bg="beige").pack()
        Button(root, text="Register",bg="Black", fg="White",font=("Times New Romans", 15), command=Register).pack()
        Button(root, text="Go to Login",bg="Black", fg="White",font=("Times New Romans", 15), command=LoginForm).pack()

    def ShowFoodWindow():
        def show_menu():
            menu_window = tk.Toplevel()
            app = FoodOrderingSystem(menu_window)

        # Function to display the review system
        def show_review():
            review_window = tk.Toplevel()
            review_system = ReviewSystem()
            app = ReviewApp(review_window, review_system)

        def show_customer_support():
            # Create a new top-level window for customer support
            support_window = tk.Toplevel(root)
            support_window.title("Customer Service Chatbot")
            support_window.geometry("500x600")

            def get_bot_response(user_input):
                user_input = user_input.lower().strip()

                responses = {
                    "hi": "Hello! How can I help you today?",
                    "hello": "Hello! How can I assist you?",
                    "what are your hours?": "Our hours are 10 AM to 10 PM, Monday through Sunday.",
                    "how can i order food?": "You can order food through the 'Menu' section in the home page.",
                    "what is your refund policy?": "You can request a refund within 24 hours of your order if you are not satisfied.",
                    "how do i contact customer service?": "You can contact our customer service through calling 0182738163.",
                    "where is my order?": "You can check the status of your order in the 'Orders' section. If there's an issue, please contact customer service.",
                    "how do i cancel my order?": "You can cancel your order within 15 minutes of placing it through the 'Cart' section in the app."
                }

                return responses.get(user_input,
                                     "I'm sorry, I don't understand your question. Please contact customer service for more assistance.")

            def send_message(event=None):
                user_input = user_entry.get()
                if user_input:
                    chat_display.configure(state='normal')
                    chat_display.insert(tk.END, f"You: {user_input}\n", 'user')
                    user_entry.delete(0, tk.END)

                    bot_response = get_bot_response(user_input)
                    chat_display.insert(tk.END, f"Bot: {bot_response}\n", 'bot')
                    chat_display.configure(state='disabled')
                    chat_display.yview(tk.END)

            header_font = font.Font(family="Helvetica", size=14, weight="bold")
            text_font = font.Font(family="Arial", size=12)

            header_frame = tk.Frame(support_window, bg='#ff5722')
            header_frame.pack(fill=tk.X)
            header_label = tk.Label(header_frame, text="Customer Service Chatbot", bg='#ff5722', fg='white',
                                    font=header_font,
                                    pady=10)
            header_label.pack()

            chat_display = scrolledtext.ScrolledText(support_window, state='disabled', wrap=tk.WORD, font=text_font,
                                                     bg='white',
                                                     fg='black')
            chat_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
            chat_display.tag_configure('user', foreground='#0b5394', font=('Arial', 12, 'bold'))
            chat_display.tag_configure('bot', foreground='#a4c639', font=('Arial', 12))

            input_frame = tk.Frame(support_window, bg='#f8f8f8')
            input_frame.pack(fill=tk.X, pady=5, padx=10)

            user_entry = tk.Entry(input_frame, font=text_font, bg='white', fg='black', bd=2, relief=tk.GROOVE)
            user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
            user_entry.bind('<Return>', send_message)

            send_button = tk.Button(input_frame, text="Send", font=header_font, bg='#ff5722', fg='white', bd=2,
                                    relief=tk.RAISED,
                                    command=send_message)
            send_button.pack(side=tk.RIGHT)

            root.mainloop()

        class FoodOrderingSystem:
            def __init__(self, root):
                self.root = root
                self.root.title("Food Ordering System")
                self.root.geometry("800x600")
                self.root.config(bg="#f8f8f8")

                self.label = tk.Label(root, text="Menu", font=("Arial", 24), bg="pink")
                self.label.pack(pady=10)

                self.category_frame = tk.Frame(root, bg="#f8f8f8")
                self.category_frame.pack(side=tk.TOP, fill=tk.X)

                self.menu_container = tk.Frame(root, bg="#f8f8f8")
                self.menu_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

                self.scrollbar = tk.Scrollbar(self.menu_container, orient=tk.HORIZONTAL)
                self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

                self.canvas = tk.Canvas(self.menu_container, bg="#f8f8f8", xscrollcommand=self.scrollbar.set)
                self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

                self.scrollbar.config(command=self.canvas.xview)

                self.menu_inner_frame = tk.Frame(self.canvas, bg="#f8f8f8")
                self.canvas.create_window((0, 0), window=self.menu_inner_frame, anchor="nw")

                self.menu_items = [
                    {"name": "Pasta", "price": 29, "description": "Cheesy pasta with toppings.",
                     "image_path": "Images/pasta.jpeg", "category": "Main"},
                    {"name": "Americano", "price": 9, "description": "Something good to help stay alive.",
                     "image_path": "Images/americano.jpeg", "category": "Drinks"},
                    {"name": "Cake", "price": 18, "description": "Pistachio cake.",
                     "image_path": "Images/cake.jpeg", "category": "Desserts"},
                    {"name": "Cookies", "price": 8, "description": "New York cookies.",
                     "image_path": "images/cookie.jpeg", "category": "Desserts"},
                    {"name": "Waffles", "price": 13, "description": "Waffles with honey toppings.",
                     "image_path": "images/waffle.jpeg", "category": "Desserts"},
                    {"name": "Ice Cream", "price": 11, "description": "Homemade mint vanilla icecream.",
                     "image_path": "images/icecream.jpeg", "category": "Desserts"},
                    {"name": "Sorbet", "price": 13, "description": "Special-made sorbet icecream.",
                     "image_path": "images/sorbet.jpeg", "category": "Desserts"},
                    {"name": "Pie", "price": 16, "description": "Icecream pie",
                     "image_path": "images/pie.jpeg", "category": "Desserts"},
                    {"name": "Lamb Stick", "price": 33, "description": "Lamb stick with eggs.",
                     "image_path": "images/lambstick.jpeg", "category": "Main"},
                    {"name": "Quinoa", "price": 26, "description": "'Rice' with apple.",
                     "image_path": "images/quinoa.jpeg", "category": "Main"},
                    {"name": "Burger", "price": 29, "description": "HUGE burger with exclusive patty.",
                     "image_path": "images/burger.jpeg", "category": "Main"},
                    {"name": "Latte", "price": 13, "description": "Coffee with milk.",
                     "image_path": "images/latte.jpeg", "category": "Drinks"},
                    {"name": "Apple Soda", "price": 16, "description": "Sparking apple juice.",
                     "image_path": "images/applesoda.jpeg", "category": "Drinks"},
                    {"name": "Fries", "price": 13, "description": "Cheezy Fries.",
                     "image_path": "images/fries.jpeg", "category": "Snacks"}
                ]

                self.order_quantities = {}
                self.order_remarks = {}
                self.cart_items = {}

                self.category_buttons = {}
                categories = ["Main", "Drinks", "Desserts", "Snacks"]

                for category in categories:
                    button = tk.Button(self.category_frame, text=category, font=("Arial", 16), bg="#ff5722", fg="white",
                                       command=lambda c=category: self.show_category(c))
                    button.pack(side=tk.LEFT, padx=10)
                    self.category_buttons[category] = button

                self.menu_items_widgets = []

                for item_index, item in enumerate(self.menu_items):
                    if os.path.isfile(item["image_path"]):
                        self.create_menu_item(item, item_index)

                self.view_cart_button = tk.Button(root, text="View Cart", font=("Arial", 16), bg="#4CAF50", fg="white",
                                                  command=self.view_cart)
                self.view_cart_button.pack(pady=20)

                self.update_menu_layout()

            def create_menu_item(self, item, item_index):
                frame = tk.Frame(self.menu_inner_frame, bg="white", bd=2, relief="groove")
                frame.grid(row=item_index // 10, column=item_index % 10, padx=30, pady=30)

                img = Image.open(item["image_path"])
                img = img.resize((200, 200), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)

                img_label = tk.Label(frame, image=photo, bg="white")
                img_label.image = photo
                img_label.pack(pady=5)

                details_frame = tk.Frame(frame, bg="white")
                details_frame.pack(fill="x")

                name_label = tk.Label(details_frame, text=item["name"], font=("Arial", 14, "bold"), bg="white")
                name_label.pack(anchor="w")

                desc_label = tk.Label(details_frame, text=item["description"], font=("Arial", 12), bg="white",
                                      wraplength=150,
                                      justify="left")
                desc_label.pack(anchor="w")

                price_label = tk.Label(details_frame, text=f"${item['price']}", font=("Arial", 12, "bold"), bg="white")
                price_label.pack(anchor="w")

                qty_label = tk.Label(details_frame, text="Quantity:", font=("Arial", 12), bg="white")
                qty_label.pack(anchor="w")

                qty_var = tk.IntVar(value=0)
                qty_entry = tk.Entry(details_frame, textvariable=qty_var, width=5, font=("Arial", 12))
                qty_entry.pack(anchor="w")

                self.order_quantities[item["name"]] = qty_var

                remark_label = tk.Label(details_frame, text="Remark:", font=("Arial", 12), bg="white")
                remark_label.pack(anchor="w")

                remark_var = tk.StringVar()
                remark_entry = tk.Entry(details_frame, textvariable=remark_var, width=20, font=("Arial", 12))
                remark_entry.pack(anchor="w")

                self.order_remarks[item["name"]] = remark_var

                add_to_cart_button = tk.Button(details_frame, text="Add to Cart", font=("Arial", 12), bg="#ff5722",
                                               fg="white",
                                               command=lambda i=item, q=qty_var, r=remark_var: self.add_to_cart(i, q,
                                                                                                                r))
                add_to_cart_button.pack(anchor="w", pady=5)

                self.menu_items_widgets.append((frame, img_label, name_label, desc_label, price_label, qty_entry,
                                                remark_entry, add_to_cart_button))

            def add_to_cart(self, item, qty_var, remark_var):
                qty = qty_var.get()
                remark = remark_var.get()
                if qty > 0:
                    if item["name"] in self.cart_items:
                        self.cart_items[item["name"]]["quantity"] += qty
                        self.cart_items[item["name"]]["remark"] = remark
                    else:
                        self.cart_items[item["name"]] = {
                            "price": item["price"],
                            "quantity": qty,
                            "remark": remark
                        }
                    messagebox.showinfo("Cart", f"Added {qty} {item['name']}(s) to cart with remark: {remark}.")
                else:
                    messagebox.showwarning("Cart", "Please enter a valid quantity.")

            def view_cart(self):
                CartWindow(self.cart_items)

            def show_category(self, category):
                # Clear current menu items
                for widget_tuple in self.menu_items_widgets:
                    for widget in widget_tuple:
                        widget.grid_forget()

                # Filter items of the selected category
                filtered_items = [item for item in self.menu_items if item["category"] == category]

                # Show items of the selected category
                for item_index, item in enumerate(filtered_items):
                    self.create_menu_item(item, item_index)

                # Update menu layout after showing new items
                self.update_menu_layout()

            def update_menu_layout(self):
                # Update canvas and scroll region
                self.menu_inner_frame.update_idletasks()
                self.canvas.config(scrollregion=self.canvas.bbox("all"))

        class CartWindow:
            def __init__(self, cart_items):
                self.cart_items = cart_items
                self.window = tk.Toplevel()
                self.window.title("Your Cart")
                self.window.geometry("400x400")

                self.cart_frame = tk.Frame(self.window)
                self.cart_frame.pack(pady=20)

                self.show_cart_items()

                self.payment_methods = ["E-wallet", "Online Banking", "Card"]
                self.payment_var = tk.StringVar(value=self.payment_methods[0])

                payment_label = tk.Label(self.window, text="Select Payment Method:", font=("Arial", 16))
                payment_label.pack(pady=10)

                for method in self.payment_methods:
                    radio_button = tk.Radiobutton(self.window, text=method, variable=self.payment_var, value=method,
                                                  font=("Arial", 14))
                    radio_button.pack(anchor="w")

                self.checkout_button = tk.Button(self.window, text="Checkout", font=("Arial", 16), bg="#ff5722",
                                                 fg="white",
                                                 command=self.checkout)
                self.checkout_button.pack(pady=20)

            def show_cart_items(self):
                for item, details in self.cart_items.items():
                    item_frame = tk.Frame(self.cart_frame, bg="white", bd=2, relief="groove")
                    item_frame.pack(padx=10, pady=10, fill="x")

                    name_label = tk.Label(item_frame, text=item, font=("Arial", 18, "bold"), bg="white")
                    name_label.pack(anchor="w")

                    qty_label = tk.Label(item_frame, text=f"Quantity: {details['quantity']}", font=("Arial", 14),
                                         bg="white")
                    qty_label.pack(anchor="w")

                    remark_label = tk.Label(item_frame, text=f"Remark: {details['remark']}", font=("Arial", 14),
                                            bg="white")
                    remark_label.pack(anchor="w")

                    price_label = tk.Label(item_frame, text=f"Price: ${details['price'] * details['quantity']}",
                                           font=("Arial", 14), bg="white")
                    price_label.pack(anchor="w")

            def checkout(self):
                total_amount = sum(
                    item_details['price'] * item_details['quantity'] for item_details in self.cart_items.values())

                if total_amount > 0:
                    messagebox.showinfo("Checkout", f"Total amount to be paid: ${total_amount:.2f}")
                    self.generate_receipt(self.cart_items, total_amount)
                    self.cart_window.destroy()
                else:
                    messagebox.showwarning("Checkout", "Your cart is empty!")

            def generate_receipt(self, cart_items, total_amount):
                receipt_filename = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                                filetypes=[("PDF files", "*.pdf"),
                                                                           ("All files", "*.*")])

                if not receipt_filename:
                    return

                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)

                pdf.cell(200, 10, txt="Food Ordering System Receipt", ln=True, align="C")
                pdf.ln(10)

                for item_name, item_details in cart_items.items():
                    line = f"{item_name} - ${item_details['price']} x {item_details['quantity']} - Remark: {item_details['remark']}"
                    print("Adding to PDF:", line)  # Debug print
                    pdf.cell(200, 10, txt=line, ln=True)

                pdf.ln(10)
                pdf.cell(200, 10, txt=f"Total Amount: ${total_amount:.2f}", ln=True)

                pdf.output(receipt_filename)
                messagebox.showinfo("Receipt", f"Receipt saved as {receipt_filename}")

        class Review:
            def __init__(self, user_name, rating, comment, photo_path=None):
                self.user_name = user_name
                self.rating = rating
                self.comment = comment
                self.photo_path = photo_path

            def __str__(self):
                return f"{self.user_name} rated {self.rating}/5: {self.comment}"

        class ReviewSystem:
            def __init__(self):
                self.reviews = []

            def add_review(self, user_name, rating, comment, photo_path=None):
                if rating < 1 or rating > 5:
                    raise ValueError("Rating must be between 1 and 5.")
                review = Review(user_name, rating, comment, photo_path)
                self.reviews.append(review)

            def get_reviews(self):
                return self.reviews

            def average_rating(self):
                if not self.reviews:
                    return None
                total_rating = sum(review.rating for review in self.reviews)
                return total_rating / len(self.reviews)

        class ReviewApp:
            def __init__(self, root, review_system):
                self.review_system = review_system
                self.rating = 0
                self.photo_path = None  # Initialize photo path

                root.title("Food Ordering System - Add Review")
                root.geometry("400x450")  # Increased height to accommodate photo upload

                self.user_name_label = tk.Label(root, text="User Name")
                self.user_name_label.pack(pady=5)
                self.user_name_entry = tk.Entry(root)
                self.user_name_entry.pack(pady=5)

                self.comment_label = tk.Label(root, text="Comment")
                self.comment_label.pack(pady=5)
                self.comment_entry = tk.Entry(root)
                self.comment_entry.pack(pady=5)

                self.rating_label = tk.Label(root, text="Rating")
                self.rating_label.pack(pady=5)

                # Create a frame for the star images
                self.stars_frame = tk.Frame(root)
                self.stars_frame.pack()

                # Resize star images
                self.star_images_empty = [self.load_image('images/star_empty.png') for _ in range(5)]
                self.star_images_filled = [self.load_image('images/star_filled.png') for _ in range(5)]
                self.star_labels = []
                for i in range(5):
                    label = tk.Label(self.stars_frame, image=self.star_images_empty[i])
                    label.grid(row=0, column=i)
                    label.bind('<Button-1>', lambda e, idx=i: self.set_rating(idx + 1))
                    self.star_labels.append(label)

                # Photo upload button
                self.upload_button = tk.Button(root, text="Upload Photo", command=self.upload_photo)
                self.upload_button.pack(pady=5)

                self.submit_button = tk.Button(root, text="Submit Review", command=self.submit_review)
                self.submit_button.pack(pady=5)

                self.admin_button = tk.Button(root, text="View Reviews", command=self.open_admin_view)
                self.admin_button.pack(pady=5)

            def load_image(self, path, size=(32, 32)):
                image = Image.open(path)
                image = image.resize(size, Image.LANCZOS)
                return ImageTk.PhotoImage(image)

            def set_rating(self, rating):
                self.rating = rating
                for i in range(5):
                    if i < rating:
                        self.star_labels[i].config(image=self.star_images_filled[i])
                    else:
                        self.star_labels[i].config(image=self.star_images_empty[i])

            def upload_photo(self):
                file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
                if file_path:
                    self.photo_path = file_path
                    messagebox.showinfo("Success", "Photo uploaded successfully!")

            def submit_review(self):
                user_name = self.user_name_entry.get()
                comment = self.comment_entry.get()

                if self.rating == 0:
                    messagebox.showerror("Error", "Please select a rating.")
                    return

                try:
                    self.review_system.add_review(user_name, self.rating, comment, self.photo_path)
                    messagebox.showinfo("Success", "Review added successfully!")
                    self.clear_entries()
                except ValueError as ve:
                    messagebox.showerror("Error", str(ve))

            def clear_entries(self):
                self.user_name_entry.delete(0, tk.END)
                self.comment_entry.delete(0, tk.END)
                self.set_rating(0)
                self.photo_path = None

            def open_admin_view(self):
                AdminView(tk.Toplevel(), self.review_system)

        class AdminView:
            def __init__(self, root, review_system):
                self.review_system = review_system

                root.title("Admin - View Reviews")
                root.geometry("800x600")

                self.review_frame = tk.Frame(root)
                self.review_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

                self.display_reviews()

            def display_reviews(self):
                reviews = self.review_system.get_reviews()
                if not reviews:
                    tk.Label(self.review_frame, text="No reviews available.").pack()
                else:
                    for review in reviews:
                        review_frame = tk.Frame(self.review_frame, bd=1, relief=tk.RIDGE, padx=10, pady=10)
                        review_frame.pack(pady=10, fill=tk.BOTH)

                        # Display review details (user, rating, comment)
                        tk.Label(review_frame, text=f"User: {review.user_name}").pack(anchor=tk.W)
                        tk.Label(review_frame, text=f"Rating: {review.rating}/5").pack(anchor=tk.W)
                        tk.Label(review_frame, text="Comment:").pack(anchor=tk.W)
                        tk.Label(review_frame, text=review.comment).pack(anchor=tk.W)

                        # Display uploaded photo, if any
                        if review.photo_path:
                            photo = Image.open(review.photo_path)
                            photo = photo.resize((200, 200), Image.LANCZOS)
                            photo = ImageTk.PhotoImage(photo)
                            photo_label = tk.Label(review_frame, image=photo)
                            photo_label.image = photo
                            photo_label.pack()

        # Create the main window
        root = tk.Tk()
        root.title("Customer Homepage")
        root.geometry("1000x1000")
        root.configure(bg="pink")

        # Create and place the title label at the top center
        title_label = tk.Label(root, text="HOME", font=("Ink Free", 50, "bold"), fg="black", bg="pink")
        title_label.pack(pady=60)

        # Create and place the buttons on the window
        menu_button = tk.Button(root, text="MENU", bg="black", fg="white", font=("Helvetica", 20, "bold"),
                                command=show_menu)
        menu_button.pack(pady=5, padx=20)

        review_button = tk.Button(root, text="REVIEW", bg="black", fg="white", font=("Helvetica", 20, "bold"),
                                  command=show_review)
        review_button.pack(pady=5, padx=20)

        customer_support_button = tk.Button(root, text="CUSTOMER SUPPORT", bg="black", fg="white",
                                            font=("Helvetica", 20, "bold"), command=show_customer_support)
        customer_support_button.pack(pady=5, padx=20)

        logout_button = tk.Button(root, text="LOGOUT", bg="black", fg="white", font=("Helvetica", 20, "bold"),
                                  command=open_customer_login)
        logout_button.pack(pady=5, padx=20)

        # Define the show_review function to open the review window
        def show_review():
            review_system = ReviewSystem()
            review_app = ReviewApp(tk.Toplevel(), review_system)

        # Start the Tkinter event loop
        root.mainloop()

    def clear_frame():
        for widget in root.winfo_children():
            widget.destroy()

    LoginForm()
    root.mainloop()

open_customer_login()