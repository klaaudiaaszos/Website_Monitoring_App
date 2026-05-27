import requests
import time
from datetime import datetime
from threading import Thread
import tkinter as tk
from tkinter import messagebox

class WebsiteCheckerApp (tk.Tk):
    def __init__ (self):
        super().__init__()
        self.title ("Website Checker")
        self.geometry ("800x600")
        self.websites = [
            { "url" : "https://onet.pl", "Last Checked" : None },
            { "url" : "https://ithardware.pl", "Last Checked" : None },
            { "url" : "https://fsdfsfs.pl", "Last Checked" : None }
        ]
        self.createWidgets ()
        self.updateWebsitesList ()
        Thread (target= self.startChecking, daemon = True).start ()
    
    def createWidgets (self):
        self.urlEntry = tk.Entry (self)
        self.urlEntry.pack (pady = 20)

        self.addButton = tk.Button (self, text= "Add Website", command = self.addWebsite)
        self.addButton.pack (pady=10)

        self.websitesList = tk.Listbox (self, width=100, height=15)
        self.websitesList.pack (fill=tk.BOTH, expand = True, padx = 20, pady = 20)
    
    def addWebsite (self):
        url = self.urlEntry.get ()
        if url:
            self.websites.append ({ "url" : url, "Last Checked" : None })
            self.updateWebsitesList ()
            self.urlEntry.delete (0, tk.END)
        else:
            messagebox.showwarning ("Error", "Url cannot be empty.")

    def updateWebsitesList (self):
        self.websitesList.delete (0, tk.END)
        for website in self.websites:
            lastChecked = website ["Last Checked"] if website ["Last Checked"] else "Not checked yet"
            displayText = f"{website ["url"]} - Last Checked: {lastChecked}"
            self.websitesList.insert (tk.END, displayText)

    def checkWebsite (self, website):
        try:
            response = requests.get(website ["url"], timeout = 5)
            status = "OK" if response.status_code == 200 else "Problem"
        except requests.RequestException:
            status = "Problem"
        return status
    
    def startChecking (self):
        while True:
            for i, website in enumerate (self.websites):
                status = self.checkWebsite (website)
                lastChecked = datetime.now ().strftime ("%Y-%m-%d %H:%M:%S")
                self.updateWebsiteStatus (i, website ["url"], status, lastChecked )
            time.sleep (5)
    
    def updateWebsiteStatus (self, index, url, status, lastChecked):
        def _update ():
            displayText = f"{url} - {status} - Last Checked: {lastChecked}"
            self.websitesList.delete (index)
            self.websitesList.insert (index, displayText)
            self.websites [index]["Last Checked"] = lastChecked
        self.after (0, _update)

if __name__ == "__main__":
    app = WebsiteCheckerApp ()
    app.mainloop ()