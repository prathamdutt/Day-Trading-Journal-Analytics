from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime
import threading
import os
import sys
import csv
import json
import requests

def get_base_path():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

config_path = os.path.join(get_base_path(), "config.json")
with open(config_path, "r") as f:
    config = json.load(f)

server_url = config.get("cloudflare_url") or config["local_host"]
ENDPOINTS = [
    "https://www.google.com",
    "https://www.microsoft.com",
    "https://www.apple.com",
]
def request_recieve(symbol):
    with open(config_path, "r") as f:
        AUTH_TOKEN = json.load(f)["Authorization"]
    headers = {
        "Authorization" : AUTH_TOKEN

    }
    print(f"{server_url}/feature")
    reply = requests.post(f"{server_url}/feature", json={"SYMBOL": symbol},
                          headers= headers)
    if reply.status_code == 404 or reply.status_code == 401:
        return 0
    else:
        return reply.json()

def has_internet(timeout=3):
    for i in ENDPOINTS:
        try:
            requests.get(i, timeout=timeout)
            return True
        except requests.RequestException:
            continue
    try:
        r = requests.get("https://cp.cloudflare.com/generate_204", timeout=3)
        return r.status_code == 204
    except requests.RequestException:
        return False
def check_api_feature(btn):
    
    btn.config(state = DISABLED)
    def worker():
        if (has_internet() and server_is_on()) == False:
            btn.after(0, lambda : btn.config(state = DISABLED))
        else:
            btn.after(0, lambda : btn.config(state = NORMAL))
    threading.Thread(target=worker, daemon=True).start()

def server_is_on():
    try:
        r = requests.get(f"{server_url}/health", timeout=5)
        return r.status_code == 200

    except requests.exceptions.RequestException:
        return False

def search_price(symbol ,entry, price_type = "NSE"):
    if hasattr(symbol, "get"):
        symbol = symbol.get()
    entry.delete(0, END)
    entry.insert(0, "searching...")
    
    if symbol == "":
        entry.delete(0, END)
        entry.insert(0, "none")
        return
    
    def worker():
        try:
            result = request_recieve(symbol)
            if result == 0:
               
                entry.after(
                    0, lambda : (
                        entry.delete(0, END),
                        entry.insert(0, "")))

            if result != 0:
                entry.after(
                    0,
                    lambda: (
                        entry.delete(0, END),
                        entry.insert(0, float(result[price_type]))
                    )
                )
            
                

        except Exception as e:
            print("WORKER ERROR:", e)
    threading.Thread(target = worker, daemon = True).start()

def openT(work_frame, open_trade, work_frames):
    if "open_trade_panels" in work_frames and len(work_frames["open_trade_panels"]) == 3:
        return
    form_frame = Frame(work_frame, border= 2, relief= "groove", bg= "#2b3249")
    form_frame.pack()#place(x=btn_x, y=(btn_y+20))
    
    Label(form_frame, text= " Name =",
          font=("Terminal", 11),
           bg= "#2b3249",fg='#ffffff'
          ).grid(row= 0, column=0)
    Label(form_frame, text= " price =",
          font=("Terminal", 11),
           bg= "#2b3249",fg='#ffffff').grid(row= 0, column=5)
    Label(form_frame, text= " buy/sell =",
          font=("Terminal", 11),
           bg= "#2b3249",fg='#ffffff').grid(row= 0, column=10)
    side_frame = Frame(form_frame)
    side_var = StringVar()
    side_var.set("Buy")
   
    entries = {
        "name": Entry(form_frame, bg="#0C0A25",
                      fg= "#ffffff", insertbackground='white', bd=5,
                      relief="sunken"),
        "price": Entry(form_frame, bg="#0C0A25",
                      fg= "#ffffff", insertbackground='white', bd=5,
                      relief="sunken"),
        "buy/sell": [Radiobutton(side_frame,
                                text="Buy", variable=side_var, value= "Buy",
                                font=("Terminal", 11), bg= "#2b3249", 
                                fg='#ffffff', activebackground="#2b3249", activeforeground="#ffffff",
                                selectcolor="#2b3249", width=10, anchor="nw"), 
                     Radiobutton(side_frame,
                                text="Sell", variable=side_var, value= "Sell",
                                bg= "#2b3249", font=("Terminal", 11), 
                                fg='#ffffff', activebackground="#2b3249", activeforeground="#ffffff",
                                selectcolor="#2b3249", width=10, anchor="nw")],
        
    }
    api_price_btn = Button(form_frame, text="Search for Stock Price", bg = "#2c2aa5", fg= "#ffffff", command= lambda x = entries["name"], y = entries["price"] : search_price(x, y))
    entries["name"].grid(row=0, column=1)
    entries["price"].grid(row=0, column=6)
    form_frame.update_idletasks()
    api_price_btn.place(anchor = "nw", x=entries["price"].winfo_x(), y=entries["price"].winfo_y()+entries["price"].winfo_height()+10)
    check_api_feature(api_price_btn)
    side_frame.grid(row=0, column=11)
    entries["buy/sell"][0].pack()
    entries["buy/sell"][1].pack()
    work_frame.update_idletasks()
    work_frames.setdefault("open_trade_panels", []).append((work_frame.winfo_x(), work_frame.winfo_x() ,work_frame.winfo_width(),work_frame.winfo_height()))
    

    def submit():
        vals = dict()
        for  i,j in entries.items():
            if i != "buy/sell":
                vals[i] = j.get()
        form_frame.destroy()
        open_trade(name = vals["name"], price = vals["price"], b_s = side_var.get())
        work_frames["open_trade_panels"].pop()
        
    #cancel logic
    def cancel():
        for i in entries.values():
            if isinstance(i, list):
                i[0].destroy()
                i[1].destroy()
                continue
            i.delete(0, 'end')
        entries.clear()
        form_frame.destroy()
        work_frames["open_trade_panels"].pop()
        

    Button(form_frame, text= " ok",bg="#070525", fg= "#ffffff",command=submit, padx=3, pady= 2, anchor="center", width=5,
           font=("Terminal", 9),).grid(row = 2, column=0)
    #cancel button
    Button(form_frame, text= "cancel", bg="#c45c5c", fg= "#ffffff", command= cancel, 
           font=("Terminal", 9), width=5, anchor="center").grid(row = 4, column=0)


