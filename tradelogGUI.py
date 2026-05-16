from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime
import os
import csv
import json 



def openT(work_frame, open_trade, work_frames):
    if "open_trade_panels" in work_frames and len(work_frames["open_trade_panels"]) == 3:
        return
    form_frame = Frame(work_frame, border= 2, relief= "groove", bg= "#2b3249")
    form_frame.pack()#place(x=btn_x, y=(btn_y+20))
    
    Label(form_frame, text= "Name = ").grid(row= 0, column=0)
    Label(form_frame, text= "price = ").grid(row= 0, column=5)
    Label(form_frame, text= "buy/sell = ").grid(row= 0, column=10)
    side_frame = Frame(form_frame)
    side_var = StringVar()
    side_var.set("Buy")
   
    entries = {
        "name": Entry(form_frame),
        "price": Entry(form_frame),
        "buy/sell": [Radiobutton(side_frame,text="Buy", variable=side_var, value= "Buy"), Radiobutton(side_frame,text="Sell", variable=side_var, value= "Sell")]
    }

    entries["name"].grid(row=0, column=1)
    entries["price"].grid(row=0, column=6)
    side_frame.grid(row=0, column=11)
    entries["buy/sell"][0].pack()
    entries["buy/sell"][1].pack()
    work_frame.update_idletasks()
    work_frames.setdefault("open_trade_panels", []).append((work_frame.winfo_width(),work_frame.winfo_height()))
    print(work_frames)

    def submit():
        vals = dict()
        for  i,j in entries.items():
            if i != "buy/sell":
                vals[i] = j.get()
        form_frame.destroy()
        open_trade(name = vals["name"], price = vals["price"], b_s = side_var.get())
        work_frames["open_trade_panels"].pop()
        print(work_frames)
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
        print(work_frames)

    Button(form_frame, text= " ok",bg="#070525", fg= "#ffffff",command=submit, padx=3, pady= 2, anchor="se").grid(row = 2, column=0)
    #cancel button
    Button(form_frame, text= "cancel", bg="#c45c5c", fg= "#ffffff", command= cancel).grid(row = 4, column=0)
    

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
            form_frame.destroy()
        def on_select(val):
            if val not in entries:
                Label(entry_frame, text= f"enter the closing price of {val}:-").pack(padx=5, pady=5)
                e = Entry(entry_frame)
                e.pack(padx=10, pady=5)
                entries[val] = e

        Label(form_frame, text= "choose the following trades : ").pack(padx=5, pady=5)
        r = StringVar()
        for n in open_trades.keys():
            
            #button append to entries
            Radiobutton(form_frame, text=n, variable = r, value = n, command= lambda val = n: on_select(val) ).pack(padx=5, pady=5, anchor="w")
        entry_frame = Frame(form_frame, border= 2, relief="groove", bg="#252a3b")
        entry_frame.pack(padx=5, pady=5)
        Button(form_frame, text= "ok", bg="#040a61", fg= "#ffffff", command=submit).pack(padx=5,pady=5)
        #cancel buton
        def cancel():
            for i in entries.values():
                i.delete(0, 'end')
            entries.clear()
            form_frame.destroy()
            work_frames.pop("close_trade_panel", None)
            print(work_frames)

        Button(form_frame, text= "cancel", bg="#c45c5c", fg= "#ffffff", command=cancel).pack(padx=5,pady=5)
        work_frame.update_idletasks()
        work_frames.setdefault("close_trade_panel", (form_frame.winfo_x(), form_frame.winfo_y()))
        print(work_frames)
    else:
        def clean_cross():
            work_frames.pop("close_trade_panel", None)
            print(work_frames)
            form_frame.destroy()

        Label(form_frame, text= "there are no trades to close!").pack(padx=5, pady=5)
        Button(form_frame, text= "X", fg="#ffffff", bg="#c45c5c", command=clean_cross).pack(anchor="ne")

        work_frame.update_idletasks()
        work_frames.setdefault("close_trade_panel", (form_frame.winfo_x(), form_frame.winfo_y()))
        print(work_frames)

        

def view(root, open_trades, workframes):
 
    form_frame = Frame(root, border= 2, relief= "groove")
    form_frame.place(relx= 0.6, rely= 0, anchor = "nw")
    Label(form_frame, text="all the trades are viewd here:-").pack(padx=10, pady=5)
    for n,t in open_trades.items():
        now = datetime.now()
        elapse_time = now - datetime.combine(now.date(), t.open_time)
        Label(form_frame, text=f" name = {n}, open price = {t.open_price}, side = {t.buy_or_sell}, time elapsed = {elapse_time} HH:MM:SS").pack(padx= 10, pady=1)
    form_frame.update_idletasks()
    workframes["view_trades_panel"] = (form_frame.winfo_width(), form_frame.winfo_height())



def end(root, trades, work_frame, work_frames):
    tot_profit  = 0
    choice_path = None
    choice_type_file = "txt"
    

    form_frame = Frame(root, border= 2, relief= "groove")
    work_frame.update_idletasks()
    #x= workframe width and y = view panel hieght
    form_frame.place(relx=1, anchor="ne", y = work_frames["view_trades_panel"][1] +10 if "view_trades_panel" in work_frames else 0)#grid(row= 30, column= 1)
    #path update
    Label(form_frame, text=" please choose or enter the path of file:-").pack(padx=10, pady=5)
    e1 = Entry(form_frame)
    e1.pack(padx=10, pady=5)

    #browse file system
    save_dir = StringVar(value="")

    def browse():
        save_dir.set(filedialog.askdirectory())
        print("save directory : ", save_dir.get())
        
    browse = ttk.Button(form_frame, text= "Browse", style= "Browse.TButton", command=browse)
    browse.pack()
    
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
                         "time" : str(t.close_time)

                         } 
                entries.append(entry) 
            if os.path.exists(full_path):
                with open(full_path, "r") as file:
                    data = json.load(file)
            else:
                data = {
                    "entries" : []
                }
            for e in entries:
                exists = any(i["id"] == e["id"] for i in data["entries"])
                if not exists:
                    data["entries"].append(e)
                else:
                    print("some duplicates are skipped")
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
                 foreground="#ffffff",
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


#live sim for analytics panel (FOR FUTURE UPGRADE)


#calucations
def calculate_ananlytics(trades):
    profits = [t.profit_loss for t in trades.values()]
    total_pnl = sum(profits)
    wins = [p for p in profits if p > 0]
    losses = [p for p in profits if p < 0]
    avg_wins = sum(wins)/len(wins) if wins else 0
    avg_losses = sum(losses)/len(losses) if losses else 0
    win_rate = (len(wins)/len(profits) * 100) if profits else 0
    
    return win_rate, total_pnl, avg_wins, avg_losses
    
def update_analytics(trades, analytics_widgets):
        if not trades:
            return
        win_rate, total_pnl, avg_wins, avg_losses = calculate_ananlytics(trades)
        analytics_widgets["win_rate_label"].config(text= f"win rate = {win_rate}%")
        analytics_widgets["PnL_label"].config(text= f"total P/L = {total_pnl}")
        analytics_widgets["avg_win"].config(text= f"avg wins = {avg_wins}")
        analytics_widgets["avg_loss"].config(text= f"avg loss = {avg_losses}")
        analytics_widgets["tot_trades"].config(text= f"total trades = {len(trades)}")
