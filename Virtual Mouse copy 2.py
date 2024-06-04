import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from tkinter.simpledialog import askstring
import tkinter.simpledialog as simpledialog
from PIL import ImageTk,Image,ImageOps
# 40,25,70,22,35,60,80,90,10,30
#10,18,7,15,16,30,25,40,60,2,1,70
# 40,50,70,30,20,45,25,10,5,32,1,35
root = tk.Tk()
root.title("Data Structures Program")

root.wm_iconbitmap(r"D:\download\Project\Images\1.ico")
# root.geometry("800x600")

tab_control = ttk.Notebook(root)
tab_control.pack(fill=tk.BOTH, expand=True)

parent = None

def insert_values():
    values1 = value_entry1.get().split(',')
    for value1 in values1:
        insert_node(int(value1.strip()))
    update_tree_visual()

def insert_node(value1):
    global parent
    if parent is None:
        parent = {"value": value1, "left": None, "right": None}
    else:
        insert_recursive(parent, value1)

def insert_recursive(node, value):
    if value < node["value"]:
        if node["left"] is None:
            node["left"] = {"value": value, "left": None, "right": None}
        else:
            insert_recursive(node["left"], value)
    else:
        if node["right"] is None:
            node["right"] = {"value": value, "left": None, "right": None}
        else:
            insert_recursive(node["right"], value)

def search_node():
    value = int(value_entry1.get())
    result = search_recursive(parent, value)
    if result:
        messagebox.showinfo("Search Result", f"The value {value} was found in the binary search tree.")
    else:
        messagebox.showinfo("Search Result", f"The value {value} was not found in the binary search tree.")

def search_recursive(node, value):
    if node is None or node["value"] == value:
        return node is not None
    if value < node["value"]:
        return search_recursive(node["left"], value)
    else:
        return search_recursive(node["right"], value)

def update_tree_visual():
    canvas1.delete("all")
    if parent is not None:
        draw_node(parent, 300, 50, 100)

