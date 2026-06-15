from datetime import datetime
import uuid
from utility import*
from tkinter import *


root = Tk()
root.geometry("1200x1000")
bg_default = '#1b1919'
root.config(bg= bg_default)
style = ttk.Style()
#print(style.theme_names())
style.theme_use("alt")
style.configure('Browse_b.TButton', font =
               ('calibri', 10, 'bold'),
                foreground = 'white', background= "#171855")
icon_path = os.path.join(get_base_path(), "icons", "Untitled5_20260614152344.ico")
root.iconbitmap(icon_path)
root.title("TRADE LOGGER")


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
        if self.buy_or_sell == "Buy":
            self.profit_loss = self.close_price - self.open_price
            return self.profit_loss
        if self.buy_or_sell == "Sell":
            self.profit_loss = self.open_price - self.close_price
            
            return self.profit_loss
        
    def close(self, price):
        self.close_price = price
        self.close_time = datetime.now().time()
        self.P_L()
trades = {}   
open_trades = {}


def close_trade(price, key):
    if open_trades.get(key) == None:
        raise ValueError("there are no trades open of this company")
    open_trades[key].close(price)
    del open_trades[key]
    update_analytics(trades=trades, analytics_widgets=analytics_widgets)
    
    

def open_trade(name, price, b_s):
    if name in open_trades:
        raise ValueError("Trade already open")
    trade =  Trade(name=name, buy_or_sell= b_s, open_price= price)
    trades[trade.id] =  trade
    open_trades[name] = trade 
    update_analytics(trades=trades, analytics_widgets=analytics_widgets)
    


#frame for work area
work_frame = LabelFrame(root,text="you'll be working here...",fg="#ffffff", font=("Terminal", 15, 'bold'), border=3, relief="groove", bg="#1b1919")
work_frames = {}

#frame for buttons
btn_frame = LabelFrame(root, border=2, relief= "groove", text= "NAV: ", font=('Terminal', 20, 'bold'), fg= "#ddf08b", 
                       bg= "#6a7083")
btn_frame.place(relx= 0, rely= 0.001)


Button(btn_frame, text="Open Trade", width= 20, height= 2,font =
               ('calibri', 12, 'bold'),bg= "#B686EE" , command=lambda r = work_frame : openT(r,open_trade, work_frames=work_frames)).pack()
Button(btn_frame, text="Close Trade",bg= "#B686EE" , width= 20, height= 2,font =
               ('calibri', 12, 'bold'), command=lambda r = work_frame : closeT(r, close_trade, open_trades, work_frames=work_frames )).pack()
Button(btn_frame, text="View Trade",bg= "#B686EE" , width= 20, height= 2,font =
               ('calibri', 12, 'bold'), command=lambda r = root : view(r, open_trades, workframes= work_frames)).pack()
Button(btn_frame, text = "End Day!",bg= "#B686EE" , width= 20, height= 2,font =
               ('calibri', 12, 'bold'), command=lambda r = root : end(r, trades, work_frame=work_frame, work_frames=work_frames)).pack()

 
root.update_idletasks() 
work_frame.place(x= btn_frame.winfo_width() + 10, y=0) 
Label(work_frame, text=" ", bg="#1b1919").pack()
root.update_idletasks()
work_frames["idle_width"] = work_frame.winfo_width()

work_frames["idle_cor"] = (work_frame.winfo_x(), work_frame.winfo_y())



#nalytics frame
analytic_frame = LabelFrame(root, border= 2, relief= "groove", text="Analytics Dash Board", bg="#1b1919", fg="#ffffff",
                            font= ('Terminal', 15, 'bold'))
analytic_frame.place(relx= 0, rely= 0.8)

#analytics 
analytics_widgets = {
    "win_rate_label" : Label(analytic_frame, text = "win rate = 0%", bg="#1b1919", fg="#ffffff", font=('Terminal', 10)),
    "PnL_label" : Label(analytic_frame, text = " total P/L = 0", bg="#1b1919", fg="#ffffff", font=('Terminal', 10)),
    "avg_win" : Label(analytic_frame, text = "avg wins = 0", bg="#1b1919", fg="#ffffff", font=('Terminal', 10)),
    "avg_loss" : Label(analytic_frame, text = "avg losses = 0", bg="#1b1919", fg="#ffffff", font=('Terminal', 10)),
    "tot_trades" : Label(analytic_frame, text = f"tot. Trades = {len(trades)}", bg="#1b1919", fg="#ffffff", font=('Terminal', 10))
}
#refresh buttn
refresh_btn = Button(analytic_frame, text="⟲", bg = "#7854CE", font = ('Terminal', 12, 'bold'), command=lambda : update_analytics(trades=trades, analytics_widgets=analytics_widgets))
refresh_btn.place(relx=1, rely=0, width=30, height=30, anchor="ne")
for i in analytics_widgets.keys():
    analytics_widgets[i].pack()

#connection status
status_frame = Frame(root, bg="#1b1919")
btn_frame.update_idletasks()
status_frame.place(x = 10, y = btn_frame.winfo_height() + 15, anchor="nw", width=btn_frame.winfo_width())
status_frame_widgets = {
    "connect_stat" : Label(status_frame, text="connection : ", bg="#1b1919", fg="#ffffff", font=('Terminal', 10)),
    "server_stat" : Label(status_frame, text="server : ", bg="#1b1919", fg="#ffffff", font=('Terminal', 10)),
    "stat_1" : Label(status_frame, text="...", bg="#1b1919", fg="#ffffff", font=('Terminal', 10, 'bold')),
    "stat_2" : Label(status_frame, text="...", bg="#1b1919", fg="#ffffff", font=('Terminal', 10, 'bold'))
}
status_frame_widgets["connect_stat"].pack(anchor="nw")
status_frame_widgets["server_stat"].pack(anchor="nw")
status_frame.update_idletasks()
status_frame_widgets["stat_1"].place(x = status_frame_widgets["connect_stat"].winfo_x() + status_frame_widgets["connect_stat"].winfo_width(), y=status_frame_widgets["connect_stat"].winfo_y())
status_frame_widgets["stat_2"].place(x = status_frame_widgets["server_stat"].winfo_x() + status_frame_widgets["server_stat"].winfo_width(), y=status_frame_widgets["server_stat"].winfo_y())
#connection_status(status_frame_widgets["stat_1"], status_frame_widgets["stat_2"])
refresh_btn = Button(status_frame, text="⟲", bg = "#7854CE", font = ('Terminal', 7, 'bold'), command=lambda n = status_frame_widgets["stat_1"], s = status_frame_widgets["stat_2"] : connection_status(n, s))
refresh_btn.place(relx=1, rely=0, width=15, height=15, anchor="ne")

root.mainloop()


