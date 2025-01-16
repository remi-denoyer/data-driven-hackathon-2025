import plotly.express as px


def create_tree_map(data, selected_company):
    fig = px.treemap(
        data,
        path=["segment", "name"],  # Hierarchical levels: category > name
        values="headcount",  # Block size determined by headcount
        color="headcount_growth",  # Color determined by growth
        color_continuous_scale=["green", "yellow", "red"],  # Custom green-to-red scale
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
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent background
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
        margin=dict(t=50, l=25, r=25, b=25),  # Reduce margins for better space usage
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
