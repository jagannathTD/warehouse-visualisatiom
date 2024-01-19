

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import datetime



current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')  # Format as: 'YYYY-MM-DD HH:MM:SS'

# Setting random seed for reproducibility
np.random.seed(0)

# Number of rows and columns for each heatmap
rows = 10
cols = 3

# Generating matrix with desired color proportions
def generate_matrix():
    total_cells = rows * cols
    
    empty_shelves = [-1] * int(0.15 * total_cells)
    color_0 = [0] * int(0.45 * total_cells)
    color_1 = [1] * int(0.2 * total_cells)
    color_2 = [2] * int(0.1 * total_cells)
    color_3 = [3] * int(0.1 * total_cells)
    
    while len(empty_shelves + color_0 + color_1 + color_2 + color_3) < total_cells:
        empty_shelves.append(-1)  # Adjusting for any rounding errors by adding to empty shelves
    
    products = empty_shelves + color_0 + color_1 + color_2 + color_3
    np.random.shuffle(products)
    
    return np.array(products).reshape(rows, cols)

# Generate value matrix between 40 and 70
def generate_value_matrix():
    values = np.random.randint(40, 71, size=(rows, cols))
    return values

heatmaps = [generate_matrix() for _ in range(8)]
value_maps = [generate_value_matrix() for _ in range(8)]

# List of SKU codes
sku_codes = [
    "GH002KL0050JB", "GH002TN0050JA", "GH0041660JE", "GH0040830JE", "GH0040800TEA", 
    "GH0040400TEA", "GH0040200JE", "GH0031660JE", "GH002TN2000TA", "GH002TN1000JA", 
    "GH002TN1000JA", "GH002TN0500JA", "GH002TN0200JA", "GH002TN0100SA", "GH002TN0100JA", 
    "GH002TN0050SA", "GH002TN0050JA", "GH002TN0010A", "GH001KA0500JA", "GH001KA0200JA"
]

# Colors for the products with an additional color (white) for empty shelves
# colors = ["white", "#ADD8E6", "#66b2b2", "#99e6e6", "#ffcc99", "#FFB6C1"]  # "#FFB6C1" is light red

# colors = ["#FFEB3B", "#FFC107", "#FF9800", "#FF5722", "#CDDC39", "#8BC34A"]
# colors = ["white", "#f7dc6f", "#f5b041", "#5b2c6f", "#f39c12", "#e74c3c"]
colors = ["white", "#fbf67f", "#8a659f", "#504f6f", "#fdb75e", "#e77c97"]



# # Use a predefined colorscale ('Viridis') instead of the list of colors
# colorscale = 'Viridis'

# # Create the subplots
fig = go.Figure()


# Add each heatmap to the figure
for i, (heatmap, value_map) in enumerate(zip(heatmaps, value_maps)):
    hovertext = []
    for j in range(rows):
        row_hovertext = []
        for k in range(cols):
            if heatmap[j][k] == -1:  # -1 represents empty shelves
                row_hovertext.append("Available")
            elif heatmap[j][k] == 0:  # For color #ADD8E6
                batch_year = 2023
                batch_month = np.random.randint(1, 9)  # Random month between 3 and 9
                
                # Calculate expiry month/year which is 6 months from the batch date
                expiry_month = batch_month + 6
                expiry_year = batch_year
                if expiry_month > 12:
                    expiry_month -= 12
                    expiry_year += 1
                
                # Check if the product has expired
                if (expiry_year, expiry_month) < (current_datetime.year, current_datetime.month):
                    heatmap[j][k] = 4  # Setting a distinct value for expired products to color them light red
                    
                random_sku = np.random.choice(sku_codes)
                
                row_hovertext.append("Product: Ghee<br>Stock: {}<br>SKU: {}<br>Batch: {}/{}<br>Expiry: {}/{}".format(
                    value_map[j][k], 
                    random_sku,
                    batch_month, batch_year, 
                    expiry_month, expiry_year
                ))
            elif heatmap[j][k] == 1:  # Sweets
                row_hovertext.append("Product: Sweets<br>Expiry: Month {:02d}/{:04d}".format(np.random.randint(1, 13), datetime.datetime.now().year))
            elif heatmap[j][k] == 2 or heatmap[j][k] == 3:  # Snacks
                row_hovertext.append("Product: Snacks<br>Batch: {:02d}<br>Month: {:02d}".format(np.random.randint(1, 11), np.random.randint(1, 10)))
        hovertext.append(row_hovertext)
    
    fig.add_trace(go.Heatmap(z=heatmap, 
                            x=[x + i*(cols+1) for x in range(cols)],  # +1 for the gap
                            y=list(range(rows)), 
                            colorscale=colors,
                            text=value_map, 
                            hoverinfo='text+z',
                            hovertext=hovertext, 
                            showscale=False))
# Add each heatmap to the figure
for i, (heatmap, value_map) in enumerate(zip(heatmaps, value_maps)):
    hovertext = []

legend_labels = [
    "Empty Shelf", "Product: Ghee", "Product: Sweets", "Product: Snacks", "Product: Others", "Expired"
]

# Add dummy scatter plots for the legend
for color, label in zip(colors, legend_labels):
    fig.add_trace(
        go.Scatter(
            x=[None],  # These None values ensure the scatter plot doesn't actually display any points
            y=[None],
            mode='markers',
            marker=dict(size=10, color=color),
            showlegend=True,
            name=label,
        )
    )


# Adding R1, R2, ... labels and adjusting heatmap positions
num_regions = len(heatmaps)  # Total number of regions (which are sets of 3 columns)
custom_positions = {2: 4, 3: 7, 4: 12, 5: 15, 6: 21, 7: 24}  # Specify custom positions for R2 to R7

for i in range(num_regions):
    x_position = (i * (cols + 1)) + (cols / 2) + 0.5  # Default x position
    
    if i + 1 in custom_positions:  # Check if the current region needs a custom position
        x_position = custom_positions[i + 1]  # Update the x position
        # Update heatmap x values for the current region
        fig.data[i].x = [x_position + x for x in range(cols)]
        
    fig.add_annotation(
        go.layout.Annotation(
            text=f"R{i+1}",
            xref="x",
            yref="paper",
            x=x_position,
            y=1.07,  # Just above the top
            showarrow=False,
            font=dict(size=16)
        )
    )
# Update the title of the figure with the current date and time
# fig.update_layout(title='Warehouse Stock Visualization - ' + formatted_datetime)
# fig.update_layout(title='Warehouse Stock Visualization - ' + formatted_datetime, height=800, width=1000)
    
# Assuming fig is your existing figure
# formatted_datetime = "YourFormattedDateTime"  # Replace with your actual formatted datetime

fig.update_layout(
    title='Warehouse Stock Visualization - ' + formatted_datetime,
    height=800,
    width=1000,
    plot_bgcolor='rgba(500, 500, 500, 0.7)', 
    title_x=0.25,  # Center the title
)


# Streamlit app
st.title('Warehouse Stock Visualization')


# Plotly figure
st.plotly_chart(fig)

