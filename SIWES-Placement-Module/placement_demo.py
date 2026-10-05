import tkinter as tk
from placement.placement_module import PlacementManager

root = tk.Tk()
root.withdraw()

PlacementManager(root)

root.mainloop()
