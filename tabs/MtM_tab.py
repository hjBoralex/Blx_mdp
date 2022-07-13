# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 13:04:12 2022

@author: hermann.ngayap
"""

from dash import dcc, html

MtM_layout=html.Div(
      children=[
             html.Div(
             className="central-panel1-title",
              children=["MtM"],
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
                                 ],
                             ),
                         ],
                     ),
                 ],
             ),],
      )


# =============================================================================
# MtM_layout= html.Div(
#     children=[
#         html.Div(
#             html.Div(
#             className="central-panel1-title",
#             children=["Mark to Market/year"],
#             ),
#             className="central-panel1",
#             children=[
#                 html.Div(
#                     children=[
#                         html.Div(
#                             style={
#                                 "display": "inline-block",
#                                 "vertical-align": "top",
#                                 "width": "50%",
#                             },
#                             children=[
#                                 ],
#                         ),
#                         html.Div(
#                             style={
#                                 "display": "inline-block",
#                                 "margin-top": "0px",
#                                 "margin-left": "25px",
#                                 "width": "25%",
#                             },
#                             children=[
#                                 html.Div(
#                                     children=[
#                                         ],
#                                     className="table",
#                                 )
#                             ],
#                         ),
#                     ]
#                 ),
# 
#             ],
#         ),
#     ],
# )
# =============================================================================

