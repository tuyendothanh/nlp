# TreeTest.py - example of using fonts in tags with ttk Treeview
# 2013-08-15 16:32:39  Todd Fiske

import Tkinter as tk
import tkFont as tkfont
import ttk
import random

class TreeTest(ttk.Frame):
    def __init__(self, name='treetest'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=tk.Y, fill=tk.BOTH)
        self.master.title('Tree Test')

        self._create_treeview(self)
        #self._build_fake_data()
        #self._populate_tree()

        self.tree.bind("<Double-1>", self.OnDoubleClick)


    def _create_treeview(self, parent):
        f = ttk.Frame(parent)
        f.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.Y)

        # create the tree and scrollbars
        self.dataCols = ('ipaddress', 'pingtime', 'status', 'pcname',
            'macaddress')
        self.tree = ttk.Treeview(columns=self.dataCols)

        ysb = ttk.Scrollbar(orient=tk.VERTICAL, command= self.tree.yview)
        xsb = ttk.Scrollbar(orient=tk.HORIZONTAL, command= self.tree.xview)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set

        # setup column headings
        self.tree.heading('#0',         text='#',           anchor=tk.E)
        self.tree.heading('ipaddress',  text='IP Address',  anchor=tk.W)
        self.tree.heading('pingtime',   text='Ping Time',   anchor=tk.E)
        self.tree.heading('status',     text='Status',      anchor=tk.W)
        self.tree.heading('pcname',     text='Device Name', anchor=tk.W)
        self.tree.heading('macaddress', text='MAC Address', anchor=tk.W)

        self.tree.column('#0',         stretch=0, width=40 , anchor=tk.E)
        self.tree.column('ipaddress',  stretch=0, width=160)
        self.tree.column('pingtime',   stretch=0, width=100, anchor=tk.E)
        self.tree.column('status',     stretch=0, width=100)
        self.tree.column('pcname',     stretch=0, width=160)
        self.tree.column('macaddress', stretch=0, width=160)

        # add tree and scrollbars to frame
        self.tree.grid(in_=f, row=0, column=0, sticky=tk.NSEW)
        ysb.grid(in_=f, row=0, column=1, sticky=tk.NS)
        xsb.grid(in_=f, row=1, column=0, sticky=tk.EW)

        # set frame resizing priorities
        f.rowconfigure(0, weight=1)
        f.columnconfigure(0, weight=1)

        # create fonts and tags
        self.normal   = tkfont.Font(family='Consolas', size=10)
        self.boldfont = tkfont.Font(family='Consolas', size=10, weight='bold')
        self.whacky   = tkfont.Font(family='Jokerman', size=10)

        self.tree.tag_configure('normal',   font=self.normal)
        self.tree.tag_configure('timedout', background='pink',
            font=self.boldfont)
        self.tree.tag_configure('whacky',   background='lightgreen',
            font=self.whacky)


    def _build_fake_data(self):
        # create a dict with a number as key, and randomized contents matching
        # the column layout of the table

        self.data = {}

        for n in range(20):
            num = n + 1
            ipaddress = '192.168.164.2%.2d' % num

            if random.randrange(2) == 0:
                pingtime = '1000ms'
                status = 'Timed Out'
            else:
                pingtime = '%d ms' % random.randrange(20, 300)
                status = 'Connected'

            pcname = 'CONFERENCELAPTOP%.2d' % num
            macaddress = 'AB-CD-EF-00-24-%.2X' % num

            self.data[num] = [ipaddress, pingtime, status, pcname, macaddress]


    def _populate_tree(self):
        for n in range(len(self.data)):
            num = n+1
            item = self.data[num]

            if item[2] == 'Timed Out': # use highlight if status is 'timedout'
                tags = ('timedout')
            else:
                tags = ('normal')

            if '5' in item[0]: # override styles if there's a 5 in the ipaddress
                tags = ['whacky']

            self.tree.insert('', tk.END, text='%3d'%num, values=item, tags=tags)

    def OnDoubleClick(self, event):
        # item = self.tree.selection()[0]
        item = self.tree.identify('item',event.x,event.y)
        print("you clicked on", self.tree.item(item,"text"))


if __name__ == '__main__':
    TreeTest().mainloop()