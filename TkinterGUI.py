import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
#from sympy import *
from PIL import ImageTk, Image
# Create the tkinter window
window = tk.Tk()
window.title("Virtual Mouse")
window.wm_iconbitmap(r"C:\Users\arshg_000\OneDrive\Desktop\OLD LAPPI\PYTHON\DS\Project (1)\Images (1)\1 (1).ico")

# Create a tab control
tab_control = ttk.Notebook(window)

# Create the Laplace Transform tab
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Virtual Mouse')
size = size_var.get()
# Set background image for Stack tab
stack_bg_image = ImageTk.PhotoImage(Image.open(r"C:\Users\arshg_000\OneDrive\Desktop\OLD LAPPI\PYTHON\DS\Project (1)\Images (1)\Background (1).jpg"))
stack_background_label = ttk.Label(tab1, image=stack_bg_image)
stack_background_label.place(x=0, y=0, relwidth=1, relheight=1)
b1 = Image.open(r"C:\Users\arshg_000\OneDrive\Desktop\OLD LAPPI\PYTHON\DS\Project (1)\Images (1)\2 (1).jpg")
br1=b1.resize((60,30))
bf1=    ImageTk.PhotoImage(br1)
# b2 = tk.PhotoImage(file=r"D:\Python\Python Files\Project\Images\2.png")
b3= tk.PhotoImage(file=r"C:\Users\arshg_000\OneDrive\Desktop\OLD LAPPI\PYTHON\DS\Project (1)\Images (1)\3 (1).jpg")

canvas_width = 400
canvas_height = 300
canvas_frame = ttk.Frame(tab1)
canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

canvas_scrollbar = ttk.Scrollbar(canvas_frame)
canvas_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas = tk.Canvas(canvas_frame, width=canvas_width, height=canvas_height, yscrollcommand=canvas_scrollbar.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

canvas_scrollbar.config(command=canvas.yview)
# Set solid color for canvas background
canvas.configure(bg="white")
size_var = tk.IntVar()  
element_var = tk.IntVar() 

labelNum1 = tk.Label(tab1, text="Size Of Stack", bg="white").place(x=450, y=40)
labelNum2 = tk.Label(tab1, text="Element To\n   Push", bg="white").place(x=450, y=80)
Num1 = ttk.Entry(tab1, textvariable=size_var).place(x=530, y=40)
Num2 = tk.Entry(tab1, textvariable=element_var).place(x=520, y=80)

push_button = tk.Button(tab1, text="Push", command=push)
push_button.config(image=bf1)
push_button.pack(side=tk.LEFT)


pop_button = tk.Button(tab1, text="Pop", command=pop )
pop_button.pack(side=tk.LEFT)

clear_button = tk.Button(tab1, text="Peek", command=peek)
clear_button.pack(side=tk.LEFT)

clear_button = tk.Button(tab1, text="Display", command=display)
clear_button.pack(side=tk.LEFT)

clear_button = tk.Button(tab1, text="Clear", command=clear)
clear_button.pack(side=tk.LEFT)

stack = []
top = -1

element_image = Image.open(r"C:\Users\arshg_000\OneDrive\Desktop\OLD LAPPI\PYTHON\DS\Project (1)\Images (1)\4 (1).jpg")
element_width = 60
element_height = 30
element_image = element_image.resize((element_width, element_height), Image.LANCZOS)
element_image = ImageTk.PhotoImage(element_image)

update_stack_visual()


# stack_background_label2 = ttk.Label(canvas, image=stack_bg_image2)
# stack_background_label2.place(x=0, y=0, relwidth=1, relheight=1)

# Create the Derivative tab
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='Laplace Transpose Multiplied with t')
# Set background image for Stack tab
stack_bg_image1 = ImageTk.PhotoImage(Image.open(r"C:\Users\arshg_000\OneDrive\Desktop\OLD LAPPI\PYTHON\DS\Project (1)\Images (1)\Background (1).ico"))
stack_background_label1 = ttk.Label(tab2, image=stack_bg_image1)
stack_background_label1.place(x=0, y=0, relwidth=1, relheight=1)
queue = []
queue_canvas_width = 400
queue_canvas_height = 200
queue_item_width = 50
queue_item_height = 50
queue_item_spacing = 10
queue_canvas_padding = 20

canvas_frame = ttk.Frame(tab2)
canvas_frame.pack(pady=10)

queue_canvas = tk.Canvas(canvas_frame, width=queue_canvas_width, height=queue_canvas_height)
queue_canvas.pack()

input_frame = ttk.Frame(tab2)
input_frame.pack(pady=10)

value_label = ttk.Label(input_frame, text="Value:")
value_label.pack(side=tk.LEFT)

value_entry = ttk.Entry(input_frame, width=10)
value_entry.pack(side=tk.LEFT)
enqueue_button = ttk.Button(tab2, text="Enqueue", command=enqueue)
enqueue_button.pack(pady=10)

dequeue_button = ttk.Button(tab2, text="Dequeue", command=dequeue)
dequeue_button.pack(pady=10)

display_button = ttk.Button(tab2, text="Display", command=display_queue)
display_button.pack(pady=10)

output_frame = ttk.Frame(tab2)
output_frame.pack()

queue_label = ttk.Label(output_frame, text="Queue:")
queue_label.pack(side=tk.LEFT)

queue_display = ttk.Label(output_frame, text="")
queue_display.pack(side=tk.LEFT)



# Add the Derivative tab to the tab control
tab_control.pack(expand=1, fill="both")

# Run the tkinter event loop
window.mainloop()
