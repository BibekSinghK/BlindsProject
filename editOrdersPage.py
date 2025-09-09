import customtkinter as ctk
import os
import sqlite3
import platform

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class EditOrdersPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        back_btn = ctk.CTkButton(self, text="← Back", width=80, command=lambda: self.master.show_frame(self.master.welcome_page))
        back_btn.pack(pady=(10, 0), padx=10, anchor="w")
        
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=650, height=400)
        self.scroll_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.scroll_frame._scrollbar.grid_remove()
        self.scroll_frame.bind_all("<MouseWheel>", lambda e: self.scroll_frame._parent_canvas.yview_scroll(-1*(e.delta//120), "units"))

        self.conn = sqlite3.connect("blinds_app.db")
        self.cursor = self.conn.cursor()
        self.conn.execute("PRAGMA foreign_keys = ON;")

        self.load_customers()

    def load_customers(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.cursor.execute("SELECT id, name FROM customers;")
        customers = self.cursor.fetchall()

        for idx, (customer_id, name) in enumerate(customers):
            row_frame = ctk.CTkFrame(self.scroll_frame)
            row_frame.pack(fill="x", pady=5)

            name_label = ctk.CTkLabel(row_frame, text=name, width=200, anchor="w")
            name_label.pack(side="left", padx=10)

            sheet_path = f"cost_sheets/{name}_cost_sheet.xlsx"
            if os.path.exists(sheet_path):
                open_btn = ctk.CTkButton(row_frame, text="Open Sheet", width=120,
                                         command=lambda: self.open_sheet(sheet_path))
                open_btn.pack(side="left", padx=10)
            else:
                no_sheet_label = ctk.CTkLabel(row_frame, text="No sheet available", text_color="red")
                no_sheet_label.pack(side="left", padx=10)

            delete_btn = ctk.CTkButton(row_frame, text="Delete", fg_color="red",
                                       command=lambda: self.delete_customer(customer_id, name))
            delete_btn.pack(side="right", padx=10)

    def open_sheet(self, path):
        os_type = platform.system()
        if os_type == "Windows":
            os.startfile(path)
        elif os_type == "Darwin":
            os.system(f'open "{path}"')
        elif os_type == "Linux":
            os.system(f'xdg-open "{path}"')

    def delete_customer(self, customer_id, name):
        self.cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        self.conn.commit()
        folder_path = "cost_sheets"
        file_name = f"{name}_cost_sheet.xlsx"
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)
        self.load_customers()