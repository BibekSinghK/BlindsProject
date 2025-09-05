import customtkinter as ctk
from database import Database
from welcomePage import WelcomePage
from orderCreationPage import OrderCreationPage
from blindCreationPage import BlindCreationPage
from editOrdersPage import EditOrdersPage

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class BlindsTool(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Blinds Tool")
        self.attributes('-fullscreen', True)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.db = Database()
        self.db.create_tables()
        self.curr_customer = None

        self.welcome_page = WelcomePage(self)
        self.create_order_page = OrderCreationPage(self)
        self.blind_creation_page = BlindCreationPage(self)
        self.edit_orders_page = EditOrdersPage(self)

        self.show_frame(self.welcome_page)

        self.bind("<Escape>", lambda e: self.destroy())

    def show_frame(self, frame):
        frame.tkraise()
        
if __name__ == "__main__":
    blindsTool = BlindsTool()
    blindsTool.mainloop()
    