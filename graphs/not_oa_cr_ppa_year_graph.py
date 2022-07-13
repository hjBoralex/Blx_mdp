# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 12:05:34 2022

@author: hermann.ngayap
"""
from dash import dcc, html
import plotly.graph_objs as go
from colors import colors
from tables.prod_merchant_table import prod_merchant_tbl
from functions import make_dbc_table
from sql_queries import (query_results_1, query_results_2, query_results_3, 
                         query_results_4, query_results_5, query_results_6, 
                         query_results_7, query_results_8, query_results_9,
                         query_results_10, query_results_11, query_results_12, 
                         query_results_13, query_results_14, query_results_15,
                         query_results_16, query_results_17, query_results_18,
                         query_results_19, query_results_20, query_results_21,
                         query_results_22, query_results_23, query_results_24)

years = ['2022',' 2023', '2024', '2025', '2026', '2027', '2028']

BAR_H_WIDTH = 2 
PLOTS_FONT_SIZE = 11
PLOTS_HEIGHT = 340  # For main graphs
SMALL_PLOTS_HEIGHT = 290  # For secondary graphs

year_count = []
for year in query_results_19['année'].unique():
    year_count.append({'label':str(year),'value':year})

not_oa_cr_ppa_year= html.Div(
    children=[
        html.Div(
            className="central-panel1",
            children=[
                html.Div(
                    children=[
                        html.Div(
                            style={
                                "display": "inline-block",
                                "vertical-align": "top",
                                "width": "50%",
                            },
                            children=[
                                dcc.Graph(id="m_ppa_cr_y",
                                          figure = {'data':[
                                               go.Bar(
                                                  name='HCR', 
                                                  x=years, 
                                                  y=query_results_22['coverage_ratio'],
                                                  opacity=0,
                                                  marker=dict(color=colors['white']),
                                                  marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color']),
                                                  textposition='outside',
                                                  textfont = dict(family="Times", size= 10, color= colors["white"]),
                                                      ),
                                               go.Bar(
                                                  name='PPA', 
                                                  x=years, 
                                                  y=query_results_16['ppa_year'],
                                                  opacity=1,
                                                  marker=dict(color=colors['ppa']),
                                                  marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color'])
                                                  ),
                                               go.Bar(
                                                 name='Prod Merchant', 
                                                 x=years, 
                                                 y=query_results_19['prod_merchant_year'],
                                                 opacity=0.25,
                                                 marker=dict(color=colors['e_white']),                             
                                                 marker_line=dict(width= BAR_H_WIDTH, color=colors['bar_h_color']) 
                                                 ), 
                                             ], 
                                              'layout':go.Layout(title='Prod Merchant Hedged with PPA/year',
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
                                                                 hovermode="x unified")}),
                                ],
                        ),
                        html.Div(
                            style={
                                "display": "inline-block",
                                "margin-top": "0px",
                                "margin-left": "25px",
                                "width": "25%",
                            },
                            children=[
                                html.Div(
                                    children=[
                                        prod_merchant_tbl
                                        ],
                                    className="table",
                                )
                            ],
                        ),
                    ]
                ),

            ],
        ),
    ],
    id="container_prod_fc",
)