def closeT(work_frame, close_trade, open_trades, work_frames):
    if "close_trade_panel" in work_frames:
        return
    form_frame = Frame(work_frame, border= 2, relief= "groove", bg= "#6a7083")
    form_frame.pack()#.grid(row= 10, column= 1)
    if open_trades:
        entries = dict()

        def submit():
            for i,j in entries.items():
                val = float(j.get())
                close_trade(val, i)
            work_frames.pop("close_trade_panel", None)
            form_frame.destroy()
        def on_select(val):
            if val not in entries:
                Label(entry_frame, text= f"enter the closing price of {val}:-", font=("Terminal", 11),
           bg= "#2b3249",fg='#ffffff').pack(padx=5, pady=5)
                e = Entry(entry_frame,  bg="#0C0A25",
                      fg= "#ffffff", insertbackground='white', bd=5,
                      relief="sunken")
                e.pack(padx=10, pady=5)
                entries[val] = e

        Label(form_frame, text= "choose the following trades : ", font=("Terminal", 11),
           bg= "#2b3249",fg='#ffffff').pack(padx=5, pady=5)
        r = StringVar()
        for n in open_trades.keys():
            
            #button append to entries
            Radiobutton(form_frame, text=n, variable = r, value = n, command= lambda val = n: on_select(val), bg= "#2b3249", font=("Terminal", 11), 
                                fg='#ffffff', activebackground="#2b3249", activeforeground="#ffffff",
                                selectcolor="#2b3249", width=10, anchor="nw" ).pack(padx=5, pady=5, anchor="w")
        entry_frame = Frame(form_frame, border= 2, relief="groove", bg="#252a3b")
        entry_frame.pack(padx=5, pady=5)

        # api button
        def process_all_entries():
            print(entries)
            for s,e in entries.items():
                search_price(s, e)
        api_price_btn = Button(entry_frame, text="Search for Stock Price", bg = "#2c2aa5", fg= "#ffffff", command= process_all_entries)
        api_price_btn.pack(anchor = "ne")
        check_api_feature(api_price_btn)

        Button(form_frame, text= "ok", bg="#040a61", fg= "#ffffff", command=submit).pack(padx=5,pady=5)
        #cancel buton
        def cancel():
            for i in entries.values():
                i.delete(0, 'end')
            entries.clear()
            form_frame.destroy()
            work_frames.pop("close_trade_panel", None)
            

        Button(form_frame, text= "cancel", bg="#c45c5c", fg= "#ffffff", command=cancel).pack(padx=5,pady=5)
        work_frame.update_idletasks()
        work_frames.setdefault("close_trade_panel", (form_frame.winfo_x(), form_frame.winfo_y()))
        
    else:
        def clean_cross():
            work_frames.pop("close_trade_panel", None)
            
            form_frame.destroy()

        Label(form_frame, text= "there are no trades to close!", font=("Terminal", 11),
           bg= "#2b3249",fg='#ffffff').pack(padx=5, pady=5)
        Button(form_frame, text= "X", fg="#ffffff", bg="#c45c5c", command=clean_cross).pack(anchor="ne")

        work_frame.update_idletasks()
        work_frames.setdefault("close_trade_panel", (form_frame.winfo_x(), form_frame.winfo_y()))

        

