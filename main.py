import tkinter as tk
from tkinter import ttk
from api_requests import fetch_recipes, fetch_recipe_details
from logging_config import logger
from visualization import plot_nutrition
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import requests
from io import BytesIO
import pandas as pd

# GUI Setup
root = tk.Tk()
root.title("Recipe Search Tool")
root.geometry("850x900")
root.configure(bg="#F8F8F8")

# Scrollable canvas setup
main_canvas = tk.Canvas(root, bg="#F8F8F8")
scroll_y = tk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
main_frame = tk.Frame(main_canvas, bg="#F8F8F8")

main_frame.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))
main_canvas.create_window((0, 0), window=main_frame, anchor="nw")
main_canvas.configure(yscrollcommand=scroll_y.set)

main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

# Global state
recipe_data = []
selected_nutrition = []
nutrition_visible = False

# Input Section
tk.Label(main_frame, text="Enter Ingredients:", font=("Arial", 14), bg="#F8F8F8").pack(pady=5)
entry = tk.Entry(main_frame, width=50, font=("Arial", 12))
entry.pack(pady=5)

diet_var = tk.StringVar(value="none")
tk.Label(main_frame, text="Select Diet:", font=("Arial", 12), bg="#F8F8F8").pack()
diet_dropdown = ttk.Combobox(main_frame, textvariable=diet_var,
                             values=["none", "vegetarian", "vegan", "gluten free", "ketogenic"], font=("Arial", 12))
diet_dropdown.pack(pady=5)

# Recipe List Section
search_button = ttk.Button(main_frame, text="Search Recipes",
                           command=lambda: threading.Thread(target=fetch_and_display).start())
search_button.pack(pady=10)

recipes_list = tk.Listbox(main_frame, width=60, height=6, font=("Arial", 12))
recipes_list.pack(pady=10)
recipes_list.bind("<<ListboxSelect>>", lambda event: threading.Thread(target=show_recipe_details).start())

image_label = tk.Label(main_frame, bg="#F8F8F8")
image_label.pack(pady=10)

# Buttons Frame
button_frame = tk.Frame(main_frame, bg="#F8F8F8")
button_frame.pack(pady=10)

viz_btn = ttk.Button(button_frame, text="Show Visualization",
                     command=lambda: threading.Thread(target=show_visualization).start())
viz_btn.pack(side=tk.LEFT, padx=10)

nutrition_btn = ttk.Button(button_frame, text="Show Nutrition", command=lambda: toggle_nutrition())
nutrition_btn.pack(side=tk.LEFT, padx=10)

# Nutrition Display Frame
nutrition_frame = tk.Frame(main_frame, bg="#F8F8F8")
nutrition_frame.pack(fill="x", padx=10, pady=5)
nutrition_frame.grid_columnconfigure(0, weight=1)

nutrition_text = tk.Text(nutrition_frame, width=40, height=15, wrap=tk.WORD, font=("Arial", 11),
                         bg="#FFFFFF", relief=tk.SOLID, bd=1)
nutrition_text.grid(row=0, column=1, sticky="ne", padx=10, pady=5)
nutrition_text.config(state=tk.DISABLED)
nutrition_frame.pack_forget()  # Initially hidden

# Details Frame
details_frame = tk.Frame(main_frame, bg="#F8F8F8")
details_frame.pack(pady=10, fill="both", expand=True)

details_text = tk.Text(details_frame, width=80, height=15, wrap=tk.WORD, font=("Arial", 12))
details_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Plot Frame
plot_frame = tk.Frame(main_frame, bg="#F8F8F8")
plot_frame.pack(pady=10, fill="both", expand=True)

# Functions
def fetch_and_display():
    query = entry.get().strip()
    diet = diet_var.get() if diet_var.get() != "none" else ""
    if not query:
        return

    try:
        recipes = fetch_recipes(query, diet)
        recipe_data.clear()
        recipe_data.extend(recipes)
        recipes_list.delete(0, tk.END)
        for recipe in recipes:
            recipes_list.insert(tk.END, recipe.get("title", "No Title"))
    except Exception as e:
        logger.error(f"Error in fetch_and_display: {e}")


def show_recipe_details():
    global selected_nutrition
    try:
        selected = recipes_list.curselection()
        if not selected:
            return

        index = selected[0]
        recipe = recipe_data[index]
        details = fetch_recipe_details(recipe["id"])

        selected_nutrition = details.get("nutrition", {}).get("nutrients", [])[:10]


        # Display text info
        ingredients = "\n".join([f"- {i.get('original', '')}" for i in details.get("extendedIngredients", [])])
        instructions = details.get("instructions", "No instructions available.")
        title = recipe.get("title", "Recipe")

        details_text.config(state=tk.NORMAL)
        details_text.delete("1.0", tk.END)
        details_text.insert(tk.END, f"🍽 {title}\n\n📌 Ingredients:\n{ingredients}\n\n📝 Instructions:\n{instructions}")
        details_text.config(state=tk.DISABLED)

        # Image
        img_url = details.get("image", "")
        if img_url:
            img_data = Image.open(BytesIO(requests.get(img_url).content)).resize((220, 220))
            img = ImageTk.PhotoImage(img_data)
            image_label.config(image=img)
            image_label.image = img

    except Exception as e:
        logger.error(f"Error in show_recipe_details: {e}")


def toggle_nutrition():
    global nutrition_visible
    if nutrition_visible:
        nutrition_frame.pack_forget()
    else:
        if selected_nutrition:
            df = pd.DataFrame(selected_nutrition)[["name", "amount", "unit"]]
            if len(df) >= 8:
                df = df.head(8)

            text = df.to_string(index=False)

            nutrition_text.config(state=tk.NORMAL)
            nutrition_text.delete("1.0", tk.END)
            nutrition_text.insert(tk.END, text)
            nutrition_text.config(state=tk.DISABLED)
        nutrition_frame.pack(fill="x", padx=10, pady=5)

    nutrition_visible = not nutrition_visible


def show_visualization():
    try:
        selected = recipes_list.curselection()
        if not selected:
            return

        index = selected[0]
        recipe = recipe_data[index]
        details = fetch_recipe_details(recipe["id"])
        nutrition = details.get("nutrition", {}).get("nutrients", [])

        if not nutrition:
            return

        fig = plot_nutrition(nutrition)  # You can modify plot_nutrition to take top 4 nutrients if needed

        # Clear previous plot
        for widget in plot_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    except Exception as e:
        logger.error(f"Error in show_visualization: {e}")



root.mainloop()
