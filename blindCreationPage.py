import customtkinter as ctk
from excelGenerator import ExcelGenerator

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class BlindCreationPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        self.blinds_widgets = []
        self.create_widgets()

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, pady=50, padx=50)

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        input_frame = ctk.CTkFrame(main_frame)
        input_frame.grid(row=0, column=0, sticky="n")

        row = 0
        ctk.CTkLabel(input_frame, text="Location:").grid(row=row, column=0, sticky="w", pady=5)
        self.location_entry = ctk.CTkEntry(input_frame, width=200)
        self.location_entry.grid(row=row, column=1, pady=5)

        row += 1
        ctk.CTkLabel(input_frame, text="Blind Type:").grid(row=row, column=0, sticky="w", pady=5)
        self.blind_type = ctk.CTkOptionMenu(input_frame, values=['Zebra', 'Roller', 'Roller Blackout', 'Shangri-La'],
                                            command=self.update_fabrics)
        self.blind_type.grid(row=row, column=1, pady=5)

        row += 1
        self.filter = ctk.StringVar()
        self.fabric_filter = ctk.CTkEntry(input_frame, width=200, textvariable=self.filter, placeholder_text="Fabric Filter")
        self.fabric_filter.grid(row=row, column=2, pady=5)
        
        ctk.CTkLabel(input_frame, text="Fabric:").grid(row=row, column=0, sticky="w", pady=5)
        self.fabric = ctk.CTkOptionMenu(input_frame, values=self.master.db.get_blind_types("Zebra"))
        self.fabric.grid(row=row, column=1, pady=5)
        
        self.filter.trace_add("write", self.update_filter)
        
        row += 1
        ctk.CTkLabel(input_frame, text="Width:").grid(row=row, column=0, sticky="w", pady=5)
        self.width_entry = ctk.CTkEntry(input_frame, width=200)
        self.width_entry.grid(row=row, column=1, pady=5, sticky="w")

        self.width_fraction = ctk.CTkOptionMenu(input_frame, values=["0", "1/8", "1/4", "3/8", "1/2", "5/8", "3/4", "7/8"])
        self.width_fraction.grid(row=row, column=2, padx=5)

        row += 1
        ctk.CTkLabel(input_frame, text="Height:").grid(row=row, column=0, sticky="w", pady=5)
        self.height_entry = ctk.CTkEntry(input_frame, width=200)
        self.height_entry.grid(row=row, column=1, pady=5, sticky="w")

        self.height_fraction = ctk.CTkOptionMenu(input_frame, values=["0", "1/8", "1/4", "3/8", "1/2", "5/8", "3/4", "7/8"])
        self.height_fraction.grid(row=row, column=2, padx=5)

        row += 1
        ctk.CTkLabel(input_frame, text="Control:").grid(row=row, column=0, sticky="w", pady=5)
        self.control = ctk.CTkOptionMenu(input_frame, values=["Chain", "Chain + Chainguard", "Wand", "Motor"],
                                         command=self.update_material)
        self.control.grid(row=row, column=1, pady=5)

        row += 1
        ctk.CTkLabel(input_frame, text="Control Material:").grid(row=row, column=0, sticky="w", pady=5)
        self.control_mat = ctk.CTkOptionMenu(input_frame, values=["Plastic", "Steel"])
        self.control_mat.grid(row=row, column=1, pady=5)

        row += 1
        ctk.CTkLabel(input_frame, text="Control Position:").grid(row=row, column=0, sticky="w", pady=5)
        self.control_pos = ctk.CTkOptionMenu(input_frame, values=["Left", "Right"])
        self.control_pos.grid(row=row, column=1, pady=5)

        row += 1
        ctk.CTkLabel(input_frame, text="Bracket:").grid(row=row, column=0, sticky="w", pady=5)
        self.bracket = ctk.CTkOptionMenu(input_frame, values=["#8", "#6"])
        self.bracket.grid(row=row, column=1, pady=5)

        row += 1
        ctk.CTkLabel(input_frame, text="Quantity:").grid(row=row, column=0, sticky="w", pady=5)
        self.quantity_entry = ctk.CTkEntry(input_frame, width=100)
        self.quantity_entry.grid(row=row, column=1, pady=5)

        row += 1
        add_btn = ctk.CTkButton(input_frame, text="Add Blind", width=200, command=self.add_blind)
        add_btn.grid(row=row, column=0, columnspan=3, pady=20)

        right_frame = ctk.CTkFrame(main_frame)
        right_frame.grid(row=0, column=1, padx=50, sticky="n")

        self.scrollable = ctk.CTkScrollableFrame(right_frame, width=400, height=400)
        self.scrollable.pack()

        done_btn = ctk.CTkButton(right_frame, text="Done", width=200, command=self.done)
        done_btn.pack(pady=20)

    def update_fabrics(self, blind_type):
        fabrics = self.master.db.get_blind_types(blind_type)
        self.fabric.configure(values=fabrics)
        self.fabric.set(fabrics[0])

    def update_material(self, control):
        self.control_mat.configure(state="normal")
        if control == "Chain" or control == "Chain + Chainguard":
            self.control_mat.configure(values=["Plastic", "Steel"])
        elif control == "Motor":
            self.control_mat.configure(values=["Wired", "Rechargeable"])
            self.control_mat.set("Wired")
        else:
            self.control_mat.set("Plastic")
            self.control_mat.configure(state="disabled")

    def filter_fabrics(self, fabrics, substring):
        def containsSubstring(fabric):
            return substring.lower() in fabric.lower()
        
        filteredFabrics = list(filter(containsSubstring, fabrics))
        return filteredFabrics

    def update_filter(self, *args):
        filtered = self.filter_fabrics(self.master.db.get_blind_types(self.blind_type.get()), self.filter.get())
        if not filtered:
            filtered = [""]
        self.fabric.configure(values=[])
        self.fabric.configure(values=list(set(filtered)))
        self.fabric.set(filtered[0])
    
    def add_blind(self):
        
        def convert_to_decimal(value, fraction):
            fraction_map = {
                "0": 0,
                "1/8": 0.125,
                "1/4": 0.25,
                "3/8": 0.375,
                "1/2": 0.5,
                "5/8": 0.625,
                "3/4": 0.75,
                "7/8": 0.875
            }
            return float(value) + fraction_map.get(fraction, 0)
        
        location = self.location_entry.get()
        blind_type = self.blind_type.get()
        fabric = self.fabric.get()
        width = f"{convert_to_decimal(self.width_entry.get(), self.width_fraction.get())}"
        height = f"{convert_to_decimal(self.height_entry.get(), self.height_fraction.get())}"
        control = self.control.get()
        control_mat = self.control_mat.get()
        control_pos = self.control_pos.get()
        bracket = self.bracket.get()
        quantity = self.quantity_entry.get()
        price = self.master.db.get_blind_price(blind_type, fabric)

        self.master.curr_customer.addBlind(location, blind_type, fabric, width, height, control, control_mat, control_pos, bracket, quantity, price)
        self.master.db.add_blind(self.master.curr_customer.id, location, blind_type, fabric, width, height, control, control_mat, control_pos, bracket, quantity, price)

        self.refresh_list()

    def refresh_list(self):
        for widget in self.blinds_widgets:
            widget.destroy()
        self.blinds_widgets.clear()

        for blind in self.master.curr_customer.blinds:
            row_frame = ctk.CTkFrame(self.scrollable)
            row_frame.pack(fill="x", pady=5)

            info = f"#{blind.blindNo}: {blind.location}, {blind.fabric}, {blind.width} x {blind.height}, {blind.quantity} pcs"
            label = ctk.CTkLabel(row_frame, text=info, anchor="w")
            label.pack(side="left", padx=5)

            delete_btn = ctk.CTkButton(row_frame, text="Delete", width=80,
                                       command=lambda b=blind: self.delete_blind(b))
            delete_btn.pack(side="right", padx=5)

            self.blinds_widgets.append(row_frame)

    def delete_blind(self, blind):
        self.master.curr_customer.blinds.remove(blind)
        self.master.curr_customer.blindCount -= 1
        self.refresh_list()

    def done(self):
        print(f"Customer {self.master.curr_customer.name} has {len(self.master.curr_customer.blinds)} blinds.")
        sheet = ExcelGenerator(self.master.curr_customer)
        sheet.write_blinds()
        self.master.curr_customer = None
        self.master.show_frame(self.master.welcome_page)