def view(root, open_trades, workframes):
    if "view_trades_panel" in workframes:
        return

    def clean_cross():
            workframes.pop("view_trades_panel", None)
            form_frame.destroy()
 
    form_frame = LabelFrame(root, text= "All current trades are viewed here:-", fg="#ffffff", font=("Terminal", 15, 'bold'), border=3, relief="groove", bg="#1b1919")
    root.update_idletasks()
    pos = workframes["open_trade_panels"][-1][0] + workframes["open_trade_panels"][-1][2] + 5 if "open_trade_panels" in workframes and workframes["open_trade_panels"] != [] else workframes["idle_cor"][0] + workframes["idle_width"] + 5
    
    Button(form_frame, text= "X", fg="#ffffff", bg="#c45c5c", command=clean_cross).pack(anchor="ne")
    null = None
    if not open_trades:
        null = Label(form_frame, text=" ", bg="#1b1919")
        null.pack(padx=10, pady=5)
    for n,t in open_trades.items():
        now = datetime.now()
        elapse_time = now - datetime.combine(now.date(), t.open_time)
        Label(form_frame, text=f"$- name = {n}, open price = {t.open_price}, side = {t.buy_or_sell}, time elapsed = {elapse_time} HH:MM:SS",
               bg="#1b1919", fg="#ffffff", font=('Terminal', 10), wraplength= root.winfo_width() - pos - 15).pack(padx= 10, pady=5, anchor="w")
    form_frame.update_idletasks()
    
    form_frame.place(x= pos, y= 0, width= min(form_frame.winfo_reqwidth(), root.winfo_width() - pos - 10), anchor = "nw")
    form_frame.update_idletasks()
    workframes["view_trades_panel"] = (form_frame.winfo_width(), form_frame.winfo_height())
    



def end(root, trades, work_frame, work_frames):
    tot_profit  = 0
    choice_path = None
    choice_type_file = "txt"
    

    form_frame = Frame(root, border= 2, relief= "groove", bg="#1b1919")
    work_frame.update_idletasks()
    #x= workframe width and y = view panel hieght
    form_frame.place(relx=1, anchor="ne", y = work_frames["view_trades_panel"][1] +10 if "view_trades_panel" in work_frames else 0)#grid(row= 30, column= 1)
    #path update
    Label(form_frame, text="Please choose or enter the path:-",
          font=("Terminal", 11),
           bg= "#1b1919",fg='#ffffff').pack(padx=10, pady=5)
    e1 = Entry(form_frame,
                bg="#0C0A25",
                fg= "#ffffff", insertbackground='white', bd=5,
                relief="sunken")
    e1.pack(padx=10, pady=5)

    #browse file system
    save_dir = StringVar(value="")

    def browse():
        save_dir.set(filedialog.askdirectory())
        
    browse_b = ttk.Button(form_frame, text= "Browse", style= "Browse.TButton", command=browse)
    browse_b.pack()
    
    
    #save funtion
    def save_file(tot_profit, trades):
        choice_type_file = type_var.get()
        

        file_name = f"logs_{str(datetime.now().date())}.{choice_type_file}"
        
        #path to save the files at
        if save_dir.get():
            dir = os.path.join(save_dir.get(), "tradelogs")
            os.makedirs(dir, exist_ok=True)
            full_path = os.path.join(dir, file_name)
        elif e1.get() and not save_dir.get():
            try:
                dir = os.path.join(e1.get(), "tradelogs")
                os.makedirs(dir, exist_ok=True)
            except (OSError, ValueError):
                messagebox.showerror("invalid Path!!", "invalid path provided, please try a valid path again.")
                return
            full_path = os.path.join(dir, file_name)
        else:
            dir = os.path.join(os.path.expanduser("~"), "tradelogs")
            os.makedirs(dir, exist_ok=True)
            full_path = os.path.join(dir, file_name)
            
            

        #for CSV file
        if choice_type_file == "csv":
            with open(full_path, "w", newline="", encoding="utf-8") as f:
                field_names = ["name", "open_price", "close_price", "profit", "b or s", "time"]
                data = [
                    [trade.name, trade.open_price, trade.close_price, trade.profit_loss, trade.buy_or_sell, trade.close_time] for trade in trades.values()
                ]
                writer = csv.writer(f)
                writer.writerow(field_names)
                writer.writerows(data)


        #JSON file
        if choice_type_file == "json":
            entries = []
            for t in trades.values():

                entry = {"id": str(t.id),
                         "name" : t.name,
                         "open_price" : t.open_price,
                         "profit" : t.profit_loss,
                         "b or s" : t.buy_or_sell,
                         "entry_time" : str(t.open_time),
                         "exist_time" : str(t.close_time)
                         } 
                entries.append(entry) 

            #if json already exists
            if os.path.exists(full_path):
                with open(full_path, "r") as file:
                    data = json.load(file)
                    data["Accurate_analytics"] = "False"
            #if there is no existing log, brand new json
            else:
                analysis = calculate_ananlytics(trades)
                data = {
                    "entries" : [],
                    "total_trades" : len(trades),
                    "win_rate" : analysis["win_rate"],
                    "total_pnl" : analysis["total_pnl"],
                    "avg_wins" : analysis["avg_wins"],
                    "avg_losses" : analysis["avg_losses"],
                    "comment" : "if the trade/trades that are added later then the analytics are not accurate from that point!!",
                    "Accurate_analytics" : "True",
                    "status" : "True"
                }#for now it does not support the udating analytics for json
            for e in entries:
                exists = any(i["id"] == e["id"] for i in data["entries"])
                if not exists:
                    data["entries"].append(e)
                else:
                    pass
            
            with open(full_path, "w") as file:
                json.dump(data, file, indent=2)
                


        #for txt file 
        if choice_type_file == "txt":

            with open(full_path, "a") as f:
                f.write(f"\n \ndate = {str(datetime.now().date())}\n")
                for i in trades.keys():
                    trade = trades[i]
                    data = f"--name = {trade.name}, open_price = {str(trade.open_price)}, close_price = {str(trade.close_price)}, profit = {str(trade.profit_loss)}, b or s = {trade.buy_or_sell}, time = {trade.close_time}\n"
                    f.write(data)
                    tot_profit += trade.profit_loss
                f.write(f"\ntotal profit/loss for today = {str(tot_profit)}")
        
        root.destroy()
    

    #file type drop 
    type_var = StringVar(value= "txt")
    ttk.Combobox(form_frame, 
                 textvariable= type_var,
                 foreground="#000000",
                 background="#2b3249",
                 values= ["txt", "csv", "json"],
                 state= "readonly"
                 ).pack(pady=10)


    #save button
    Button(form_frame, text= "save", command= lambda : save_file(trades= trades, tot_profit= tot_profit), fg="#ffffff", bg="#4648a5").pack(pady=10)
    #cancel button
    def cancel():
        e1.delete(0, 'end')
        form_frame.destroy()
    Button(form_frame, text= "cancel", bg="#c45c5c", fg= "#ffffff", command=cancel).pack(padx=5,pady=5)
    
    Label(form_frame, text="(Note: by default the path is C:/Users/<username>/tradelogs)",
          font=("Terminal", 7),
           bg= "#1b1919",fg='#ffffff').pack()
    form_frame.update_idletasks()
    Label(form_frame, text="(warning! : - make sure the there is file of the same date currently in the folder)",
          font=("Terminal", 7), wraplength= form_frame.winfo_width(),
           bg= "#1b1919",fg='#ffffff').pack()
    Label(form_frame, text="(warning! : the APP will close after you press save button)",
          font=("Terminal", 7),
           bg= "#1b1919",fg="#fa0505").pack()


