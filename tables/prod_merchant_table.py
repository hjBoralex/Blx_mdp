# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 11:54:42 2022

@author: hermann.ngayap
"""
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from functions import make_dbc_table


from sql_queries import (query_results_1, query_results_2, query_results_3, 
                         query_results_4, query_results_5, query_results_6, 
                         query_results_7, query_results_8, query_results_9,
                         query_results_10, query_results_11, query_results_12, 
                         query_results_13, query_results_14, query_results_15,
                         query_results_16, query_results_17, query_results_18,
                         query_results_19, query_results_20, query_results_21,
                         query_results_22, query_results_23, query_results_24)
cols = ['Years', 'Merchant', 'HCR']

table_header = [
     html.Thead(html.Tr([html.Th(i) for i in cols]))] 

table_body = [
         html.Tbody(
             [
                 html.Tr([html.Td(query_results_19.iloc[i][col]) for col in query_results_19.columns]) 
                 for i in range(len(query_results_19))
                 ]
             )
         ]

prod_merchant_tbl=html.Div(
    children=[
     dbc.Table(
         table_header + table_body,
         bordered=False,
         responsive=True,
         hover=True,
         striped=True,
         #style=table,
         className="table")
     ]
 )



