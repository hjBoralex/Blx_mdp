# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 14:13:05 2022

@author: hermann.ngayap
"""
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


quarters = ['Q1', 'Q2', 'Q3', 'Q4']


BAR_H_WIDTH = 2 
PLOTS_FONT_SIZE = 11
PLOTS_HEIGHT = 340  # For main graphs
SMALL_PLOTS_HEIGHT = 290  # For secondary graphs

year_count = []
for year in query_results_19['année'].unique():
    year_count.append({'label':str(year),'value':year})
    
not_oa_cr_ppa_qtr=html.Div(
    children=[
        #Dropdown Merchant hedged with ppa/quarter
        dcc.Dropdown(id='drop_year_m_ppa_q', options=year_count, value=query_results_19['année'].min(),
        style=dict(width='40%',verticalAlign="center", display='inline-block')),
        #Merchant hedged with ppa/quarter
        dcc.Graph(id="m_ppa_cr_q",
                  figure = {'data':[
                      go.Bar(
                           name='HCR', 
                           x=quarters, 
                           y=query_results_23['coverage_ratio'],
                           opacity=0,
                           marker=dict(color=colors['white']),
                           marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color']),
                           textposition='outside',
                           textfont = dict(family="Times", size= 10, color= colors["white"]),
                              ),
                      go.Bar(
                          name='PPA', 
                          x=quarters, 
                          y=query_results_17['ppa_qtr'],
                          opacity=1,
                          marker=dict(color=colors['ppa']),
                          marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color'])
                          ),
                     go.Bar(
                         name='Prod Merchant', 
                         x=quarters, 
                         y=query_results_20['prod_merchant_qtr'],
                         opacity=0.25,
                         marker=dict(color=colors['e_white']),                             
                         marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color']) 
                         ), 
                     ], 
                      'layout':go.Layout(title='Prod Merchant Hedged with PPA/Quarter',
                                         annotations=[dict(x=quarters[0], y=(query_results_20.iloc[0, 3]), text=query_results_23.iloc[0, 3], showarrow=False, align='center', font=dict(size=8)), 
                                                        dict(x=quarters[1], y=(query_results_20.iloc[1, 3]),text=query_results_23.iloc[1, 3], showarrow=False, align='center', font=dict(size=8)),
                                                        dict(x=quarters[2], y=(query_results_20.iloc[2, 3]),text=query_results_23.iloc[2, 3], showarrow=False, align='center', font=dict(size=8)),
                                                        dict(x=quarters[3], y=(query_results_20.iloc[3, 3]),text=query_results_23.iloc[3, 3], showarrow=False, align='center', font=dict(size=8))
                                                        ],
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
                  style={'width': '65%', 'display': 'inline-block', 'vertical-align': 'top'},
                  ),
        ]
    )