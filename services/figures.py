import plotly.express as px


def create_tree_map(data, selected_company):
    fig = px.treemap(
        data,
        path=["segment", "name"],  # Hierarchical levels: segment > name
        values="headcount",  # Block size determined by headcount
        color="headcount_growth",  # Color determined by headcount growth
        color_continuous_scale=[
            "rgb(226, 72, 66)",  # Red
            "rgb(177, 73, 73)",
            "rgb(130, 72, 79)",
            "rgb(66, 69, 83)",  # Grey
            "rgb(70, 117, 81)",
            "rgb(82, 156, 87)",
            "rgb(102, 201, 104)",  # Green
        ],
        title=f"Competitive landscape of {selected_company}",
    )

    # Enhance layout and styling
    fig.update_layout(
        font=dict(
            family="Arial, sans-serif",  # Modern font
            size=20,  # Larger font size
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
    )

    # Update traces for centered text and percentages
    fig.update_traces(
        textinfo="label+text",  # Display company name and custom text
        texttemplate=("%{label}<br>" "Size: %{value}"),
        textfont=dict(size=16),  # Larger text inside rectangles
        textposition="middle center",  # Center the text in each rectangle
        marker=dict(line=dict(color="black", width=1)),  # Subtle borders for contrast
    )

    return fig
