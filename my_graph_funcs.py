import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64

def avg_lap_speed_ts(df, max_speeds, min_speeds):

    constructor_names = {'alfa': 'Alfa Romeo', 'alphatauri': 'AlphaTauri',
                         'mclaren': 'McLaren', 'mercedes': 'Mercedes', 'racing_point': 'Racing Point',
                         'red_bull': 'Red Bull', 'renault': 'Renault',
                         'ferrari': 'Ferrari', 'haas': 'Haas', 'williams': 'Williams'}

    line_map = {'mercedes': 'solid', 'red_bull': 'solid',
                'racing_point': 'dash', 'mclaren': 'solid',
                'renault': 'solid', 'ferrari': 'solid', 'alphatauri': 'dot',
                'alfa': 'dot', 'haas': 'dash', 'williams': 'dot'}

    col_map = {'mercedes': '#484848',
               'red_bull': '#4575b4',
               'racing_point': '#484848',
               'mclaren': '#fc8d59',
               'renault': '#fee090',
               'ferrari': '#d73027',
               'alphatauri': '#4575b4',
               'alfa': '#d73027',
               'haas': '#d73027',
               'williams': '#484848'}

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=max_speeds['year'], y=max_speeds['avg_lap_speed'],
                             fill=None,
                             mode='lines',
                             line_color='rgb(217, 217, 217)',
                             hovertemplate='<b>Max Speed: </b>%{y}<br><extra></extra>',
                             showlegend=False))

    fig.add_trace(go.Scatter(x=min_speeds['year'], y=min_speeds['avg_lap_speed'],
                             fill='tonexty',
                             mode='lines', line_color='rgb(217, 217, 217)',
                             hovertemplate='<b>Min Speed: </b>%{y}<br><extra></extra>',
                             name="Average Speed Range"))

    for key, grp in df.groupby(['constructorRef_mapped']):
        fig.add_trace(go.Scatter(x=grp['year'], y=grp['avg_lap_speed'],
                                 mode='lines',
                                 line=dict(color=col_map[key], dash=line_map[key]),
                                 name=constructor_names[key],
                                 hovertemplate=
                                 f'<b>Constructor:</b> {constructor_names[key]} <br>' +
                                 '<b>Drivers:</b> %{text}<extra></extra>',
                                 text=df.loc[(df.constructorRef_mapped == key), "drivers"], ))

    fig.add_vrect(
        x0="1996", x1="2005",
        fillcolor="azure",  # opacity=0.5,
        layer="below", line_width=0,
    ),

    fig.add_vrect(
        x0="2005", x1="2013",
        fillcolor="cornsilk",  # opacity=0.5,
        layer="below", line_width=0,
    ),

    fig.add_vrect(
        x0="2013", x1="2020",
        fillcolor="honeydew",  # opacity=0.5,
        layer="below", line_width=0,
    ),

    fig.add_annotation(x=2005, y=3.53,
                       xref="x", yref="y", ax=1996, ay=3.53,
                       axref="x", ayref="y",
                       arrowhead=5, arrowside="end+start", arrowsize=1.5, arrowcolor='teal')

    fig.add_annotation(x=2000.5, y=3.55, text="<b>V10/12 Engines</b>",
                       showarrow=False, font=dict(size=18, color='teal'))

    fig.add_annotation(x=2005, y=3.53,
                       xref="x", yref="y", ax=2013, ay=3.53,
                       axref="x", ayref="y",
                       arrowhead=5, arrowside="end+start", arrowsize=1.5, arrowcolor='IndianRed')

    fig.add_annotation(x=2009, y=3.55, text="<b>V8 Engines</b>",
                       showarrow=False, font=dict(size=18, color='IndianRed'))

    fig.add_annotation(x=2020, y=3.53,
                       xref="x", yref="y", ax=2013, ay=3.53,
                       axref="x", ayref="y",
                       arrowhead=5, arrowside="end+start", arrowsize=1.5, arrowcolor='darkgreen')

    fig.add_annotation(x=2016.5, y=3.55, text="<b>V6 Hybrid Engines</b>",
                       showarrow=False, font=dict(size=18, color='darkgreen'))

    fig.update_layout(
        autosize=False,
        width=1175,
        height=800,

        plot_bgcolor='rgba(0,0,0,0)',

        title=dict(
            text="<b>Average Speed by Constructor</b>",
            xanchor='left',
            yanchor='top',
            y=0.92,
            x=0.1
        ),

        #legend=dict(
        #    title_text="<b>Constructors</b>",
        #),

        yaxis=dict(
            range=[2.9, 3.58],
            title_text="<b>Km/min</b>",
            tickwidth=2,
            ticks="outside",
            ticklen=10,
            tickprefix="<b>", ticksuffix="</b>",
            tickfont=dict(size=15),
            showline=True,
            linewidth=2,
            linecolor='black',
            gridcolor='lightGray'
        ),

        xaxis=dict(
            range=[1995, 2021],
            tick0=1996,
            dtick=2,
            title_text="<b>Year</b>",
            tickwidth=2,
            ticks="outside",
            tickprefix="<b>", ticksuffix="</b>",
            ticklen=10,
            showline=True,
            linewidth=2,
            linecolor='black',
            gridcolor='lightGray'
        ),

        font=dict(
            size=15,
            color='black')
    )


    return fig

