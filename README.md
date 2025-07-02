##  🥗 Recipe Finder Desktop App

A Python-based desktop application that helps users search for recipes by ingredients and visualize their nutritional breakdown using real-time data from the Spoonacular API.

---

## 📌 Features

* 🔍 **Ingredient-Based Recipe Search**
  Search recipes by entering available ingredients.

* 🥦 **Dietary Filters**
  Filter results by diet type (Vegetarian, Vegan, Gluten-Free, Ketogenic, etc.).

* 📋 **Recipe Details Viewer**
  View cooking instructions, ingredients, and recipe image.

* 📊 **Nutritional Visualization**
  Visualize nutrients using bar and pie charts via Matplotlib.

* 📑 **Pandas Nutrition Table**
  Display top 8 nutrients per recipe in a readable tabular format.

* ⚙️ **Multithreading Support**
  Keeps GUI responsive during API calls and plotting.

* 🪵 **Logging System**
  Tracks API usage, user actions, and errors for debugging.

---

## 🛠️ Tech Stack

| Technology      | Purpose                        |
| --------------- | ------------------------------ |
| Python          | Core programming language      |
| Tkinter         | GUI framework                  |
| Spoonacular API | Recipe & nutrition data source |
| Pandas          | Data handling and tabulation   |
| Matplotlib      | Nutrient data visualization    |
| Logging         | Event tracking & error logging |
| Threading       | Improves performance and UX    |

---

## 🖼️ UI Preview

*Include screenshots of:*

* Main window with search input
* Recipe list and details
* Nutrient chart and pie graph
* Pandas table output

---

## 🚀 Getting Started

### Prerequisites

Make sure Python 3.5 is installed. Then install the required libraries:


pip install requests pandas matplotlib pillow

### Setup Instructions

1. Clone or download the project.
2. Replace the placeholder `API_KEY` in `api_requests.py` with your Spoonacular API key.
3. Run the application using:

```bash
python main.py
```

---

## 📂 Project Structure

```
RecipeFinder/
│
├── main.py                  # Main GUI and logic
├── api_requests.py          # API functions and data fetching
├── visualization.py         # Nutrient chart generation
├── logging_config.py        # Log setup and config
├── README.md                # Project documentation
└── assets/                  # Optional: for images or icons
```

---

## 🔐 API Key Setup

Get a free API key from [spoonacular.com](https://spoonacular.com/food-api) and replace `"YOUR_API_KEY"` in `api_requests.py`.

---

## 🎓 Learning Outcomes

* Practical API integration
* GUI application design with Tkinter
* Data visualization and structuring
* Exception handling and multithreading
* Real-time application development with clean UI/UX

---

## 👨‍💻 Author

**Internship By:** Rubixe AI, Bengaluru
**Developer:** Nitin
**Tech Stack:** Python | Tkinter | Pandas | Matplotlib


