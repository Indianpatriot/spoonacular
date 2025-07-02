import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk  # Install with: pip install pillow
import io

# Spoonacular API Key (Replace with your key)
API_KEY = "fa456475706b443a99fc843f3077688e"

# Function to fetch recipes
def search_recipes():
    ingredient = entry.get().strip()
    if not ingredient:
        messagebox.showwarning("Input Error", "Please enter an ingredient!")
        return
    
    url = f"https://api.spoonacular.com/recipes/complexSearch?query={ingredient}&apiKey={API_KEY}&number=5"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        recipes_list.delete(0, tk.END)  # Clear old results
        recipe_images.clear()  # Clear old images
        
        if "results" in data and data["results"]:
            for recipe in data["results"]:
                recipes_list.insert(tk.END, recipe["title"])  # Add recipe name to list
                recipe_images[recipe["title"]] = recipe["image"]  # Store image URL
        else:
            recipes_list.insert(tk.END, "No recipes found!")
    else:
        messagebox.showerror("API Error", f"Error {response.status_code}: {response.text}")

# Function to display selected recipe image
def show_recipe_image(event):
    selected_index = recipes_list.curselection()
    if selected_index:
        recipe_name = recipes_list.get(selected_index)
        image_url = recipe_images.get(recipe_name)

        if image_url:
            response = requests.get(image_url)
            if response.status_code == 200:
                image_data = io.BytesIO(response.content)
                image = Image.open(image_data)
                image = image.resize((200, 150))  # Resize for display
                photo = ImageTk.PhotoImage(image)

                # Update image label
                image_label.config(image=photo)
                image_label.image = photo

# GUI Setup
root = tk.Tk()
root.title("Recipe Search Tool")
root.geometry("500x500")

# Label & Entry
label = tk.Label(root, text="Enter Ingredients:", font=("Arial", 12))
label.pack(pady=10)

entry = tk.Entry(root, width=40)
entry.pack(pady=5)

# Search Button
search_button = ttk.Button(root, text="Search Recipes", command=search_recipes)
search_button.pack(pady=10)

# Listbox to Display Recipes
recipes_list = tk.Listbox(root, width=50, height=5)
recipes_list.pack(pady=10)
recipes_list.bind("<<ListboxSelect>>", show_recipe_image)  # Bind selection event

# Label to Show Recipe Image
image_label = tk.Label(root)
image_label.pack(pady=10)

# Dictionary to store recipe images
recipe_images = {}

# Run the GUI
root.mainloop()