def draw_node(node, x, y, spacing):
    radius = 20
    text_padding = 10

    value = node["value"]
    left_child = node["left"]
    right_child = node["right"]

    canvas1.create_oval(x - radius, y - radius, x + radius, y + radius, outline="black")
    canvas1.create_text(x, y, text=value)

    if left_child:
        canvas1.create_line(x - radius, y , x - spacing, y + 2 * radius + spacing-20)
        draw_node(left_child, x - spacing, y + 2 * radius + spacing, spacing // 2)

    if right_child:
        canvas1.create_line(x + radius, y, x + spacing, y + 2 * radius + spacing-20)
        draw_node(right_child, x + spacing, y + 2 * radius + spacing, spacing // 2)

binary_tree_tab = ttk.Frame(tab_control)
tab_control.add(binary_tree_tab, text="Binary Search Tree")

bst_bg_image = ImageTk.PhotoImage(Image.open(r"D:\download\Project\Images\Background.png"))
bst_background_label = ttk.Label(binary_tree_tab, image=bst_bg_image)
bst_background_label.place(x=0, y=0, relwidth=1, relheight=1)

canvas_width1 = 600
canvas_height1 = 400

canvas_frame1 = ttk.Frame(binary_tree_tab)
canvas_frame1.pack()

canvas_scrollbar_x1 = ttk.Scrollbar(canvas_frame1, orient=tk.HORIZONTAL)
canvas_scrollbar_x1.pack(side=tk.BOTTOM, fill=tk.X)

canvas_scrollbar_y1 = ttk.Scrollbar(canvas_frame1, orient=tk.VERTICAL)
canvas_scrollbar_y1.pack(side=tk.RIGHT, fill=tk.Y)

canvas1 = tk.Canvas(canvas_frame1, width=canvas_width1, height=canvas_height1, xscrollcommand=canvas_scrollbar_x1.set,
                   yscrollcommand=canvas_scrollbar_y1.set)
canvas1.pack()

canvas_scrollbar_x1.config(command=canvas1.xview)
canvas_scrollbar_y1.config(command=canvas1.yview)

# Create a frame for input
input_frame1 = ttk.Frame(binary_tree_tab)
input_frame1.pack(pady=10)

# Create a label and an entry for node value input
value_label1 = ttk.Label(input_frame1, text="Node Values (comma-separated):")
value_label1.pack(side=tk.LEFT)

value_entry1 = ttk.Entry(input_frame1, width=30)
value_entry1.pack(side=tk.LEFT)

# Create buttons for insert and search operations
insert_button = ttk.Button(binary_tree_tab, text="Insert Nodes", command=insert_values)
insert_button.pack(pady=5)

search_button = ttk.Button(binary_tree_tab, text="Search Node", command=search_node)
search_button.pack(pady=5)








#red black tree
parent1=None
def insert_node1():
    values1 = value_entry3.get().split(",")
    for value in values1:
        value = value.strip()
        if value:
            insert1(int(value))
    update_tree_visual1()

def insert1(value):
    global parent1
    if parent1 is None:
        parent1 = {"value": value, "color": "black", "left": None, "right": None, "parent": None}
    else:
        node = {"value": value, "color": "red", "left": None, "right": None, "parent": None}
        current = parent1
        parent = None
        while current is not None:
            parent = current
            if value < current["value"]:
                current = current["left"]
            else:
                current = current["right"]

        node["parent"] = parent
        if value < parent["value"]:
            parent["left"] = node
        else:
            parent["right"] = node

        fix_insert(node)

def fix_insert(node):
    while node["parent"] is not None and node["parent"]["color"] == "red":
        if node["parent"]["parent"] is not None:
            if node["parent"] == node["parent"]["parent"]["left"]:
                uncle = node["parent"]["parent"]["right"]
                if uncle is not None and uncle["color"] == "red":
                    node["parent"]["color"] = "black"
                    uncle["color"] = "black"
                    node["parent"]["parent"]["color"] = "red"
                    node = node["parent"]["parent"]
                else:
                    if node == node["parent"]["right"]:
                        node = node["parent"]
                        rotate_left3(node)
                    node["parent"]["color"] = "black"
                    node["parent"]["parent"]["color"] = "red"
                    rotate_right(node["parent"]["parent"])
            else:
                uncle = node["parent"]["parent"]["left"]
                if uncle is not None and uncle["color"] == "red":
                    node["parent"]["color"] = "black"
                    uncle["color"] = "black"
                    node["parent"]["parent"]["color"] = "red"
                    node = node["parent"]["parent"]
                else:
                    if node == node["parent"]["left"]:
                        node = node["parent"]
                        rotate_right(node)
                    node["parent"]["color"] = "black"
                    node["parent"]["parent"]["color"] = "red"
                    rotate_left3(node["parent"]["parent"])

    parent1["color"] = "black"

def rotate_left3(node):
    if node["right"] is None:
        return

    right_child = node["right"]
    node["right"] = right_child["left"]
    if right_child["left"] is not None:
        right_child["left"]["parent"] = node

    right_child["parent"] = node["parent"]
    if node["parent"] is None:
        global parent1
        parent1 = right_child
    elif node == node["parent"]["left"]:
        node["parent"]["left"] = right_child
    else:
        node["parent"]["right"] = right_child

    right_child["left"] = node
    node["parent"] = right_child

def rotate_right(node):
    if node["left"] is None:
        return

    left_child = node["left"]
    node["left"] = left_child["right"]
    if left_child["right"] is not None:
        left_child["right"]["parent"] = node

    left_child["parent"] = node["parent"]
    if node["parent"] is None:
        global parent1
        parent1 = left_child
    elif node == node["parent"]["left"]:
        node["parent"]["left"] = left_child
    else:
        node["parent"]["right"] = left_child

    left_child["right"] = node
    node["parent"] = left_child

def update_tree_visual1():
    canvas3.delete("all")
    draw_tree(parent1, 300, 50, 100)

def draw_tree(node, x, y, spacing):
    if node is None:
        return

    radius = 20
    text_padding = 10

    value = node["value"]
    color = node["color"]
    left_child = node["left"]
    right_child = node["right"]

    fill_color = "black" if color == "black" else "red"
    canvas3.create_oval(x - radius, y - radius, x + radius, y + radius, outline="black", fill=fill_color)
    canvas3.create_text(x, y, text=str(value), fill="white")

    if left_child:
        line_color = "black" if left_child["color"] == "black" else "red"
        canvas3.create_line(x - radius, y , x - spacing, y + 2 * radius + spacing-20, fill=line_color)
        draw_tree(left_child, x - spacing, y + 2 * radius + spacing, spacing // 2)

    if right_child:
        line_color = "black" if right_child["color"] == "black" else "red"
        canvas3.create_line(x + radius, y, x + spacing, y + 2 * radius + spacing-20, fill=line_color)
        draw_tree(right_child, x + spacing, y + 2 * radius + spacing, spacing // 2)



rbt_tree_tab = ttk.Frame(tab_control)
tab_control.add(rbt_tree_tab, text="Red Black Tree")

rbt_bg_image = ImageTk.PhotoImage(Image.open(r"D:\download\Project\Images\Background.png"))
rbt_background_label = ttk.Label(rbt_tree_tab, image=rbt_bg_image)
rbt_background_label.place(x=0, y=0, relwidth=1, relheight=1)

canvas_width3 = 800
canvas_height3 = 500

canvas_frame3 = ttk.Frame(rbt_tree_tab)
canvas_frame3.pack()

canvas_scrollbar_x3 = ttk.Scrollbar(canvas_frame3, orient=tk.HORIZONTAL)
canvas_scrollbar_x3.pack(side=tk.BOTTOM, fill=tk.X)

canvas_scrollbar_y3 = ttk.Scrollbar(canvas_frame3, orient=tk.VERTICAL)
canvas_scrollbar_y3.pack(side=tk.RIGHT, fill=tk.Y)

canvas3 = tk.Canvas(canvas_frame3, width=canvas_width3, height=canvas_height3, xscrollcommand=canvas_scrollbar_x3.set,
                   yscrollcommand=canvas_scrollbar_y3.set)
canvas3.pack()

canvas_scrollbar_x3.config(command=canvas3.xview)
canvas_scrollbar_y3.config(command=canvas3.yview)

input_frame3 = ttk.Frame(rbt_tree_tab)
input_frame3.pack(pady=10)

value_label3 = ttk.Label(input_frame3, text="Node Values (comma-separated):")
value_label3.pack(side=tk.LEFT)

value_entry3 = ttk.Entry(input_frame3, width=50)
value_entry3.pack(side=tk.LEFT)

insert_button3 = ttk.Button(rbt_tree_tab, text="Insert Nodes", command=insert_node1)
insert_button3.pack(pady=5)



# AVL TREE
parent2 = None

def insert_node4():
    values4 = value_entry4.get().split(",")
    for value4 in values4:
        value4 = value4.strip()
        if value4:
            global parent2
            parent2 = insert_recursive4(parent2, int(value4))

    update_tree_visual4()


def insert_recursive4(node, value):
    if node is None:
        return {"value": value, "left": None, "right": None, "height": 1}

    if value < node["value"]:
        node["left"] = insert_recursive4(node["left"], value)
    else:
        node["right"] = insert_recursive4(node["right"], value)

    node["height"] = 1 + max(get_height4(node["left"]), get_height4(node["right"]))

    balance_factor = get_balance_factor4(node)

    if balance_factor > 1:
        if value < node["left"]["value"]:
            return rotate_right4(node)
        else:
            node["left"] = rotate_left4(node["left"])
            return rotate_right4(node)
    elif balance_factor < -1:
        if value > node["right"]["value"]:
            return rotate_left4(node)
        else:
            node["right"] = rotate_right4(node["right"])
            return rotate_left4(node)

    return node


def get_height4(node):
    if node is None:
        return 0
    return node["height"]


def get_balance_factor4(node):
    if node is None:
        return 0
    return get_height4(node["left"]) - get_height4(node["right"])


def rotate_left4(z):
    y = z["right"]
    T2 = y["left"]

    y["left"] = z
    z["right"] = T2

    z["height"] = 1 + max(get_height4(z["left"]), get_height4(z["right"]))
    y["height"] = 1 + max(get_height4(y["left"]), get_height4(y["right"]))

    return y


def rotate_right4(y):
    x = y["left"]
    T2 = x["right"]

    x["right"] = y
    y["left"] = T2

    y["height"] = 1 + max(get_height4(y["left"]), get_height4(y["right"]))
    x["height"] = 1 + max(get_height4(x["left"]), get_height4(x["right"]))

    return x


def update_tree_visual4():
    canvas4.delete("all")
    draw_node4(parent2, 300, 50, 100)


def draw_node4(node, x, y, spacing):
    if node is None:
        return

    radius = 20
    text_padding = 10

    value = node["value"]
    left_child = node["left"]
    right_child = node["right"]

    canvas4.create_oval(x - radius, y - radius, x + radius, y + radius, outline="black")
    canvas4.create_text(x, y, text=value)

    if left_child:
        canvas4.create_line(x - radius, y , x - spacing, y + 2 * radius + spacing-20)
        draw_node4(left_child, x - spacing, y + 2 * radius + spacing, spacing // 2)

    if right_child:
        canvas4.create_line(x + radius, y , x + spacing, y + 2 * radius + spacing-20)
        draw_node4(right_child, x + spacing, y + 2 * radius + spacing, spacing // 2)

avl_tree_tab = ttk.Frame(tab_control)
tab_control.add(avl_tree_tab, text="AVL TREE")

avl_bg_image = ImageTk.PhotoImage(Image.open(r"D:\download\Project\Images\Background.png"))
avl_background_label = ttk.Label(avl_tree_tab, image=avl_bg_image)
avl_background_label.place(x=0, y=0, relwidth=1, relheight=1)

canvas_width4 = 600
canvas_height4 = 400

canvas_frame4 = ttk.Frame(avl_tree_tab)
canvas_frame4.pack()

canvas_scrollbar_x4 = ttk.Scrollbar(canvas_frame4, orient=tk.HORIZONTAL)
canvas_scrollbar_x4.pack(side=tk.BOTTOM, fill=tk.X)

canvas_scrollbar_y4 = ttk.Scrollbar(canvas_frame4, orient=tk.VERTICAL)
canvas_scrollbar_y4.pack(side=tk.RIGHT, fill=tk.Y)

canvas4 = tk.Canvas(canvas_frame4, width=canvas_width4, height=canvas_height4, xscrollcommand=canvas_scrollbar_x4.set,
                   yscrollcommand=canvas_scrollbar_y4.set)
canvas4.pack()

canvas_scrollbar_x4.config(command=canvas4.xview)
canvas_scrollbar_y4.config(command=canvas4.yview)

# Create a frame for input
input_frame4 = ttk.Frame(avl_tree_tab)
input_frame4.pack(pady=10)

# Create a label and an entry for node value input
value_label4 = ttk.Label(input_frame4, text="Node Values (comma-separated):")
value_label4.pack(side=tk.LEFT)

value_entry4 = ttk.Entry(input_frame4, width=30)
value_entry4.pack(side=tk.LEFT)

# Create a button for inserting nodes
insert_button4 = ttk.Button(avl_tree_tab, text="Insert Nodes", command=insert_node4)
insert_button4.pack(pady=5)

tab_control.pack(expand=True, fill="both")

root.mainloop()
