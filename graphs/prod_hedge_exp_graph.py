# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 09:41:36 2022

@author: hermann.ngayap
"""
from dash import dcc, html
import plotly.graph_objs as go
from colors import colors
from x_axes import years, quarters, months 
from sql_queries import (query_results_1, query_results_2, query_results_3, 
                         query_results_4, query_results_5, query_results_6, 
                         query_results_7, query_results_8, query_results_9,
                         query_results_10, query_results_11, query_results_12, 
                         query_results_13, query_results_14, query_results_15,
                         query_results_16, query_results_17, query_results_18,
                         query_results_19, query_results_20, query_results_21,
                         query_results_22, query_results_23, query_results_24
                         )

BAR_H_WIDTH = 2 
PLOTS_FONT_SIZE = 11
PLOTS_HEIGHT = 340  # For main graphs
SMALL_PLOTS_HEIGHT = 290  # For secondary graphs

year_count = []
for year in years['years'].unique():
    year_count.append({'label':str(year),'value':year})
    
    
prod_hedge_exp_graph=html.Div(
    
    children=[
    html.H2(
        children="Production/Hedge/Exposure",
        style={
            "font-size": 14,
            "margin-bottom": "0em",
            "margin-top": "1em",
            },
        ),
    #Hedge per year
    dcc.Graph(id='hedge_type_y',
              figure = {'data':[
 
                  go.Bar(
                      name='HCR', 
                      x=years['years'], 
                      y=query_results_7['hcr_per_year'],
                      opacity=0,
                      marker=dict(color=colors['white']),
                      marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color']),
                      #textposition='outside',
                      #textfont = dict(family="Times", size= 10, color= colors["white"]),
                      ),
                  go.Bar(
                      name='PPA', 
                      x=years['years'], 
                      y=query_results_4.loc[query_results_4['type_contract'] == 'PPA', 'hedge'],
                      opacity=1,
                      marker=dict(color=colors['ppa']),
                      marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color'])
                      ),
                  go.Bar(
                      name='OA', 
                      x=years['years'], 
                      y=query_results_4.loc[query_results_4['type_contract'] == 'OA', 'hedge'],
                      opacity=0.4,
                      marker=dict(color=colors['oa']),
                      marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color'])
                      ),
                  go.Bar(
                      name='CR', 
                      x=years['years'], 
                      y=query_results_4.loc[query_results_4['type_contract'] == 'CR', 'hedge'],
                      opacity=0.25,
                      marker=dict(color=colors['cr']),
                      marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color'])
                      ),

                 go.Bar(
                     name='Production', 
                     x=years['years'], 
                     y=query_results_10['prod_per_year'],
                     opacity=0.09,
                     marker=dict(color=colors['e_white']),                             
                     marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color']) 
                     ), 
                 ], 
                  'layout':go.Layout(title='',
                                     annotations=[dict(x=years['years'][0], y=(query_results_10.iloc[0, 1])+20, text=query_results_7.iloc[0, 1], showarrow=False, align='center', 
                                                       font=dict(size=8)), 
                                                  dict(x=years['years'][1], y=(query_results_10.iloc[1, 1])+20,text=query_results_7.iloc[1, 1], showarrow=False, align='center', font=dict(size=8)),
                                                  dict(x=years['years'][2], y=(query_results_10.iloc[2, 1])+20,text=query_results_7.iloc[2, 1], showarrow=False, align='center', font=dict(size=8)),
                                                  dict(x=years['years'][3], y=(query_results_10.iloc[3, 1])+20,text=query_results_7.iloc[3, 1], showarrow=False, align='center', font=dict(size=8)),
                                                  dict(x=years['years'][4], y=(query_results_10.iloc[4, 1])+20,text=query_results_7.iloc[4, 1], showarrow=False, align='center', font=dict(size=8)),
                                                  dict(x=years['years'][5], y=(query_results_10.iloc[5, 1])+20,text=query_results_7.iloc[5, 1], showarrow=False, align='center', font=dict(size=8)),
                                                  dict(x=years['years'][6], y=(query_results_10.iloc[6, 1])+20,text=query_results_7.iloc[6, 1], showarrow=False, align='center', font=dict(size=8))],
                                     xaxis=dict(gridcolor=colors['grid'], title='year', dtick=1, tickangle = 45), 
                                     yaxis=dict(gridcolor=colors['grid'], title='GWh', side='left'),
                                     yaxis2=dict(gridcolor=colors['grid'], title='GWh', side='right', showline=True),
                                     barmode='overlay',
                                     paper_bgcolor = colors["background1"],
                                     plot_bgcolor= colors["background1"],
                                     font=dict(color=colors["text"], size=PLOTS_FONT_SIZE),
                                     showlegend=True,
                                     legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                                     hovermode="x unified")
                  },
              style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'top'},
              ),
    #Dropdown Hedge per quarter
    dcc.Dropdown(id='drop_year_h_q', options=year_count, value=years['years'].min(), 
                 style=dict(width='40%', verticalAlign="left", display='inline-block')),
    #Hedge per quarter
    dcc.Graph(id='hedge_type_q',
              figure = {'data':[
 
                 go.Bar(
                      name='HCR', 
                      x=quarters['quarters'], 
                      y=query_results_8['hcr_per_quarter'],
                      opacity=0,
                      marker=dict(color=colors['white']),
                      marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color']),
                      textposition = "outside",
                      textfont = dict(family="Times", size= 10, color= colors["white"]),
                      ), 
                  go.Bar(
                      name='PPA',
                      x=quarters['quarters'],
                      y=query_results_5.loc[query_results_5['type_contract']=='PPA', 'hedge'],
                      opacity=1,
                      marker=dict(color=colors['ppa']),
                      marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color'])
                      ),
                  go.Bar(
                      name='OA',
                      x=quarters['quarters'],
                      y=query_results_5.loc[query_results_5['type_contract']=='OA', 'hedge'],
                      opacity=0.4,
                      marker=dict(color=colors['oa']),
                      marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color'])
                      ),
                  go.Bar(
                      name='CR',
                      x=quarters['quarters'],
                      y=query_results_5.loc[query_results_5['type_contract']=='CR', 'hedge'],
                      opacity=0.25,
                      marker=dict(color=colors['cr']),
                      marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color'])
                      ),
 
                  go.Bar(
                      name='Production', 
                      x=quarters['quarters'],
                      y=query_results_11['prod_per_quarter'],
                      opacity=0.1,
                      marker=dict(color=colors['e_white']),
                      marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color']),

                     ),
                  ],
                  'layout':go.Layout(title='',
                                     annotations=[dict(x=quarters['quarters'][0], y=(query_results_11.iloc[0, 3])+20, text=query_results_8.iloc[0, 3], showarrow=False, align='center', font=dict(size=8)), 
                                                  dict(x=quarters['quarters'][1], y=(query_results_11.iloc[1, 3])+20, text=query_results_8.iloc[1, 3], showarrow=False, align='center', font=dict(size=8)),
                                                  dict(x=quarters['quarters'][2], y=(query_results_11.iloc[2, 3])+20, text=query_results_8.iloc[2, 3], showarrow=False, align='center', font=dict(size=8)),
                                                  dict(x=quarters['quarters'][3], y=(query_results_11.iloc[3, 3])+20, text=query_results_8.iloc[3, 3], showarrow=False, align='center', font=dict(size=8))],
                                     xaxis=dict(gridcolor=colors['grid'], title='quarter'), 
                                     yaxis=dict(gridcolor=colors['grid'], title ='GWh', side='left'),
                                     barmode='overlay',
                                     paper_bgcolor = colors["background1"],
                                     plot_bgcolor= colors["background1"],
                                     font=dict(color=colors["text"], size=PLOTS_FONT_SIZE),
                                     showlegend=True,
                                     legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                                     hovermode="x unified",
                                     ),
                  }, 
              style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'top'},
              ),
 
    #Dropdown Hedge per month
    dcc.Dropdown(id='drop_year_h_m',options=year_count,value=query_results_6['année'].min(), 
         style=dict(width='40%', verticalAlign="left", display='inline-block')),
    #Hedge per month
    dcc.Graph(id='hedge_type_m',
              figure = {'data':[
                  go.Bar(
                       name='HCR', 
                       x=months['months'], 
                       y=query_results_9['hcr_per_month'],
                       opacity=0,
                       marker=dict(color=colors['white']),
                       marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color']),
                       textposition = "outside",
                       textfont = dict(family="Times", size= 10, color= colors["white"]),
                       ), 
                  go.Bar(
                      name="0A",   
                      x=months['months'],
                      y=query_results_6.loc[query_results_6['type_contract'] == 'OA', 'hedge'],
                      opacity=0.4,
                      marker=dict(color=colors['oa']),
                      marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color'])
                      ),
                  go.Bar(
                      name="CR",
                      x=months['months'],
                      y=query_results_6.loc[query_results_6['type_contract'] == 'CR', 'hedge'],
                      opacity=0.25,
                      marker=dict(color=colors['cr']),
                      marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color'])
                      ), 
                  go.Bar(
                      name="PPA",
                      x=months['months'],
                      y=query_results_6.loc[query_results_6['type_contract'] == 'PPA', 'hedge'],
                      opacity=1,
                      marker=dict(color=colors['ppa']),
                      marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color'])
                      ),
                  go.Bar(
                      name='Production', 
                      x=months['months'],
                      y=query_results_12['prod_per_month'],
                      opacity=0.1,
                      marker=dict(color=colors['e_white']),
                      marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color']),

                     ),
                  ],
                  
                  'layout':go.Layout(title='',
                                     annotations=[dict(x=months['months'][0], y=(query_results_12.iloc[0, 3]), text=query_results_9.iloc[0, 3], showarrow=False, align='center', font=dict(size=8)), 
                                                  dict(x=months['months'][1], y=(query_results_12.iloc[1, 3]), text=query_results_9.iloc[1, 3], showarrow=False, align='center', font=dict(size=8)),
                                                  dict(x=months['months'][2], y=(query_results_12.iloc[2, 3]), text=query_results_9.iloc[2, 3], showarrow=False, align='center', font=dict(size=8)),
                                                  dict(x=months['months'][3], y=(query_results_12.iloc[3, 3]), text=query_results_9.iloc[3, 3], showarrow=False, align='center', font=dict(size=8)),
                                                  dict(x=months['months'][4], y=(query_results_12.iloc[4, 3]), text=query_results_9.iloc[4, 3], showarrow=False, align='center', font=dict(size=8)), 
                                                  dict(x=months['months'][5], y=(query_results_12.iloc[5, 3]), text=query_results_9.iloc[5, 3], showarrow=False, align='center', font=dict(size=8)),
                                                  dict(x=months['months'][6], y=(query_results_12.iloc[6, 3]), text=query_results_9.iloc[6, 3], showarrow=False, align='center', font=dict(size=8)),
                                                  dict(x=months['months'][7], y=(query_results_12.iloc[7, 3]), text=query_results_9.iloc[7, 3], showarrow=False, align='center', font=dict(size=8)),
                                                  dict(x=months['months'][8], y=(query_results_12.iloc[8, 3]), text=query_results_9.iloc[8, 3], showarrow=False, align='center', font=dict(size=8)),
                                                  dict(x=months['months'][9], y=(query_results_12.iloc[9, 3]), text=query_results_9.iloc[9, 3], showarrow=False, align='center', font=dict(size=8)),
                                                  dict(x=months['months'][10], y=(query_results_12.iloc[10, 3]), text=query_results_9.iloc[10, 3], showarrow=False, align='center', font=dict(size=8)), 
                                                  dict(x=months['months'][11], y=(query_results_12.iloc[11, 3]), text=query_results_9.iloc[11, 3], showarrow=False, align='center', font=dict(size=8))
                                                  ],
                                     xaxis = dict(gridcolor=colors['grid'], title='months', dtick=1, tickangle = 45), 
                                     yaxis= dict(gridcolor=colors['grid'], title= 'GWh'),
                                     barmode='overlay',
                                     paper_bgcolor = colors["background1"],
                                     plot_bgcolor= colors["background1"],
                                     font=dict(color=colors["text"], size=PLOTS_FONT_SIZE),
                                     showlegend=True,
                                     legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                                     hovermode="x unified"
                                     )},
              style={'width': '100%', 'display': 'block', 'vertical-align': 'top'}
              ),
        
        ],
    )