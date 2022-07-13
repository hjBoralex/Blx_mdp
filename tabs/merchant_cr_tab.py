# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 17:52:09 2022

@author: hermann.ngayap
"""
from dash import dcc, html
import plotly.graph_objs as go
from colors import colors

from graphs.not_oa_cr_ppa_year_graph import not_oa_cr_ppa_year
from graphs.not_oa_cr_ppa_qtr_graph import not_oa_cr_ppa_qtr
from graphs.not_oa_cr_ppa_mth_graph import not_oa_cr_ppa_mth


merchant_cr_layout=html.Div(
    children=[
            html.Div(
            className="central-panel1-title",
            children=["Prod Merchant"],
            ),
            
            html.Div(
           className="central-panel1",
           children=[
               html.Div(
                   children=[
                       html.Div(
                           style={
                               "display": "inline-block",
                               "vertical-align": "top",
                               "width": "70%",
                           },
                           children=[
                               not_oa_cr_ppa_year,
                               not_oa_cr_ppa_qtr,
                               not_oa_cr_ppa_mth
                               ]
                           )
                       ]
                   )]
           )],
    )



