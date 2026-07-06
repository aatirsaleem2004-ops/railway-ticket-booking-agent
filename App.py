import random
import time
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox

# Set up global styling theme to match the green mock design
ctk.set_appearance_mode("Light")  
ctk.set_default_color_theme("green")

# =======================================================
#                  DATABASE & BACKEND LOGIC
# =======================================================
trains = [
    {"id": "T101", "name": "Green Line",    "from": "Lahore",    "to": "Karachi",   "time": "08:00 AM", "price": 2500, "seats": 15},
    {"id": "T102", "name": "Karakoram Exp", "from": "Lahore",    "to": "Islamabad", "time": "10:00 AM", "price": 800,  "seats": 0},
    {"id": "T103", "name": "Khyber Mail",   "from": "Karachi",   "to": "Peshawar",  "time": "06:00 PM", "price": 3000, "seats": 12},
    {"id": "T104", "name": "Awam Express",  "from": "Islamabad", "to": "Lahore",    "time": "09:00 AM", "price": 700,  "seats": 3},
    {"id": "T105", "name": "Sir Syed Exp",  "from": "Lahore",    "to": "Karachi",   "time": "08:00 PM", "price": 2200, "seats": 8},
]

bookings = {}
complaints = {}

# =======================================================
#               MAIN APP WINDOW CLASS
# =======================================================
class RailwayApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Railway Ticket Booking Agent")
        self.geometry("1180x720")
        self.resizable(True, True)

        # Main Layout Grid Split
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------------------------------------------------
        # SIDEBAR FRAME (Perfect solid dark green column)
        # ---------------------------------------------------
        self.sidebar_frame = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color="#4E6E36")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_columnconfigure(0, weight=1) 
        self.sidebar_frame.grid_rowconfigure(8, weight=1)    

        # Sidebar Header Logo Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="🚂 Pakistan Railways", 
            font=("Arial", 20, "bold"), 
            text_color="white",
            anchor="w"
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(35, 30), sticky="ew")

        # Navigation Buttons Grid Arrangement
        self.btn_search = self.create_nav_btn("🔍  Search Trains", 1, self.show_search_frame)
        self.btn_book = self.create_nav_btn("🎫  Book Ticket", 2, self.show_book_frame)
        self.btn_pay = self.create_nav_btn("💳  Pay Ticket", 3, self.show_pay_frame)
        self.btn_cancel = self.create_nav_btn("❌  Cancel Ticket", 4, self.show_cancel_frame)
        self.btn_bookings = self.create_nav_btn("📋  My Bookings", 5, self.show_bookings_frame)
        self.btn_complaint = self.create_nav_btn("📁  File Complaint", 6, self.show_complaint_frame)

        # Bottom System Version Footer Text
        self.footer_lbl = ctk.CTkLabel(self.sidebar_frame, text="v2.1 Agent System", font=("Arial", 11, "normal"), text_color="#A9C298", anchor="w")
        self.footer_lbl.grid(row=9, column=0, padx=20, pady=20, sticky="ew")

        # ---------------------------------------------------
        # MAIN CONTENT AREA FRAME
        # ---------------------------------------------------
        self.content_frame = ctk.CTkFrame(self, fg_color="#F4F6F3", corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

        # Top Uniform Header Toolbar
        self.header_frame = ctk.CTkFrame(self.content_frame, height=75, fg_color="white", corner_radius=0, border_width=1, border_color="#E5E5E5")
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_title = ctk.CTkLabel(self.header_frame, text="Welcome Agent", font=("Arial", 24, "bold"), text_color="#2D3748")
        self.header_title.pack(side="left", padx=30, pady=20)

        self.active_view = None
        self.show_search_frame() 

    def create_nav_btn(self, text, row, command):
        btn = ctk.CTkButton(
            self.sidebar_frame, 
            text=text, 
            font=("Arial", 15, "bold"),
            anchor="w",                  
            fg_color="transparent", 
            text_color="white",
            hover_color="#3B5428",       
            height=46,
            corner_radius=4,             
            border_spacing=15,           
            command=command
        )
        btn.grid(row=row, column=0, padx=8, pady=3, sticky="ew")
        return btn

    def set_active_button(self, active_btn):
        for btn in [self.btn_search, self.btn_book, self.btn_pay, self.btn_cancel, self.btn_bookings, self.btn_complaint]:
            btn.configure(fg_color="transparent")
        active_btn.configure(fg_color="#3A5328") 

    def clear_active_view(self):
        if self.active_view is not None:
            self.active_view.destroy()

    def play_loading_animation(self, target_label, completion_text, final_task_function):
        frames = ["▰▱▱▱▱ 20%", "▰▰▱▱▱ 40%", "▰▰▰▱▱ 60%", "▰▰▰▰▱ 80%", "▰▰▰▰▰ 100%"]
        def run_anim(idx):
            if idx < len(frames):
                target_label.configure(text=f"Processing Request: {frames[idx]}", text_color="#4E6E36")
                self.after(110, lambda: run_anim(idx + 1))
            else:
                target_label.configure(text=completion_text, text_color="green")
                final_task_function()
        run_anim(0)

    # =======================================================
    # VIEW 1: SEARCH TRAINS
    # =======================================================
    def show_search_frame(self):
        self.clear_active_view()
        self.set_active_button(self.btn_search)
        self.header_title.configure(text="Search Trains")

        self.active_view = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        self.active_view.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        self.active_view.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(self.active_view, fg_color="white", border_width=1, border_color="#E0E0E0", corner_radius=12)
        card.grid(row=0, column=0, sticky="ew", pady=(0, 20), padx=5)
        card.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(card, text="Departure City", font=("Arial", 14, "bold"), text_color="#555555").grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        dep_input = ctk.CTkEntry(card, placeholder_text="e.g. Lahore", height=40, font=("Arial", 14, "normal"))
        dep_input.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")

        ctk.CTkLabel(card, text="Destination City", font=("Arial", 14, "bold"), text_color="#555555").grid(row=0, column=1, padx=20, pady=(20, 5), sticky="w")
        dest_input = ctk.CTkEntry(card, placeholder_text="e.g. Karachi", height=40, font=("Arial", 14, "normal"))
        dest_input.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="ew")

        status_lbl = ctk.CTkLabel(self.active_view, text="", font=("Arial", 13, "bold"))
        status_lbl.grid(row=1, column=0, pady=5)

        results_container = ctk.CTkFrame(self.active_view, fg_color="transparent")
        results_container.grid(row=2, column=0, sticky="ew")
        results_container.grid_columnconfigure(0, weight=1)

        def execute_search():
            for child in results_container.winfo_children():
                child.destroy()
            
            f_city = dep_input.get().strip().lower()
            t_city = dest_input.get().strip().lower()

            if not f_city or not t_city:
                status_lbl.configure(text="⚠️ Error: Please populate both fields.", text_color="red")
                return

            def RenderCards():
                found = False
                row_idx = 0
                for train in trains:
                    if train["from"].lower() == f_city and train["to"].lower() == t_city:
                        found = True
                        is_full = train["seats"] == 0
                        seat_str = "FULL" if is_full else f"{train['seats']} Left"
                        seat_color = "#E74C3C" if is_full else "#2ECC71"

                        t_card = ctk.CTkFrame(results_container, fg_color="white", corner_radius=10, border_width=1, border_color="#E2E8F0")
                        t_card.grid(row=row_idx, column=0, sticky="ew", pady=8, padx=5)
                        t_card.grid_columnconfigure((0,1,2,3), weight=1)

                        ctk.CTkLabel(t_card, text=f"{train['name']} ({train['id']})", font=("Arial", 16, "bold"), text_color="#333333").grid(row=0, column=0, padx=20, pady=15, sticky="w")
                        ctk.CTkLabel(t_card, text=f"🕒 {train['time']}", font=("Arial", 14, "normal"), text_color="#666666").grid(row=0, column=1, padx=10, pady=15)
                        ctk.CTkLabel(t_card, text=f"Rs. {train['price']}", font=("Arial", 16, "bold"), text_color="#7FA85E").grid(row=0, column=2, padx=10, pady=15)
                        
                        lbl_seats = ctk.CTkLabel(t_card, text=seat_str, font=("Arial", 13, "bold"), text_color="white", fg_color=seat_color, corner_radius=6, width=90, height=28)
                        lbl_seats.grid(row=0, column=3, padx=20, pady=15, sticky="e")
                        row_idx += 1

                if not found:
                    ctk.CTkLabel(results_container, text=f"❌ No matching trains found.", font=("Arial", 14, "bold"), text_color="#777777").grid(row=0, column=0, pady=20)

            self.play_loading_animation(status_lbl, "Showing results below:", RenderCards)

        search_btn = ctk.CTkButton(card, text="Find Available Trains", font=("Arial", 15, "bold"), fg_color="#7FA85E", hover_color="#688B4E", height=42, command=execute_search)
        search_btn.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")

    # =======================================================
    # VIEW 2: BOOK TICKET (Supports Multi-Seat Options)
    # =======================================================
    def show_book_frame(self):
        self.clear_active_view()
        self.set_active_button(self.btn_book)
        self.header_title.configure(text="Book Train Ticket")

        self.active_view = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        self.active_view.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        self.active_view.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(self.active_view, fg_color="white", border_width=1, border_color="#E0E0E0", corner_radius=12)
        card.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card, text="Train ID (e.g. T101)", font=("Arial", 14, "bold"), text_color="#555555").grid(row=0, column=0, padx=20, pady=(20, 2), sticky="w")
        tid_in = ctk.CTkEntry(card, placeholder_text="Enter unique Train ID", height=38, font=("Arial", 14, "normal"))
        tid_in.grid(row=1, column=0, padx=20, pady=(0, 12), sticky="ew")

        ctk.CTkLabel(card, text="Passenger Full Name", font=("Arial", 14, "bold"), text_color="#555555").grid(row=2, column=0, padx=20, pady=(5, 2), sticky="w")
        name_in = ctk.CTkEntry(card, placeholder_text="Enter identity document name", height=38, font=("Arial", 14, "normal"))
        name_in.grid(row=3, column=0, padx=20, pady=(0, 12), sticky="ew")

        ctk.CTkLabel(card, text="CNIC / Passport Number", font=("Arial", 14, "bold"), text_color="#555555").grid(row=4, column=0, padx=20, pady=(5, 2), sticky="w")
        cnic_in = ctk.CTkEntry(card, placeholder_text="xxxxx-xxxxxxx-x", height=38, font=("Arial", 14, "normal"))
        cnic_in.grid(row=5, column=0, padx=20, pady=(0, 12), sticky="ew")

        # Dynamic Multi-Seat Option Configuration 
        ctk.CTkLabel(card, text="Required Seat Quantities", font=("Arial", 14, "bold"), text_color="#555555").grid(row=6, column=0, padx=20, pady=(5, 2), sticky="w")
        
        seat_frame = ctk.CTkFrame(card, fg_color="transparent")
        seat_frame.grid(row=7, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        seats_spin = ctk.CTkComboBox(seat_frame, values=["1", "2", "3", "4", "5", "6"], width=90, height=38, font=("Arial", 14, "bold"))
        seats_spin.set("1")
        seats_spin.pack(side="left")
        
        ctk.CTkLabel(seat_frame, text="* Max 6 allocations per agent subkey transaction.", font=("Arial", 12, "italic"), text_color="#777777").pack(side="left", padx=15)

        status_lbl = ctk.CTkLabel(self.active_view, text="", font=("Arial", 14, "bold"))
        status_lbl.grid(row=1, column=0, pady=15)

        def confirm_booking():
            t_id = tid_in.get().strip().upper()
            p_name = name_in.get().strip()
            p_cnic = cnic_in.get().strip()
            
            try:
                seats_req = int(seats_spin.get())
            except ValueError:
                seats_req = 1

            if not t_id or not p_name or not p_cnic:
                status_lbl.configure(text="⚠️ Complete all entries to reserve seats.", text_color="red")
                return

            selected_train = next((t for t in trains if t["id"] == t_id), None)
            if not selected_train:
                status_lbl.configure(text=f"❌ Request Denied: Train ID '{t_id}' does not exist.", text_color="red")
                return
            if selected_train["seats"] < seats_req:
                status_lbl.configure(text=f"❌ Booking Failure: Only {selected_train['seats']} seats left on this train.", text_color="red")
                return

            def FinishTask():
                booking_id = "BK" + str(random.randint(100000, 999999))
                bookings[booking_id] = {
                    "booking_id": booking_id, "name": p_name, "cnic": p_cnic,
                    "train_id": selected_train["id"], "train_name": selected_train["name"],
                    "from": selected_train["from"], "to": selected_train["to"],
                    "time": selected_train["time"], "price": selected_train["price"],
                    "seats_booked": seats_req,
                    "total_price": selected_train["price"] * seats_req,
                    "status": "Unpaid", "booked_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                selected_train["seats"] -= seats_req
                
                tid_in.delete(0, 'end'); name_in.delete(0, 'end'); cnic_in.delete(0, 'end')
                messagebox.showinfo("Ticket Reserved", f"Success! Booking ID: {booking_id} generated for {seats_req} seats.")
                self.show_bookings_frame()

            self.play_loading_animation(status_lbl, "Reservation successfully saved!", FinishTask)

        btn_submit = ctk.CTkButton(card, text="Reserve Seat Ticket", font=("Arial", 15, "bold"), fg_color="#7FA85E", hover_color="#688B4E", height=42, command=confirm_booking)
        btn_submit.grid(row=8, column=0, padx=20, pady=(0, 25), sticky="ew")

    # =======================================================
    # VIEW 3: PAY FOR TICKET
    # =======================================================
    def show_pay_frame(self):
        self.clear_active_view()
        self.set_active_button(self.btn_pay)
        self.header_title.configure(text="Process Ticket Payment")

        self.active_view = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.active_view.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        self.active_view.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(self.active_view, fg_color="white", border_width=1, border_color="#E0E0E0", corner_radius=12)
        card.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card, text="Enter Booking Reference ID", font=("Arial", 14, "bold"), text_color="#555555").grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        bid_in = ctk.CTkEntry(card, placeholder_text="e.g. BK123456", height=38, font=("Arial", 14, "normal"))
        bid_in.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")

        ctk.CTkLabel(card, text="Select Preferred Gateway Provider", font=("Arial", 14, "bold"), text_color="#555555").grid(row=2, column=0, padx=20, pady=(5, 5), sticky="w")
        method_dropdown = ctk.CTkComboBox(card, values=["JazzCash", "EasyPaisa", "Credit/Debit Card", "Cash Counter"], height=38, font=("Arial", 14, "normal"))
        method_dropdown.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")

        status_lbl = ctk.CTkLabel(self.active_view, text="", font=("Arial", 14, "bold"))
        status_lbl.grid(row=1, column=0, pady=15)

        def run_payment():
            b_id = bid_in.get().strip().upper()
            gate = method_dropdown.get()

            if b_id not in bookings:
                status_lbl.configure(text="❌ Booking reference lookup failed.", text_color="red")
                return
            
            b = bookings[b_id]
            if b["status"] == "Confirmed":
                status_lbl.configure(text="ℹ️ Invoice Alert: Already paid.", text_color="blue")
                return
            if b["status"] == "Cancelled":
                status_lbl.configure(text="❌ Transaction Blocked: Ticket is cancelled.", text_color="red")
                return

            def FinishTask():
                b["status"] = "Confirmed"
                b["txn_id"] = "TXN" + str(random.randint(10000, 99999))
                b["paid_by"] = gate
                bid_in.delete(0, 'end')
                messagebox.showinfo("Payment Finalized", f"Payment Captured via {gate}!")
                self.show_bookings_frame()

            self.play_loading_animation(status_lbl, "Gateway verification approved!", FinishTask)

        btn_pay = ctk.CTkButton(card, text="Authorize Secured Payment", font=("Arial", 15, "bold"), fg_color="#7FA85E", hover_color="#688B4E", height=42, command=run_payment)
        btn_pay.grid(row=4, column=0, padx=20, pady=(0, 25), sticky="ew")

    # =======================================================
    # VIEW 4: CANCEL TICKET
    # =======================================================
    def show_cancel_frame(self):
        self.clear_active_view()
        self.set_active_button(self.btn_cancel)
        self.header_title.configure(text="Cancel Reservation Order")

        self.active_view = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.active_view.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        self.active_view.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(self.active_view, fg_color="white", border_width=1, border_color="#E0E0E0", corner_radius=12)
        card.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card, text="Active Booking Reference ID", font=("Arial", 14, "bold"), text_color="#555555").grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        bid_in = ctk.CTkEntry(card, placeholder_text="e.g. BK123456", height=38, font=("Arial", 14, "normal"))
        bid_in.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")

        status_lbl = ctk.CTkLabel(self.active_view, text="", font=("Arial", 14, "bold"))
        status_lbl.grid(row=1, column=0, pady=15)

        def process_cancellation():
            b_id = bid_in.get().strip().upper()
            if b_id not in bookings:
                status_lbl.configure(text="❌ Booking reference not found.", text_color="red")
                return
            
            b = bookings[b_id]
            if b["status"] == "Cancelled":
                status_lbl.configure(text="ℹ️ Ticket is already cancelled.", text_color="blue")
                return

            if messagebox.askyesno("Confirm Action", f"Are you sure you want to cancel booking {b_id}?"):
                was_paid = b["status"] == "Confirmed"
                b["status"] = "Cancelled"

                for t in trains:
                    if t["id"] == b["train_id"]:
                        t["seats"] += b["seats_booked"]
                        break
                
                ref_msg = "\nRefund will revert back in 3-5 standard working cycles." if was_paid else "\nNo charge incurred."
                bid_in.delete(0, 'end')
                messagebox.showwarning("Order Revoked", f"Booking order {b_id} flagged Void.{ref_msg}")
                self.show_bookings_frame()

        btn_cancel = ctk.CTkButton(card, text="Void Registration Ticket", font=("Arial", 15, "bold"), fg_color="#E74C3C", hover_color="#C0392B", height=42, command=process_cancellation)
        btn_cancel.grid(row=2, column=0, padx=20, pady=(0, 25), sticky="ew")

    # =======================================================
    # VIEW 5: MY BOOKINGS (Yellow Tag Shifted Downward Safely)
    # =======================================================
    def show_bookings_frame(self):
        self.clear_active_view()
        self.set_active_button(self.btn_bookings)
        self.header_title.configure(text="Passenger Booking Ledger")

        self.active_view = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        self.active_view.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        self.active_view.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(self.active_view, fg_color="white", border_width=1, border_color="#E0E0E0", corner_radius=12)
        card.grid(row=0, column=0, sticky="ew", pady=(0, 15), padx=5)
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card, text="Search Passenger Registered Records", font=("Arial", 14, "bold"), text_color="#555555").grid(row=0, column=0, padx=20, pady=(15, 2), sticky="w")
        name_in = ctk.CTkEntry(card, placeholder_text="Provide full traveler name to filter...", height=38, font=("Arial", 14, "normal"))
        name_in.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")

        results_container = ctk.CTkFrame(self.active_view, fg_color="transparent")
        results_container.grid(row=2, column=0, sticky="ew")
        results_container.grid_columnconfigure(0, weight=1)

        def load_ledger_cards(*args):
            for child in results_container.winfo_children():
                child.destroy()

            query = name_in.get().strip().lower()
            found_any = False
            row_idx = 0

            for b in bookings.values():
                if not query or query in b["name"].lower():
                    found_any = True
                    stat = b["status"]
                    bg_col = "#2ECC71" if stat == "Confirmed" else ("#F1C40F" if stat == "Unpaid" else "#E74C3C")

                    b_card = ctk.CTkFrame(results_container, fg_color="white", corner_radius=10, border_width=1, border_color="#E2E8F0")
                    b_card.grid(row=row_idx, column=0, sticky="ew", pady=8, padx=5)
                    b_card.grid_columnconfigure((0, 1), weight=1)

                    # Details Configuration Block Left
                    txt_left = f"🎫 Reference: {b['booking_id']}\n👤 Passenger: {b['name']} (CNIC: {b['cnic']})\n🚂 Train: {b['train_name']} [{b['train_id']}]\n💺 Allocations: {b['seats_booked']} Seats"
                    ctk.CTkLabel(b_card, text=txt_left, font=("Arial", 13, "bold"), justify="left", text_color="#444444").grid(row=0, column=0, padx=20, pady=15, sticky="w")

                    # Right aligned block containing localized route tracking labels 
                    txt_right = f"Route: {b['from']} ➔ {b['to']}\nTime Frame: {b['time']}\nTotal Cost: Rs. {b['total_price']}"
                    ctk.CTkLabel(b_card, text=txt_right, font=("Arial", 13, "normal"), justify="right", text_color="#666666").grid(row=0, column=1, padx=40, pady=15, sticky="e")

                    # FIXED OVERLAP: Placed safely below route details line rather than baseline float layers
                    lbl_status = ctk.CTkLabel(b_card, text=stat.upper(), font=("Arial", 12, "bold"), text_color="white" if stat != "Unpaid" else "black", fg_color=bg_col, corner_radius=6, width=100, height=26)
                    lbl_status.grid(row=0, column=1, padx=40, pady=(85, 10), sticky="se")

                    row_idx += 1

            if not found_any:
                ctk.CTkLabel(results_container, text="📭 No validated bookings found.", font=("Arial", 14, "bold"), text_color="#888888").grid(row=0, column=0, pady=30)

        name_in.bind("<KeyRelease>", load_ledger_cards)
        load_ledger_cards()

    # =======================================================
    # VIEW 6: COMPLAINT FILING
    # =======================================================
    def show_complaint_frame(self):
        self.clear_active_view()
        self.set_active_button(self.btn_complaint)
        self.header_title.configure(text="Customer Service Center")

        self.active_view = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        self.active_view.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        self.active_view.grid_columnconfigure(0, weight=1)

        card = ctk.CTkFrame(self.active_view, fg_color="white", border_width=1, border_color="#E0E0E0", corner_radius=12)
        card.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card, text="Your Full Name", font=("Arial", 14, "bold"), text_color="#555555").grid(row=0, column=0, padx=20, pady=(15, 2), sticky="w")
        cname_in = ctk.CTkEntry(card, placeholder_text="Enter submission name", height=38, font=("Arial", 14, "normal"))
        cname_in.grid(row=1, column=0, padx=20, pady=(0, 12), sticky="ew")

        ctk.CTkLabel(card, text="Booking Reference ID (Optional)", font=("Arial", 14, "bold"), text_color="#555555").grid(row=2, column=0, padx=20, pady=(5, 2), sticky="w")
        cbid_in = ctk.CTkEntry(card, placeholder_text="Leave blank if general issue", height=38, font=("Arial", 14, "normal"))
        cbid_in.grid(row=3, column=0, padx=20, pady=(0, 12), sticky="ew")

        ctk.CTkLabel(card, text="Primary Department Category", font=("Arial", 14, "bold"), text_color="#555555").grid(row=4, column=0, padx=20, pady=(5, 2), sticky="w")
        ctype_in = ctk.CTkComboBox(card, values=["Train Schedule Delay", "Staff Behaviour", "Cleanliness", "Refund Issue", "Other"], height=38, font=("Arial", 14, "normal"))
        ctype_in.grid(row=5, column=0, padx=20, pady=(0, 12), sticky="ew")

        ctk.CTkLabel(card, text="Comprehensive Issue Summary", font=("Arial", 14, "bold"), text_color="#555555").grid(row=6, column=0, padx=20, pady=(5, 2), sticky="w")
        cdesc_in = ctk.CTkEntry(card, placeholder_text="State your problem details clearly...", height=60, font=("Arial", 14, "normal"))
        cdesc_in.grid(row=7, column=0, padx=20, pady=(0, 20), sticky="ew")

        status_lbl = ctk.CTkLabel(self.active_view, text="", font=("Arial", 14, "bold"))
        status_lbl.grid(row=1, column=0, pady=10)

        def log_complaint():
            nm = cname_in.get().strip()
            bk = cbid_in.get().strip().upper()
            tp = ctype_in.get()
            ds = cdesc_in.get().strip()

            if not nm or not ds:
                status_lbl.configure(text="⚠️ Complete Identity and Details boxes.", text_color="red")
                return

            def FinishTask():
                cm_id = "CM" + str(random.randint(10000, 99999))
                complaints[cm_id] = {
                    "complaint_id": cm_id, "name": nm, "booking_id": bk if bk else "N/A",
                    "type": tp, "description": ds, "filed_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "status": "Under Review"
                }
                cname_in.delete(0, 'end'); cbid_in.delete(0, 'end'); cdesc_in.delete(0, 'end')
                messagebox.showinfo("Ticket Escalated", f"Complaint Logged! ID: {cm_id}")
                status_lbl.configure(text="")

            self.play_loading_animation(status_lbl, "Complaint transmitted safely.", FinishTask)

        btn_com = ctk.CTkButton(card, text="File Official Incident Report", font=("Arial", 15, "bold"), fg_color="#7FA85E", hover_color="#688B4E", height=42, command=log_complaint)
        btn_com.grid(row=8, column=0, padx=20, pady=(0, 25), sticky="ew")


# =======================================================
#               SYSTEM APP PROCESS ENTRYPOINT
# =======================================================
if __name__ == "__main__":
    app = RailwayApp()
    app.mainloop()