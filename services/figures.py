import plotly.express as px


def create_tree_map(data, selected_company, metric):
    # Filter out entries where the selected metric is <= 0
    data = [entry for entry in data if entry.get(metric, 0) > 0]

    # Create the tree map
    fig = px.treemap(
        data,
        path=["segment", "name"],  # Hierarchical levels: segment > name
        values=metric,  # Dynamically use the selected metric for block sizes
        color="headcount_growth",  # Color determined by headcount growth
        color_continuous_scale=[
            (0.0, "rgb(226, 72, 66)"),  # Red for low (negative max)
            (0.2, "rgb(177, 73, 73)"),  # Less intense red at ~-2%
            (0.5, "rgb(66, 69, 83)"),  # Gray for 0%
            (0.8, "rgb(82, 156, 87)"),  # Less intense green at ~2%
            (1.0, "rgb(102, 201, 104)"),  # Green for high (positive max)
        ],
        range_color=[-1, 1],  # Adjust range to handle smaller percentage values
        color_continuous_midpoint=0,  # Center the scale at 0
        title=f"Competitive landscape of {selected_company}",
    )

    # Enhance layout and styling
    fig.update_layout(
        font=dict(
            family="Lato, sans-serif",  # Modern font
            size=15,  # Larger font size
            color="white",
        ),
        title=dict(
            font=dict(size=28),  # Larger title font
            x=0.5,  # Center the title
            xanchor="center",
        ),
        paper_bgcolor="rgb(39, 41, 48)",  # Transparent background
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
        margin=dict(t=50, l=25, r=25, b=25),  # Reduce margins for better space usage
        autosize=True,  # Allow automatic resizing
        width=1200,
        coloraxis_colorbar=dict(
            title="Headcount Growth (%)",  # Add scale name
            tickformat=".0%",  # Format ticks as percentages
        ),
    )

    # Update traces for centered text and percentages
    fig.update_traces(
        textinfo="label+text",  # Display company name and custom text
        texttemplate="%{label}<br>Size: %{value}",  # Format the text
        textfont=dict(size=16),  # General text font size inside rectangles
        textposition="middle center",  # Center the text in each rectangle
        marker=dict(line=dict(color="black", width=1)),  # Subtle borders for contrast
    )

    # Customize top-level category styling
    fig.update_traces(
        selector=dict(path_depth=0),  # Style only the top-level categories
        textfont=dict(
            size=18,  # Larger font size for categories
            weight="bold",  # Bold font for categories
        ),
    )

    # Optional: Customize sub-level styling (if needed)
    fig.update_traces(
        selector=dict(path_depth=1),  # Style subcategories
        textfont=dict(
            size=14,  # Slightly smaller font for subcategories
            color="lightgray",
        ),
    )

    return fig
