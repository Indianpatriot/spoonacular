import matplotlib.pyplot as plt
import pandas as pd

def plot_nutrition(nutrients):
    if not nutrients:
        return plt.figure(figsize=(6, 4))

    # Unit normalization factors
    conversion_factors = {
        "kcal": 1,
        "g": 1,
        "mg": 0.001
    }

    # Normalize nutrients
    normalized = []
    for n in nutrients:
        name = n.get("name", "Unknown")
        amount = n.get("amount", 0)
        unit = n.get("unit", "").lower()
        factor = conversion_factors.get(unit, 1)
        norm_amount = amount * factor
        normalized.append({"name": name, "amount": norm_amount})

    # Build dataframe
    df = pd.DataFrame(normalized)
    df = df.groupby("name", as_index=False).sum()
    df_sorted = df.sort_values(by="amount", ascending=False)

    # Bar chart data (top 8)
    bar_df = df_sorted.head(8)

    # Pie chart data (top 4 + others)
    pie_df = df_sorted.copy()  # fresh copy
    pie_top4 = pie_df.head(4)
    pie_labels = pie_top4["name"].tolist()
    pie_values = pie_top4["amount"].tolist()
    others_total = pie_df.iloc[4:]["amount"].sum()

    if others_total > 0:
        pie_labels.append("Others")
        pie_values.append(others_total)

    total = sum(pie_values)
    pie_percentages = [(v / total) * 100 for v in pie_values]

    # Plot
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))

    # Bar chart
    axs[0].bar(bar_df["name"], bar_df["amount"], color="skyblue")
    axs[0].set_title("Top Nutrients (Bar Chart)")
    axs[0].tick_params(axis='x', labelrotation=45)
    axs[0].set_ylabel("Amount (kcal/g)")

    # Pie chart
    axs[1].pie(pie_percentages, labels=pie_labels, autopct='%1.1f%%', startangle=140)
    axs[1].set_title("Top 4 Nutrients (Pie Chart)")

    plt.tight_layout()
    return fig
