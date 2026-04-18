from tkinter import *
from tkinter import ttk
from datetime import datetime
import os
import csv
import json 

def openT(root, open_trade):
    
    form_frame = Frame(root, border= 2, relief= "groove")
    form_frame.grid(row= 0, column= 1, rowspan=2)
    Label(form_frame, text= "Name = ").grid(row= 0, column=0)
    Label(form_frame, text= "price = ").grid(row= 0, column=5)
    Label(form_frame, text= "buy/sell = ").grid(row= 0, column=10)

    entries = {
        "name": Entry(form_frame),
        "price": Entry(form_frame),
        "buy/sell": Entry(form_frame)
    }

    entries["name"].grid(row=0, column=1)
    entries["price"].grid(row=0, column=6)
    entries["buy/sell"].grid(row=0, column=11)

    def submit():
        vals = dict()
        for  i,j in entries.items():
            vals[i] = j.get()
        form_frame.destroy()
        btn = None
        open_trade(name = vals["name"], price = vals["price"], b_s = vals["buy/sell"])
    #cancel logic
    def cancel():
        for i in entries.values():
            i.delete(0, 'end')
        entries.clear()
        form_frame.destroy()

    Button(form_frame, text= " ok",bg="#070525", fg= "#ffffff",command=submit, padx=3, pady= 2, anchor="se").grid(row = 2, column=0)
    #cancel button
    Button(form_frame, text= "cancel", bg="#c45c5c", fg= "#ffffff", command= cancel).grid(row = 4, column=0)
    

def closeT(root, close_trade, open_trades):
    form_frame = Frame(root, border= 2, relief= "groove")
    form_frame.grid(row= 10, column= 1)
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
        entry_frame = Frame(form_frame, border= 2, relief="groove")
        entry_frame.pack(padx=5, pady=5)
        Button(form_frame, text= "ok", bg="#040a61", fg= "#ffffff", command=submit).pack(padx=5,pady=5)
        #cancel buton
        def cancel():
            for i in entries.values():
                i.delete(0, 'end')
            entries.clear()
            form_frame.destroy()

        Button(form_frame, text= "cancel", bg="#c45c5c", fg= "#ffffff", command=cancel).pack(padx=5,pady=5)
    else:
        Label(form_frame, text= "there are no trades to close!").pack(padx=5, pady=5)

        

def view(root, open_trades):
 
    form_frame = Frame(root, border= 2, relief= "groove")
    form_frame.grid(row= 10, column= 10, sticky = "NE")
    Label(form_frame, text="all the trades are viewd here:-").pack(padx=10, pady=5)
    for n,t in open_trades.items():
        now = datetime.now()
        elapse_time = now - datetime.combine(now.date(), t.open_time)
        Label(form_frame, text=f" name = {n}, open price = {t.open_price}, time elapsed = {elapse_time} HH:MM:SS").pack(padx= 10, pady=1)

def end(root, trades):
    tot_profit  = 0
    choice_path = None
    choice_type_file = "txt"
    

    form_frame = Frame(root, border= 2, relief= "groove")
    form_frame.grid(row= 30, column= 1)
    #path update
    Label(form_frame, text="enter the path of file(optional):-").pack(padx=10, pady=5)
    e1 = Entry(form_frame)
    e1.pack(padx=10, pady=5)
    #save funtion
    def save_file(tot_profit, trades):
        choice_type_file = type_var.get()

        file_name = f"logs_{str(datetime.now().date())}.{choice_type_file}"
        full_path = os.path.join((e1.get() or ""), file_name)

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
        if choice_type_file == "csv":

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
    avg_wins = sum(wins)/len(wins)
    avg_losses = sum(losses)/len(losses)
    win_rate = (len(wins)/len(profits) * 100) if profits else 0

    #def update_analytics(trades):
    #    win_rate, total_pnl, avg_wins, avg_losses = calculate_ananlytics(trades)
    #    win_rate_label.config(text= f"win rate = {win_rate}%")
    #    PnL_label.config(text= f"total P/L = {total_pnl}")
    #    avg_win.config(text= f"avg wins = {avg_wins}%")
    #    avg_loss.config(text= f"win rate = {avg_losses}%")
    #    tot_trades.config(text= f"win rate = {len(trades)}%")
    
    return win_rate, total_pnl, avg_wins, avg_losses
    

