import customtkinter as ctk
from tkinter import ttk
import sqlite3
from datetime import datetime
from db.db_manager import DatabaseManager
from utils.validation import is_valid_record
from ui.analysis_ui import AnalysisUI
from tkinter import messagebox

class UIManager:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Parallel Self Tracker")
        self.root.geometry("1200x700")
        
        self.db_manager = DatabaseManager()
        self.db_manager.create_table()

        self.analysis_ui = AnalysisUI(self, self.root, self.db_manager)
        
        self.setup_ui()
        self.load_data()

        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

    def on_exit(self):
        if messagebox.askyesno("Exit", "Do you want to quit the application?"):
            try:
                self.root.destroy()
            except Exception as e:
                print(e)
        
    def setup_ui(self):
        # Main Frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left Frame
        left_frame = ctk.CTkFrame(self.main_frame, width=400)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        
        # Title
        title_label = ctk.CTkLabel(left_frame, text="Data Input", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Input Fields
        self.my_paragon_var = ctk.StringVar()
        self.opp_paragon_var = ctk.StringVar()
        self.turn_order_var = ctk.StringVar()
        self.result_var = ctk.StringVar()
        self.my_mmr_var = ctk.StringVar()
        self.date_var = ctk.StringVar()
        
        # My Paragon Entry
        my_paragon_frame = ctk.CTkFrame(left_frame)
        my_paragon_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(my_paragon_frame, text="My Paragon:").pack(side="left", padx=5)
        ctk.CTkEntry(my_paragon_frame, textvariable=self.my_paragon_var, width=200).pack(side="right", padx=5)
        
        # Opp Paragon Entry
        opp_paragon = ctk.CTkFrame(left_frame)
        opp_paragon.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(opp_paragon, text="Opponent's Paragon:").pack(side="left", padx=5)
        ctk.CTkEntry(opp_paragon, textvariable=self.opp_paragon_var, width=200).pack(side="right", padx=5)
        
        # Turn Order Entry
        turn_order_frame = ctk.CTkFrame(left_frame)
        turn_order_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(turn_order_frame, text="Turn Order:").pack(side="left", padx=5)

        self.turn_order_var.set("OTP")
        def toggle_turn_order():
            if self.turn_order_var.get() == "OTP":
                self.turn_order_var.set("OTD")
            else:
                self.turn_order_var.set("OTP")
            turn_order_btn.configure(text=self.turn_order_var.get())
        
        turn_order_btn = ctk.CTkButton(turn_order_frame, text=self.turn_order_var.get(), 
                                     command=toggle_turn_order, width=200, fg_color="white", text_color="black", hover_color="gray")
        turn_order_btn.pack(side="right", padx=5)
        
        # Result Entry
        result_frame = ctk.CTkFrame(left_frame)
        result_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(result_frame, text="Result:").pack(side="left", padx=5)

        self.result_var.set("WIN")
        def toggle_result():
            if self.result_var.get() == "WIN":
                self.result_var.set("LOSE")
            else:
                self.result_var.set("WIN")
            result_btn.configure(text=self.result_var.get())
        
        result_btn = ctk.CTkButton(result_frame, text=self.result_var.get(), 
                                 command=toggle_result, width=200, fg_color="white", text_color="black", hover_color="gray")
        result_btn.pack(side="right", padx=5)
            

        # My MMR Entry
        my_mmr_frame = ctk.CTkFrame(left_frame)
        my_mmr_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(my_mmr_frame, text="My MMR:").pack(side="left", padx=5)
        ctk.CTkEntry(my_mmr_frame, textvariable=self.my_mmr_var, width=200).pack(side="right", padx=5)

        # Date Entry
        date_frame = ctk.CTkFrame(left_frame)
        date_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(date_frame, text="Date:").pack(side="left", padx=5)
        ctk.CTkEntry(date_frame, textvariable=self.date_var, width=200).pack(side="right", padx=5)
        
        # Right Frame
        right_frame = ctk.CTkFrame(self.main_frame)
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Search Navigation Bar
        nav_frame = ctk.CTkFrame(right_frame)
        nav_frame.pack(fill="x", padx=10, pady=10)
        
        # Search Options
        self.search_by_var = ctk.StringVar(value="my_paragon")
        search_options = ["my_paragon", "opp_paragon", "turn_order", "result", "my_mmr", "date"]
        search_combo = ctk.CTkComboBox(nav_frame, values=search_options, 
                                     variable=self.search_by_var, width=150)
        search_combo.pack(side="left", padx=5)
        
        # Search Input
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(nav_frame, textvariable=self.search_var, 
                                   placeholder_text="Enter Search Condition", width=200)
        search_entry.pack(side="left", padx=5)
        
        # Search Button
        search_btn = ctk.CTkButton(nav_frame, text="Search", command=self.search_records, width=80)
        search_btn.pack(side="left", padx=5)
        
        # Show All Button
        showall_btn = ctk.CTkButton(nav_frame, text="Show All", command=self.load_data, width=80)
        showall_btn.pack(side="left", padx=5)
        
        # Treeview
        tree_frame = ctk.CTkFrame(right_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Setup Treeview
        columns = ("ID", "My Paragon", "Opp's Paragon", "Turn Order", "Result", "My MMR", "Date")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        self.selected_ids = []

        def on_tree_select(event):
            self.selected_ids = []
            selected_items = self.tree.selection()
            if selected_items:
                for item_iid in selected_items:
                    item_values = self.tree.item(item_iid, "values")
                    item_text = self.tree.item(item_iid, "text")
                    self.selected_ids.append(item_values[0])
            print(self.selected_ids)

        self.tree.bind("<<TreeviewSelect>>", on_tree_select)
        
        # Set Column Headers
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bottom Button Area
        button_frame = ctk.CTkFrame(right_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        # Operation Buttons
        add_btn = ctk.CTkButton(button_frame, text="Add Record", command=self.add_record)
        add_btn.pack(side="left", padx=5)
        
        update_btn = ctk.CTkButton(button_frame, text="Update Record", command=self.update_record)
        update_btn.pack(side="left", padx=5)
        
        delete_btn = ctk.CTkButton(button_frame, text="Delete Record", command=self.delete_record)
        delete_btn.pack(side="left", padx=5)

        # Analysis Button
        analysis_btn = ctk.CTkButton(button_frame, text="Analysis", command=self.open_analysis_window)
        analysis_btn.pack(side="left", padx=5)

        self.load_data()
        
    def load_data(self):
        # Clear Existing Data
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        records = self.db_manager.get_all_records()
        
        for record in records:
            self.tree.insert("", "end", values=record)
            
    def search_records(self):
        search_term = self.search_var.get()
        search_by = self.search_by_var.get()
        
        if not search_term:
            self.load_data()
            return
            
        # Clear Existing Data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        records = self.db_manager.fetch_all(f"SELECT * FROM records WHERE {search_by} LIKE ? ORDER BY id", 
                                            (f"%{search_term}%",))
        
        for record in records:
            self.tree.insert("", "end", values=record)
            
    def add_record(self):
        my_paragon = self.my_paragon_var.get()
        opp_paragon = self.opp_paragon_var.get()
        turn_order = self.turn_order_var.get()
        result = self.result_var.get()
        my_mmr = self.my_mmr_var.get()
        date = self.date_var.get()
        print(my_paragon, opp_paragon, turn_order, result, my_mmr, date)
        
        if not is_valid_record((my_paragon, opp_paragon, turn_order, result, my_mmr, date)):
            messagebox.showerror("Invalid Input", "Please check your input")
            return

        self.db_manager.insert_record((my_paragon, opp_paragon, turn_order, result, my_mmr, date))
        
        self.clear_entries()
        self.load_data()
        
    def update_record(self):
        if not self.selected_ids:
            return
            
        my_paragon = self.my_paragon_var.get()
        opp_paragon = self.opp_paragon_var.get()
        turn_order = self.turn_order_var.get()
        result = self.result_var.get()
        my_mmr = self.my_mmr_var.get()
        date = self.date_var.get()
        
        if not is_valid_record((my_paragon, opp_paragon, turn_order, result, my_mmr, date)):
            return
        
        self.db_manager.update_record((my_paragon, opp_paragon, turn_order, result, my_mmr, date), self.selected_ids[0])

        self.clear_entries()
        self.load_data()
        
    def delete_record(self):
        if not self.selected_ids:
            return
        
        self.db_manager.delete_record(self.selected_ids)

        self.clear_entries()
        self.load_data()
        
    def clear_entries(self):
        self.opp_paragon_var.set("")
        self.my_mmr_var.set("")
        
    def run(self):
        self.root.mainloop()

    def reset_ui(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            print(widget)
        self.main_frame.pack_forget()

    def open_analysis_window(self):
        self.reset_ui()
        self.analysis_ui.setup_ui()
