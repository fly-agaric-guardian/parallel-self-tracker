import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
from collections import defaultdict
import customtkinter as ctk
from tkinter import ttk
import tkinter as tk

class AnalysisUI:
    def __init__(self, parent, parent_root, db_manager):
        self.parent = parent
        self.parent_root = parent_root
        self.db_manager = db_manager
        
    def setup_ui(self):
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.parent_root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create title
        title_label = ctk.CTkLabel(self.main_frame, text="Game Data Analysis", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
        
        # Create button frame
        button_frame = ctk.CTkFrame(self.main_frame)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        # Back button
        back_btn = ctk.CTkButton(button_frame, text="Back to Main Menu", command=self.back_to_main)
        back_btn.pack(side="left", padx=5)
        
        # Analyze button
        analyze_btn = ctk.CTkButton(button_frame, text="Generate Analysis", command=self.generate_analysis)
        analyze_btn.pack(side="left", padx=5)
        
        # Create scrollable frame to contain charts
        self.canvas_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def reset_ui(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.main_frame.pack_forget()
        
    def back_to_main(self):
        self.reset_ui()
        self.parent.setup_ui()
        
    def generate_analysis(self):
        # Clear previous content
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
            print(widget)
            
        # Get all records
        records = self.db_manager.get_all_records()
        
        if not records:
            no_data_label = ctk.CTkLabel(self.canvas_frame, text="No data available for analysis")
            no_data_label.pack(pady=20)
            return
            
        # Generate analysis
        self.create_paragon_analysis_tables(records)
        self.create_mmr_graph(records)
        
    def create_paragon_analysis_tables(self, records):
        paragon_stats = defaultdict(lambda: defaultdict(lambda: {
            'otp_matches': 0, 'otp_wins': 0, 'otd_matches': 0, 'otd_wins': 0
        }))
        
        for record in records:
            my_paragon = record[1]
            opp_paragon = record[2]
            turn_order = record[3]
            result = record[4]
            
            is_win = result == "WIN"
            
            if turn_order == "OTP":
                paragon_stats[my_paragon][opp_paragon]['otp_matches'] += 1
                if is_win:
                    paragon_stats[my_paragon][opp_paragon]['otp_wins'] += 1
            else:  # OTD
                paragon_stats[my_paragon][opp_paragon]['otd_matches'] += 1
                if is_win:
                    paragon_stats[my_paragon][opp_paragon]['otd_wins'] += 1
        
        # Create table for each of my paragons
        for my_paragon in paragon_stats:
            # Create paragon title
            paragon_title = ctk.CTkLabel(self.canvas_frame, text=f"{my_paragon} Analysis", 
                                       font=("Arial", 16, "bold"))
            paragon_title.pack(pady=(20, 10))
            
            # Create table frame
            table_frame = ctk.CTkFrame(self.canvas_frame)
            table_frame.pack(fill="x", padx=10, pady=5)
            
            # Create table
            columns = ("Opp's Paragon", "Total Matches", "Total Winrate", "OTP Matches", "OTP Wins", "OTP Winrate", "OTD Matches", "OTD Wins", "OTD Winrate")
            tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=len(paragon_stats[my_paragon]) + 1)
            
            # Set column titles
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor="center")
            
            # Calculate total data
            total_otp_matches = 0
            total_otp_wins = 0
            total_otd_matches = 0
            total_otd_wins = 0
            
            for stats in paragon_stats[my_paragon].values():
                total_otp_matches += stats['otp_matches']
                total_otp_wins += stats['otp_wins']
                total_otd_matches += stats['otd_matches']
                total_otd_wins += stats['otd_wins']
            
            # Add total row
            total_otp_winrate = (total_otp_wins / total_otp_matches * 100) if total_otp_matches > 0 else 0
            total_otd_winrate = (total_otd_wins / total_otd_matches * 100) if total_otd_matches > 0 else 0
            total_matches = total_otp_matches + total_otd_matches
            total_wins = total_otp_wins + total_otd_wins
            total_winrate = (total_wins / total_matches * 100) if total_matches > 0 else 0
            
            tree.insert("", "end", values=(
                "Overall",
                total_matches,
                f"{total_winrate:.1f}%",
                total_otp_matches,
                total_otp_wins,
                f"{total_otp_winrate:.1f}%",
                total_otd_matches,
                total_otd_wins,
                f"{total_otd_winrate:.1f}%",
            ), tags=('total',))
            
            # Add data
            for opp_paragon, stats in paragon_stats[my_paragon].items():
                otp_matches = stats['otp_matches']
                otp_wins = stats['otp_wins']
                otp_winrate = (otp_wins / otp_matches * 100) if otp_matches > 0 else 0
                
                otd_matches = stats['otd_matches']
                otd_wins = stats['otd_wins']
                otd_winrate = (otd_wins / otd_matches * 100) if otd_matches > 0 else 0
                
                total_matches = otp_matches + otd_matches
                total_wins = otp_wins + otd_wins
                total_winrate = (total_wins / total_matches * 100) if total_matches > 0 else 0
                
                tree.insert("", "end", values=(
                    opp_paragon,
                    total_matches,
                    f"{total_winrate:.1f}%",
                    otp_matches,
                    otp_wins,
                    f"{otp_winrate:.1f}%",
                    otd_matches,
                    otd_wins,
                    f"{otd_winrate:.1f}%"
                ))
            
            # Set total row style
            tree.tag_configure('total', background='lightgray', font=('Arial', 10, 'bold'))
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
    def create_mmr_graph(self, records):
        # Create MMR graph title
        mmr_title = ctk.CTkLabel(self.canvas_frame, text="MMR Changes", 
                               font=("Arial", 16, "bold"))
        mmr_title.pack(pady=(30, 10))
        
        # Prepare data: only include MMR > 1000
        dates = []
        mmrs = []
        
        for record in records:
            date = record[6]  # date column
            mmr = record[5]   # mmr column
            
            try:
                mmr_int = int(mmr)
                if mmr_int > 1000:
                    dates.append(date)
                    mmrs.append(mmr_int)
            except ValueError:
                continue
        
        if not dates:
            no_mmr_label = ctk.CTkLabel(self.canvas_frame, text="No valid MMR data")
            no_mmr_label.pack(pady=10)
            return
        
        # Create matplotlib chart
        fig = Figure(figsize=(12, 6))
        ax = fig.add_subplot(111)
        
        # Plot MMR line
        ax.plot(range(len(dates)), mmrs, marker='o', linewidth=2, markersize=4)
        
        # Set title and labels
        ax.set_title('MMR changes', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('MMR', fontsize=12)
        
        # Set x-axis labels (show every 10th date)
        if len(dates) > 10:
            step = len(dates) // 10
            x_positions = list(range(0, len(dates), step))
            x_labels = [dates[i] for i in x_positions]
            ax.set_xticks(x_positions)
            ax.set_xticklabels(x_labels, rotation=45)
        else:
            ax.set_xticks(range(len(dates)))
            ax.set_xticklabels(dates, rotation=45)
        
        #Add grid
        ax.grid(True, alpha=0.3)
        
        # Embed matplotlib chart into tkinter
        canvas = FigureCanvasTkAgg(fig, self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)