#connection status
def connection_status(l1,l2):
    l1.config(text="...", fg = '#ffffff')
    l2.config(text="...", fg = '#ffffff')
    def worker():
        if not has_internet():
            status = ("OFF", "#e00101", "OFF", "#e00101")
        elif server_is_on():
            status = ("ON", "#00df38", "ON", "#00df38")
        else:
            status = ("ON", "#00df38", "OFF", "#e00101")
        l1.after(
            0,
            lambda :(
                l1.config(text = status[0], fg = status[1]),
                l2.config(text = status[2], fg = status[3])
            ))
    threading.Thread(target=worker, daemon=True).start() 
    

#live sim for analytics panel (FOR FUTURE UPGRADE)


#calucations
def calculate_ananlytics(trades):
    profits = [t.profit_loss for t in trades.values()]
    wins = [p for p in profits if p > 0]
    losses = [p for p in profits if p < 0]
    result = {
        "total_pnl" : sum(profits),
        "avg_wins" : sum(wins)/len(wins) if wins else 0,
        "avg_losses" : sum(losses)/len(losses) if losses else 0,
        "win_rate" : (len(wins)/len(profits) * 100) if profits else 0,
        "total_trades" : len(trades)


    }
    
    return result
    
def update_analytics(trades, analytics_widgets):
        if not trades:
            return
        a = calculate_ananlytics(trades)
        analytics_widgets["win_rate_label"].config(text= f"win rate = {a["win_rate"]}%")
        analytics_widgets["PnL_label"].config(text= f"total P/L = {a["total_pnl"]}")
        analytics_widgets["avg_win"].config(text= f"avg wins = {a["avg_wins"]}")
        analytics_widgets["avg_loss"].config(text= f"avg loss = {a["avg_losses"]}")
        analytics_widgets["tot_trades"].config(text= f"total trades = {len(trades)}")