def engine_barplot(df, df_exp, df_count):

    with open("logos/ferrari.png", "rb") as image_file_ferrari:
        encoded_string = base64.b64encode(image_file_ferrari.read()).decode()
    # Add the prefix that plotly will want when using the string as source
    encoded_image_ferrari = "data:image/png;base64," + encoded_string

    with open("logos/mercedes.png", "rb") as image_file_mercedes:
        encoded_string = base64.b64encode(image_file_mercedes.read()).decode()
    # Add the prefix that plotly will want when using the string as source
    encoded_image_mercedes = "data:image/png;base64," + encoded_string

    with open("logos/renault.png", "rb") as image_file_renault:
        encoded_string = base64.b64encode(image_file_renault.read()).decode()
    encoded_image_renault = "data:image/png;base64," + encoded_string

    col_map = {'mercedes': 'royalBlue',
               'renault': 'goldenrod',
               'ferrari': 'firebrick'}

    name_map = {'mercedes': 'Mercedes',
                'renault': 'Renault',
                'ferrari': 'Ferrari'}

    fig = make_subplots(rows=3, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.05,
                        # subplot_titles=('<b>Ferrari</b>', '<b>Mercedes</b>', '<b>Renault</b>')
                        )

    i = 1
    ypos = [0.95, 0.6, 0.25]

    for engine in df['engine'].unique():

        leg_bool = True
        tl = 10
        xtitle = "<b>Year</b>"
        ytitle = ""
        if i < 3:
            leg_bool = False
            tl = 0
            xtitle = ""
        if i == 2:
            ytitle = "<b>Win Count</b>"

        df1 = df.loc[df.engine == engine, :]
        fig.add_trace(go.Bar(
            x=df1['year'],
            y=df1['engine_win_count'],
            name=name_map[engine],
            marker_color=col_map[engine],
            hovertemplate=
            '<b>Year: :</b> %{x} <br>' +
            '<b>Win Count: </b>%{y}<extra></extra>',
            showlegend=False
        ), row=i, col=1)

        df2 = df_exp.loc[df_exp.engine == engine, :]
        fig.add_trace(go.Scatter(
            x=df2['year'],
            y=df2['expected wins'],
            mode='lines+markers',
            line=dict(color='black', dash='dash', width=2),
            marker=dict(symbol='circle', size=5),
            name='<b>Expected Win Count</b>',
            hovertemplate=
            '<b>Year: :</b> %{x} <br>' +
            '<b>Teams With Engine: </b>%{text}<br>' +
            '<b>Expected Win Count: </b>%{y}<extra></extra>',
            text=df_count.loc[(df_count.engine == engine), "engine_count"],
            showlegend=leg_bool
        ), row=i, col=1)

        fig.update_yaxes(
            range=[0, 20.5],
            title_text=ytitle,
            tickwidth=2,
            ticks="outside",
            ticklen=10,
            tickprefix="<b>", ticksuffix="</b>",
            tickfont=dict(size=15),
            showline=True,
            linewidth=2,
            linecolor='black',
            gridcolor='lightGray',
            row=i, col=1),

        fig.update_xaxes(
            range=[1995, 2020.5],
            tick0=1996,
            dtick=2,
            title_text=xtitle,
            tickwidth=2,
            ticks="outside",
            tickprefix="<b>", ticksuffix="</b>",
            ticklen=tl,
            showline=True,
            linewidth=2,
            linecolor='black',
            row=i, col=1),

        # fig.layout.annotations[i-1].update(x=0.02, y=ypos[i-1], xanchor='left', font=dict(size=20))

        i = i + 1

    fig.add_vrect(
        x0="1995", x1="2005.5",
        fillcolor="azure",  # opacity=0.5,
        layer="below", line_width=0,
    ),

    fig.add_vrect(
        x0="2005.5", x1="2013.5",
        fillcolor="cornsilk",  # opacity=0.5,
        layer="below", line_width=0,
    ),

    fig.add_vrect(
        x0="2013.5", x1="2021",
        fillcolor="honeydew",  # opacity=0.5,
        layer="below", line_width=0,
    ),

    fig.add_annotation(x=2005.5, y=17,
                       xref="x", yref="y", ax=1995.5, ay=17,
                       axref="x", ayref="y",
                       arrowhead=5, arrowside="end+start", arrowsize=1.5, arrowcolor='teal')

    fig.add_annotation(x=2000.5, y=18.5, text="<b>V10/12 Engines</b>",
                       showarrow=False, font=dict(size=18, color='teal'))

    fig.add_annotation(x=2005.5, y=17,
                       xref="x", yref="y", ax=2013.5, ay=17,
                       axref="x", ayref="y",
                       arrowhead=5, arrowside="end+start", arrowsize=1.5, arrowcolor='IndianRed')

    fig.add_annotation(x=2009.5, y=18.5, text="<b>V8 Engines</b>",
                       showarrow=False, font=dict(size=18, color='IndianRed'))

    fig.add_annotation(x=2020.5, y=17,
                       xref="x", yref="y", ax=2013.5, ay=17,
                       axref="x", ayref="y",
                       arrowhead=5, arrowside="end+start", arrowsize=1.5, arrowcolor='darkgreen')

    fig.add_annotation(x=2017, y=18.5, text="<b>V6 Hybrid Engines</b>",
                       showarrow=False, font=dict(size=18, color='darkgreen'))

    fig.add_layout_image(
        dict(
            source=encoded_image_ferrari,
            xref="paper", yref="paper",
            x=0.15, y=0.84,
            sizex=0.15, sizey=0.15,
            xanchor="right", yanchor="bottom"
        )
    )

    fig.add_layout_image(
        dict(
            source=encoded_image_mercedes,
            xref="paper", yref="paper",
            x=0.22, y=0.57,
            sizex=0.2, sizey=0.2,
            xanchor="right", yanchor="bottom"
        )
    )

    fig.add_layout_image(
        dict(
            source=encoded_image_renault,
            xref="paper", yref="paper",
            x=0.17, y=0.23,
            sizex=0.15, sizey=0.15,
            xanchor="right", yanchor="bottom"
        )
    )

    fig.update_layout(
        autosize=False,
        width=1000,
        height=800,

        plot_bgcolor='rgba(0,0,0,0)',

        title=dict(
            text="<b>F1 Grand Prix Wins by Engine Manufacturer </b>",
            xanchor='left',
            yanchor='top',
            y=0.92,
            x=0.1
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right", x=1
        ),

        font=dict(
            size=15,
            color='black')
    )

    return fig


