from datetime import datetime
import uuid
from tradelogGUI import*
from tkinter import *

root = Tk()


class Trade:
    def __init__(self, name ,buy_or_sell, open_price):
        now = datetime.now()
        self.open_time = now.time()
        self.close_time = None
        self.date = now.date()
        self.buy_or_sell = buy_or_sell
        self.name = str(name)
        self.open_price = float(open_price)
        self.close_price = 0
        self.profit_loss = 0
        self.id = uuid.uuid4().hex
        
    def P_L(self):
        if self.buy_or_sell in "Bb":
            self.profit_loss = self.close_price - self.open_price
            return self.profit_loss
        if self.buy_or_sell in "Ss":
            self.profit_loss = self.open_price - self.close_price
            
            return self.profit_loss
        
    def close(self, price):
        self.close_price = price
        self.close_time = datetime.now().time()
        print("trade has been close.")
        print("profit/loss = ", self.P_L())
trades = {}   
open_trades = {}


def close_trade(price, key):
    if open_trades.get(key) == None:
        raise ValueError("there are no trades open of this company")
    open_trades[key].close(price)
    del open_trades[key]
    
    

def open_trade(name, price, b_s):
    if name in open_trades:
        raise ValueError("Trade already open")
    trade =  Trade(name=name, buy_or_sell= b_s, open_price= price)
    trades[trade.id] =  trade
    open_trades[name] = trade 
    print("trade has been set.")

            

btn_frame = LabelFrame(root, border=2, relief= "groove", text= "nav: ")
btn_frame.grid(row= 0, column= 0)
Button(btn_frame, text="Open Trade", command=lambda r = root : openT(r,open_trade)).pack()
Button(btn_frame, text="Close Trade", command=lambda r = root : closeT(r, close_trade, open_trades)).pack()
Button(btn_frame, text="View Trade", command=lambda r = root : view(r, open_trades)).pack()
Button(btn_frame, text = "End Day!", command=lambda r = root : end(r, trades)).pack()

#nalytics
analytic_frame = LabelFrame(root, border= 2, relief= "groove", text="anlaytics dash board (not operable)")
analytic_frame.grid(row= 20, column= 0, sticky = "W")

#labels NOT OPERABLE (FOR LATER UPGRADE)
win_rate_label = Label(analytic_frame, text = "win rate = 0%")
PnL_label = Label(analytic_frame, text = " total P/L = 0")
avg_win = Label(analytic_frame, text = "avg wins = 0")
avg_loss = Label(analytic_frame, text = "avg losses = 0")
tot_trades = Label(analytic_frame, text = f"tot. Trades = {len(trades)}")
win_rate_label.pack()
PnL_label.pack()
avg_win.pack()
avg_loss.pack()
tot_trades.pack()

root.mainloop()


