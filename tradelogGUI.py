from tkinter import *
from tkinter import ttk
from datetime import datetime
import os
global btn 

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

    Button(form_frame, text= " ok",bg="#070525", fg= "#ffffff",command=submit, padx=3, pady= 2, anchor="se").grid(row = 2, column=0)
    
    

def closeT(root, close_trade, open_trades):
    form_frame = Frame(root, border= 2, relief= "groove")
    form_frame.grid(row= 5, column= 1, rowspan= 20)
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
    else:
        Label(form_frame, text= "there are no trades to close!").pack(padx=5, pady=5)

        
    #Entry(form_frame).grid(row=0, column=5)
    #Button(form_frame, text= " ok",bg="#070525", fg= "#ffffff", padx=3, pady= 2).grid(row = 2, column=0)

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
    form_frame.grid(row= 15, column= 20, sticky = "NE")
    #path update
    Label(form_frame, text="enter the path of file(optional):-").pack(padx=10, pady=5)
    e1 = Entry(form_frame)
    e1.pack(padx=10, pady=5)
    #save funtion
    def save_file(tot_profit, trades):
        choice_type_file = type_var.get()

        file_name = f"logs_{str(datetime.now().date())}.{choice_type_file}"
        full_path = os.path.join((e1.get() or ""), file_name)

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
    



