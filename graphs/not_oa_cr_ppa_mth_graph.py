# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 14:13:07 2022

@author: hermann.ngayap
"""
import plotly.graph_objs as go
from colors import colors
from dash import dcc, html
from sql_queries import (query_results_1, query_results_2, query_results_3, 
                        query_results_4, query_results_5, query_results_6, 
                        query_results_7, query_results_8, query_results_9,
                        query_results_10, query_results_11, query_results_12, 
                        query_results_13, query_results_14, query_results_15,
                        query_results_16, query_results_17, query_results_18,
                        query_results_19, query_results_20, query_results_21,
                        query_results_22, query_results_23, query_results_24)

months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug',' sep', 'oct', 'nov', 'dec']

BAR_H_WIDTH = 2 
PLOTS_FONT_SIZE = 11
PLOTS_HEIGHT = 340  # For main graphs
SMALL_PLOTS_HEIGHT = 290  # For secondary graphs

year_count = []
for year in query_results_19['année'].unique():
    year_count.append({'label':str(year),'value':year})
    
not_oa_cr_ppa_mth=html.Div(
    children=[
        #Dropdown hedge with ppa/month
        dcc.Dropdown(id='drop_year_m_ppa_m', options=year_count, value=query_results_19['année'].min(),
        style=dict(width='40%',verticalAlign="center", display='inline-block')),
        #Merchant hedge with ppa/month 
        dcc.Graph(id="m_ppa_cr_mth",
              figure = {'data':[
                  go.Bar(
                          name='HCR', 
                          x=months, 
                          y=query_results_24['coverage_ratio'],
                          opacity=0,
                          marker=dict(color=colors['white']),
                          marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color']),
                          textposition='outside',
                          textfont = dict(family="Times", size= 10, color= colors["white"]),
                          ),
                 go.Bar(
                      name='PPA', 
                      x=months, 
                      y=query_results_18['ppa_mth'],
                      opacity=1,
                      marker=dict(color=colors['ppa']),
                      marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color'])
                      ),
                 go.Bar(
                     name='Prod Merchant', 
                     x=months, 
                     y=query_results_21['prod_merchant_mth'],
                     opacity=0.25,
                     marker=dict(color=colors['e_white']),                             
                     marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color']) 
                     ), 
                 ], 
                  'layout':go.Layout(title='Prod Merchant Hedged with PPA/Month',
                                     annotations=[dict(x=months[0], y=(query_results_21.iloc[0, 3]), text=query_results_24.iloc[0, 3], showarrow=False, align='center', font=dict(size=8)), 
                                                    dict(x=months[1], y=(query_results_21.iloc[1, 3]),text=query_results_24.iloc[1, 3], showarrow=False, align='center', font=dict(size=8)),
                                                    dict(x=months[2], y=(query_results_21.iloc[2, 3]),text=query_results_24.iloc[2, 3], showarrow=False, align='center', font=dict(size=8)),
                                                    dict(x=months[3], y=(query_results_21.iloc[3, 3]),text=query_results_24.iloc[3, 3], showarrow=False, align='center', font=dict(size=8)),
                                                    dict(x=months[4], y=(query_results_21.iloc[4, 3]),text=query_results_24.iloc[4, 3], showarrow=False, align='center', font=dict(size=8)),
                                                    dict(x=months[5], y=(query_results_21.iloc[5, 3]),text=query_results_24.iloc[5, 3], showarrow=False, align='center', font=dict(size=8)),
                                                    dict(x=months[6], y=(query_results_21.iloc[6, 3]),text=query_results_24.iloc[6, 3], showarrow=False, align='center', font=dict(size=8)),
                                                    
                                                    dict(x=months[7], y=(query_results_21.iloc[7, 3]),text=query_results_24.iloc[7, 3], showarrow=False, align='center', font=dict(size=8)),
                                                    dict(x=months[8], y=(query_results_21.iloc[8, 3]),text=query_results_24.iloc[8, 3], showarrow=False, align='center', font=dict(size=8)),
                                                    dict(x=months[9], y=(query_results_21.iloc[9, 3]),text=query_results_24.iloc[9, 3], showarrow=False, align='center', font=dict(size=8)),
                                                    dict(x=months[10], y=(query_results_21.iloc[10, 3]),text=query_results_24.iloc[10, 3], showarrow=False, align='center', font=dict(size=8)),
                                                    dict(x=months[11], y=(query_results_21.iloc[11, 3]),text=query_results_24.iloc[11, 3], showarrow=False, align='center', font=dict(size=8))
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
              style={'width': '65%', 'height':'10%', 'display': 'inline-block', 'vertical-align': 'top'},
              ),
        
        ]
    )
