import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class WelcomePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        inner_frame = ctk.CTkFrame(self, fg_color="transparent")
        inner_frame.grid(row=0, column=0)

        label = ctk.CTkLabel(inner_frame, text="Welcome!", font=("Helvetica", 36, "bold"))
        label.pack(pady=(0, 20))

        create_btn = ctk.CTkButton(inner_frame, text="Create New Order", width=300, height=60,
                                   command=lambda: self.master.show_frame(self.master.create_order_page))
        create_btn.pack(pady=10)

        edit_btn = ctk.CTkButton(inner_frame, text="Edit Orders", width=300, height=60,
                                 command=self.refresh_customers)
        edit_btn.pack(pady=10)
        
    def refresh_customers(self):
        self.master.edit_orders_page.load_customers()
        self.master.show_frame(self.master.edit_orders_page)