# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 14:13:05 2022

@author: hermann.ngayap
"""
import os
os.chdir("C:\hjBoralex\etl\gitcwd\dash")

from dash import dcc, html
import plotly.graph_objs as go
from colors import colors
from sql_queries import (query_results_1, query_results_2, query_results_3, 
                         query_results_4, query_results_5, query_results_6, 
                         query_results_7, query_results_8, query_results_9,
                         query_results_10, query_results_11, query_results_12, 
                         query_results_13, query_results_14, query_results_15,
                         query_results_16, query_results_17, query_results_18,
                         query_results_19, query_results_20, query_results_21,
                         query_results_22, query_results_23, query_results_24)

years = ['2022',' 2023', '2024', '2025', '2026', '2027', '2028']
quarters = ['Q1-22', 'Q2-22', 'Q3-22', 'Q4-22', 'Q1-23', 'Q2-23', 'Q3-23', 'Q4-23', 
            'Q1-24', 'Q2-24', 'Q3-24', 'Q4-24', 'Q1-25', 'Q2-25', 'Q3-25', 'Q4-25',
            'Q1-26', 'Q2-26', 'Q3-26', 'Q4-26', 'Q1-27', 'Q2-27', 'Q3-27', 'Q4-27',
            'Q1-28', 'Q2-28', 'Q3-28', 'Q4-28']
months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug',' sep', 'oct', 'nov', 'dec']

BAR_H_WIDTH = 2 
PLOTS_FONT_SIZE = 11
PLOTS_HEIGHT = 340  # For main graphs
SMALL_PLOTS_HEIGHT = 290  # For secondary graphs

year_count = []
for year in query_results_19['année'].unique():
    year_count.append({'label':str(year),'value':year})
    
not_oa_cr_ppa_year=html.Div(
    children=[
        dcc.Graph(id="m_ppa_cr_y",
                  figure = {'data':[
                       go.Bar(
                          name='CR', 
                          x=years, 
                          y=query_results_22['Coverage_Ratio'],
                          opacity=0.02,
                          marker=dict(color=colors['white']),
                          marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color']),
                          textposition='outside',
                          textfont = dict(family="Times", size= 10, color= colors["white"]),
                              ),
                       go.Bar(
                          name='PPA', 
                          x=years, 
                          y=query_results_16['ppa_y'],
                          opacity=0.2,
                          marker=dict(color=colors['ppa']),
                          marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color'])
                          ),
                     go.Bar(
                         name='Prod_Not_OA_CR', 
                         x=years, 
                         y=query_results_19['not_oa_cr_y'],
                         opacity=0.4,
                         marker=dict(color=colors['e_white']),                             
                         marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color']) 
                         ), 
                     ], 
                      'layout':go.Layout(title='Prod NOT OA CR hedged with PPA/year',
                                         annotations=[dict(x=years[0], y=(query_results_19.iloc[0, 1]), text=query_results_22.iloc[0, 1], showarrow=False, align='center', 
                                                            font=dict(size=8)), 
                                                        dict(x=years[1], y=(query_results_19.iloc[1, 1]),text=query_results_22.iloc[1, 1], showarrow=False, align='center', font=dict(size=8)),
                                                        dict(x=years[2], y=(query_results_19.iloc[2, 1]),text=query_results_22.iloc[2, 1], showarrow=False, align='center', font=dict(size=8)),
                                                        dict(x=years[3], y=(query_results_19.iloc[3, 1]),text=query_results_22.iloc[3, 1], showarrow=False, align='center', font=dict(size=8)),
                                                        dict(x=years[4], y=(query_results_19.iloc[4, 1]),text=query_results_22.iloc[4, 1], showarrow=False, align='center', font=dict(size=8)),
                                                        dict(x=years[5], y=(query_results_19.iloc[5, 1]),text=query_results_22.iloc[5, 1], showarrow=False, align='center', font=dict(size=8)),
                                                        dict(x=years[6], y=(query_results_19.iloc[6, 1]),text=query_results_22.iloc[6, 1], showarrow=False, align='center', font=dict(size=8))],
                                         xaxis=dict(gridcolor=colors['grid'], title='year', dtick=1, tickangle = 45), 
                                         yaxis=dict(gridcolor=colors['grid'], title='GWh', side='left'),
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
        ]
    )