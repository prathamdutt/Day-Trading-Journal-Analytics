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

            
#def close_trade_value_handler():
#    data1 = openT(root)
#
#    if data1 is not None:
#            print(data1)
#            name = data1["name"]
#            price = data1["price"]
#            by_sel = data1["buy/sell"]
#            close_trade(name= name, price= price, b_s= by_sel.lower())
#            print("trade has been set")



#if btn == "o":
#    print("this condition is triggered")
#    data1 = openT(root)
#    if data1 is not None:
#        name = data1["name"]
#        price = data1["price"]
#        by_sel = data1["buy/sell"]
        
#name = input("enter the name of the trade : ")
#price = float(input("enter the price of the trade : "))
#by_sel = input("b or s : ")
#    open_trade(name= name, price= price, b_s= by_sel.lower())
#    print("trade has been set")
#if btn == "c":
#    print("choose the following trades : ")
#    for i in open_trades.keys():
#        print(i)
#    key = input("")
#    price = float(input("enter the price of the trade : "))
#    close_trade(price=price, key=key)
#
#if btn == "v":
#    print(f"here are all open trades currently : ")
#    for n,t in open_trades.items():
#        now = datetime.now()
#        elapse_time = now - datetime.combine(now.date(), t.open_time)
#        print(f" name = {n}, open price = {t.open_price}, time elapsed = {elapse_time.time()} HH:MM:SS")
#
#if btn == "e":
#    tot_profit  = 0
#    with open(f"logs_{str(datetime.now().date())}.txt", "a") as f:
#        f.write(f"\n \ndate = {str(datetime.now().date())}\n")
#        for i in trades.keys():
#            trade = trades[i]
#            data = f"--name = {trade.name}, open_price = {str(trade.open_price)}, close_price = {str(trade.close_price)}, profit = {str(trade.profit_loss)}, b or s = {trade.buy_or_sell}, time = {trade.close_time}\n"
#            f.write(data)
#            tot_profit += trade.profit_loss
#        f.write(f"\ntotal profit/loss for today = {str(tot_profit)}")
                
            #print(f"name = {trade.name}, open_price = {str(trade.open_price)}, close_price = {str(trade.close_price)}, profit = {str(trade.profit_loss)}, b or s = {trade.buy_or_sell}, time = {trade.close_time}")
            
        #print(f"total profit = {str(tot_profit)}")
btn_frame = LabelFrame(root, text= "nav:", border=2, relief= "groove").grid(row= 0, column= 0, rowspan=10)
Button(btn_frame, text="Open Trade", command=lambda r = root : openT(r,open_trade)).grid(row=0, column=0)
Button(btn_frame, text="Close Trade", command=lambda r = root : closeT(r, close_trade, open_trades)).grid(row=3, column=0)
Button(btn_frame, text="View Trade", command=lambda r = root : view(r, open_trades)).grid(row=5, column=0)
Button(btn_frame, text = "End Day!", command=lambda r = root : end(r, trades)).grid(row= 10, column= 0)

root.mainloop()


