import plotly.express as px


CHART_PALETTES = [
    ["#9C6CFF", "#B18AFF", "#D8C8FF"],
    ["#FF9279", "#FFB19F", "#FFD2C7"],
    ["#6E9BFF", "#91B3FF", "#C8D7FF"],
    ["#F0B35A", "#F5CB82", "#FBE6B8"],
    ["#D778C4", "#E5A0D8", "#F4D2EE"],
    ["#67C7A2", "#91D9BD", "#C8F0DE"],
]


def _chart_palette(title):
    index = sum(ord(character) for character in title) % len(CHART_PALETTES)
    return CHART_PALETTES[index]


def _style_chart(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#171718",
        plot_bgcolor="#171718",
        colorway=_chart_palette(fig.layout.title.text or "chart"),
        font={"color": "#F4F0F7", "family": "DM Sans, sans-serif"},
        margin={"l": 30, "r": 20, "t": 54, "b": 30},
        title={"font": {"size": 15, "family": "DM Sans, sans-serif"}},
        hovermode="closest",
        hoverlabel={"bgcolor": "#9C6CFF", "font": {"color": "#ffffff"}},
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="#2a282d",
        zeroline=False,
        linecolor="#454149",
    )
    fig.update_yaxes(
        gridcolor="#2a282d",
        zeroline=False,
        linecolor="#454149",
    )
    return fig


def bar_chart(
    data,
    x,
    y,
    title,
    text=None
):

    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        text=text,
        color_discrete_sequence=_chart_palette(title),
    )

    fig.update_layout(
        xaxis_title=x,
        yaxis_title=y
    )

    return _style_chart(fig)


def line_chart(
    data,
    x,
    y,
    title
):

    fig = px.line(
        data,
        x=x,
        y=y,
        title=title,
        color_discrete_sequence=_chart_palette(title),
    )
    fig.update_traces(line={"width": 3})
    return _style_chart(fig)


def scatter_chart(
    data,
    x,
    y,
    color=None,
    title=""
):

    color = color or None
    fig = px.scatter(
        data,
        x=x,
        y=y,
        color=color,
        title=title,
        opacity=0.62,
        color_discrete_sequence=_chart_palette(title),
    )
    return _style_chart(fig)


def histogram(
    data,
    x,
    color=None,
    title="",
    nbins=40,
    log_x=False,
):

    color = color or None
    fig = px.histogram(
        data,
        x=x,
        color=color,
        title=title,
        marginal="box",
        nbins=nbins,
        color_discrete_sequence=_chart_palette(title),
    )
    if log_x:
        fig.update_xaxes(type="log")
    return _style_chart(fig)


def pie_chart(data, names, values, title, hole=0.0):
    fig = px.pie(
        data,
        names=names,
        values=values,
        title=title,
        hole=hole,
        color_discrete_sequence=_chart_palette(title),
    )
    return _style_chart(fig)


def horizontal_bar_chart(data, x, y, title):
    fig = px.bar(
        data,
        x=x,
        y=y,
        orientation="h",
        title=title,
        color=x,
        color_continuous_scale=_chart_palette(title),
    )
    return _style_chart(fig)


def treemap_chart(data, path, values, title):
    fig = px.treemap(
        data,
        path=path,
        values=values,
        title=title,
        color=values,
        color_continuous_scale=_chart_palette(title),
    )
    return _style_chart(fig)


def sunburst_chart(data, path, values, title):
    fig = px.sunburst(
        data,
        path=path,
        values=values,
        title=title,
        color=values,
        color_continuous_scale=_chart_palette(title),
    )
    return _style_chart(fig)


def funnel_chart(data, x, y, title):
    fig = px.funnel(
        data,
        x=x,
        y=y,
        title=title,
        color_discrete_sequence=_chart_palette(title),
    )
    return _style_chart(fig)


def polar_chart(data, theta, radius, title):
    fig = px.line_polar(
        data,
        theta=theta,
        r=radius,
        line_close=True,
        markers=True,
        title=title,
        color_discrete_sequence=_chart_palette(title),
    )
    return _style_chart(fig)


def risk_profile_chart(data, group, title):
    fig = px.bar(
        data.sort_values("default_rate"),
        x="default_rate",
        y=group,
        orientation="h",
        color="risk_level",
        text="default_rate",
        title=title,
        category_orders={
            "risk_level": ["Low risk", "Medium risk", "High risk"],
        },
        color_discrete_map={
            "Low risk": "#2CB7A6",
            "Medium risk": "#D8B34F",
            "High risk": "#E06B52",
        },
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(xaxis_title="Default rate (%)", yaxis_title="")
    return _style_chart(fig)