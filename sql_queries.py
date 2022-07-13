# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 16:45:57 2022

@author: hermann.ngayap
"""
#Sql queries to pull up data from the sql server DB
import pandas as pd
import pyodbc
import sqlalchemy
from sqlalchemy import create_engine
from server_credentials import server_credentials

def open_database():
    print('Connecting to SQL Server with ODBC driver')
    connection_string = 'DRIVER={SQL Server};SERVER='+server_credentials['server']+';DATABASE='+server_credentials['database']+';UID='+server_credentials['username']+';Trusted_Connection='+server_credentials['yes']
    cnxn = pyodbc.connect(connection_string)
    print('connected!')

    return cnxn

#windows authentication 
def mssql_engine(): 
    engine = create_engine('mssql+pyodbc://BLX186-SQ1PRO01/StarDust?driver=SQL+Server+Native+Client+11.0') 
    return engine
#================================================================
#======================= SQL Queries  ===========================
#================================================================
#======1.Exposition per year
query_1 ="SELECT année \
	,ROUND(ISNULL(SUM(p50), 0) / 1000, 5) + ( \
		SELECT ROUND(ISNULL(SUM(p50), 0) / 1000, 5) \
		FROM p50_p90_hedge AS h \
		WHERE a.année = h.année \
		) AS yearly_exposition \
FROM p50_p90_asset AS a \
GROUP BY année \
ORDER BY année;"
query_results_1 = pd.read_sql(query_1, mssql_engine()) 

#======2.Exposition per quarter per year
query_2 ="SELECT année \
	,trimestre \
	,CASE \
        WHEN LEFT(trimestre, 2) = 'Q1' \
			THEN 'Q1' \
		WHEN LEFT(trimestre, 2) = 'Q2' \
			THEN 'Q2' \
		WHEN LEFT(trimestre, 2) = 'Q3' \
			THEN 'Q3' \
		WHEN LEFT(trimestre, 2) = 'Q4' \
			THEN 'Q4' \
		END AS quarters \
	,(ISNULL(SUM(p50), 0) / 1000) + ( \
		SELECT ISNULL(SUM(p50), 0) / 1000 \
		FROM p50_p90_hedge AS h \
		WHERE a.année = h.année \
			AND a.trimestre = h.trimestre \
		) AS quarterly_exposition \
FROM p50_p90_asset AS a \
GROUP BY année \
	,trimestre \
ORDER BY année \
	,trimestre;"
query_results_2 = pd.read_sql(query_2, mssql_engine())

#======3.Exposition per month per year

query_3="SELECT année \
	,mois \
	,CASE \
        WHEN mois = 1 \
			THEN 'jan' \
		WHEN mois = 2 \
			THEN 'feb' \
		WHEN mois = 3 \
			THEN 'mar' \
		WHEN mois = 4 \
			THEN 'apr' \
		WHEN mois = 5 \
			THEN 'may' \
		WHEN mois = 6 \
			THEN 'jun' \
		WHEN mois = 7 \
			THEN 'jul' \
		WHEN mois = 8 \
			THEN 'aug' \
		WHEN mois = 9 \
			THEN 'sep' \
		WHEN mois = 10 \
			THEN 'oct' \
		WHEN mois = 11 \
			THEN 'nov' \
		WHEN mois = 12 \
			THEN 'dec' \
		END AS months \
	,   ROUND(ISNULL(SUM(p50), 0) / 1000, 5) + ( \
		SELECT ROUND(ISNULL(SUM(p50), 0) / 1000, 5) \
		FROM p50_p90_hedge AS h \
		WHERE a.année = h.année \
			AND a.mois = h.mois \
		) AS monthly_exposition \
FROM p50_p90_asset AS a \
GROUP BY année \
	,mois \
ORDER BY année \
	,mois;"
query_results_3 = pd.read_sql(query_3, mssql_engine())

#=====4. Hedge type per year

query_4 ="SELECT année \
	,   CASE \
        WHEN type_hedge = 'CR16' \
			THEN 'CR' \
		WHEN type_hedge = 'CR17' \
			THEN 'CR' \
		WHEN type_hedge = 'CR' \
			THEN 'CR' \
		WHEN type_hedge = 'OA' \
			THEN 'OA' \
		WHEN type_hedge = 'PPA' \
			THEN 'PPA' \
		END AS type_contract \
	,   ROUND(ISNULL(SUM(- p50), 0) / 1000, 5) AS hedge \
FROM p50_p90_hedge \
GROUP BY année \
	,   CASE \
		WHEN type_hedge = 'CR16' \
			THEN 'CR' \
		WHEN type_hedge = 'CR17' \
			THEN 'CR' \
		WHEN type_hedge = 'CR' \
			THEN 'CR' \
		WHEN type_hedge = 'OA' \
			THEN 'OA' \
		WHEN type_hedge = 'PPA' \
			THEN 'PPA' \
		END \
ORDER BY année \
	,type_contract;"
query_results_4 = pd.read_sql(query_4, mssql_engine())  
  
#=====5. Hedge per quarter per year

query_5 ="SELECT année, trimestre, \
                 CASE WHEN type_hedge = 'CR16' THEN 'CR' \
                      WHEN type_hedge = 'CR17' THEN 'CR' \
                      WHEN type_hedge = 'CR' THEN 'CR' \
                      WHEN type_hedge = 'OA' THEN 'OA' \
                      WHEN type_hedge = 'PPA' THEN 'PPA' \
                 END AS type_contract, \
                 CASE WHEN LEFT(trimestre, 2)='Q1' THEN 'Q1' \
                      WHEN LEFT(trimestre, 2)='Q2' THEN 'Q2' \
                      WHEN LEFT(trimestre, 2)='Q3' THEN 'Q3' \
                      WHEN LEFT(trimestre, 2)='Q4' THEN 'Q4' \
                      END AS quarters, \
                ROUND(ISNULL(SUM(-p50), 0)/1000, 5) AS hedge \
          FROM p50_p90_hedge \
          GROUP BY année, trimestre, \
              CASE WHEN type_hedge='CR16' THEN 'CR' \
                   WHEN type_hedge='CR17' THEN 'CR' \
                   WHEN type_hedge='CR' THEN 'CR' \
                   WHEN type_hedge='OA' THEN 'OA' \
                   WHEN type_hedge='PPA' THEN 'PPA' \
                   END \
          ORDER BY année, quarters;"
query_results_5 = pd.read_sql(query_5, mssql_engine())  

#=====6. Hedge per month per year
query_6 ="SELECT année, mois,\
                 CASE WHEN type_hedge = 'CR16' THEN 'CR' \
                      WHEN type_hedge = 'CR17' THEN 'CR' \
                      WHEN type_hedge = 'CR' THEN 'CR' \
                      WHEN type_hedge = 'OA' THEN 'OA' \
                      WHEN type_hedge = 'PPA' THEN 'PPA' \
                 END AS type_contract, \
                 CASE WHEN mois=1 THEN 'jan'\
                      WHEN mois=2 THEN 'feb' \
                      WHEN mois=3 THEN 'mar' \
                      WHEN mois=4 THEN 'apr' \
                      WHEN mois=5 THEN 'may' \
                      WHEN mois=6 THEN 'jun' \
                      WHEN mois=7 THEN 'jul' \
                      WHEN mois=8 THEN 'aug' \
                      WHEN mois=9 THEN 'sep' \
                      WHEN mois=10 THEN 'oct' \
                      WHEN mois=11 THEN 'nov' \
                      WHEN mois=12 THEN 'dec' \
                 END AS months,\
                ROUND(ISNULL(SUM(-p50), 0)/1000, 5) AS hedge \
          FROM p50_p90_hedge \
          GROUP BY année, mois,\
              CASE WHEN type_hedge='CR16' THEN 'CR' \
                   WHEN type_hedge='CR17' THEN 'CR' \
                   WHEN type_hedge='CR' THEN 'CR' \
                   WHEN type_hedge='OA' THEN 'OA' \
                   WHEN type_hedge='PPA' THEN 'PPA' \
                   END \
          ORDER BY année, mois;"
query_results_6 = pd.read_sql(query_6, mssql_engine()) 

#=====7.HCR per year
query_7 = "SELECT année, CAST(CAST(ROUND((SELECT ISNULL(SUM(-p50), 0) \
                        FROM p50_p90_hedge AS h \
                        WHERE a.année=h.année) / ISNULL(SUM(p50), 0)*100, 2) AS DECIMAL(5, 2)) AS VARCHAR(10)) + '%' AS hcr_per_year \
            FROM p50_p90_asset AS a \
            GROUP BY année \
            ORDER BY année;"
query_results_7 = pd.read_sql(query_7, mssql_engine())
#=====8.HCR per quarter
query_8 = "SELECT année, trimestre, \
                  CASE WHEN LEFT(trimestre, 2) = 'Q1' THEN 'Q1' \
                       WHEN LEFT(trimestre, 2) = 'Q2' THEN 'Q2' \
                       WHEN LEFT(trimestre, 2) = 'Q3' THEN 'Q3' \
                       WHEN LEFT(trimestre, 2) = 'Q4' THEN 'Q4' \
                       END AS quarters,\
                          CAST(CAST(ROUND((SELECT ISNULL(SUM(-p50), 0) \
                            FROM p50_p90_hedge AS h \
                            WHERE a.année=h.année AND  a.trimestre=h.trimestre) / ISNULL(SUM(p50), 0)*100, 2) AS DECIMAL(5, 2)) AS VARCHAR(10)) + '%' AS hcr_per_quarter \
            FROM p50_p90_asset AS a \
            GROUP BY année, trimestre \
            ORDER BY année, trimestre;"
query_results_8= pd.read_sql(query_8, mssql_engine())
#=====9.HCR per month
query_9 = "SELECT année, mois, \
                  CASE WHEN mois=1 THEN 'jan' \
                       WHEN mois=2 THEN 'feb' \
                       WHEN mois=3 THEN 'mar' \
                       WHEN mois=4 THEN 'apr' \
		               WHEN mois=5 THEN 'may' \
		               WHEN mois=6 THEN 'jun' \
		               WHEN mois=7 THEN 'jul' \
		               WHEN mois=8 THEN 'aug' \
		               WHEN mois=9 THEN 'sep' \
		               WHEN mois=10 THEN 'oct' \
		               WHEN mois=11 THEN 'nov' \
		               WHEN mois=12 THEN 'dec' \
		          END AS months, \
                  CAST(CAST(ROUND((SELECT ISNULL(SUM(-p50), 0) \
                  FROM p50_p90_hedge AS h \
                  WHERE a.année=h.année AND  a.mois=h.mois) / ISNULL(SUM(p50), 0)*100, 2) AS DECIMAL(5, 2)) AS VARCHAR(10)) + '%' AS hcr_per_month \
            FROM p50_p90_asset AS a \
            GROUP BY année, mois \
            ORDER BY année, mois;"
query_results_9= pd.read_sql(query_9, mssql_engine())

#=============================
#====    PRODUCTION  =========
#=============================

#=====Prod per year
query_10 = "SELECT année, \
                   ROUND(ISNULL(SUM(p50), 0)/1000, 5) AS prod_per_year \
            FROM p50_p90_asset AS a \
            GROUP BY année \
            ORDER BY année;"
query_results_10 = pd.read_sql(query_10, mssql_engine())

#====Prod per quarter

query_11 = "SELECT année, trimestre, \
                   CASE WHEN LEFT(trimestre, 2)='Q1' THEN 'Q1' \
                   WHEN LEFT(trimestre, 2)='Q2' THEN 'Q2' \
                   WHEN LEFT(trimestre, 2)='Q3' THEN 'Q3' \
                   WHEN LEFT(trimestre, 2)='Q4' THEN 'Q4' \
                   END AS quarters, \
                   ROUND(ISNULL(SUM(p50), 0)/1000, 5) AS prod_per_quarter \
            FROM p50_p90_asset \
            GROUP BY année, trimestre \
            ORDER BY année, trimestre;"
query_results_11 = pd.read_sql(query_11, mssql_engine())            

#=====Prod per month
query_12 = "SELECT année, mois, \
                   CASE WHEN mois=1 THEN 'jan' \
                        WHEN mois=2 THEN 'feb' \
                        WHEN mois=3 THEN 'mar' \
	                    WHEN mois=4 THEN 'apr' \
			            WHEN mois=5 THEN 'may' \
			            WHEN mois=6 THEN 'jun' \
			            WHEN mois=7 THEN 'jul' \
			            WHEN mois=8 THEN 'aug' \
			            WHEN mois=9 THEN 'sep' \
			            WHEN mois=10 THEN 'oct' \
			            WHEN mois=11 THEN 'nov' \
			            WHEN mois=12 THEN 'dec' \
			       END AS months, \
ROUND(ISNULL(SUM(p50), 0)/1000, 5) AS prod_per_month \
FROM p50_p90_asset \
GROUP BY année, mois \
ORDER BY année, mois;"
query_results_12 = pd.read_sql(query_12, mssql_engine())   

#=====Fixed & merchant per year
query_13 = "SELECT année, \
            SUM(CASE WHEN type_hedge='CR16' OR type_hedge='CR17' OR type_hedge='CR' OR type_hedge='OA' THEN -p50/1000 END) AS fixed_price, \
			SUM(CASE WHEN type_hedge='PPA' THEN  -p50/1000 END) AS merchant \
FROM p50_p90_hedge \
GROUP BY année \
ORDER BY année;"
query_results_13 = pd.read_sql(query_13, mssql_engine())

#=====Fixed & merchant per quarter
query_14 = "SELECT année, trimestre, \
			       CASE WHEN LEFT(trimestre, 2)='Q1' THEN 'Q1' \
			            WHEN LEFT(trimestre, 2)='Q2' THEN 'Q2' \
			            WHEN LEFT(trimestre, 2)='Q3' THEN 'Q3' \
			            WHEN LEFT(trimestre, 2)='Q4' THEN 'Q4' \
			END AS quarters, \
			SUM(CASE WHEN type_hedge='CR16' OR type_hedge='CR17' OR type_hedge='CR' OR type_hedge='OA' THEN -p50/1000 END) AS fixed_price, \
			SUM(CASE WHEN type_hedge='PPA' THEN  -p50/1000 END) AS merchant \
FROM p50_p90_hedge \
GROUP BY année, trimestre \
ORDER BY année, trimestre;"
query_results_14 = pd.read_sql(query_14, mssql_engine())

#=====Fixed & merchant per months
query_15 = "SELECT année, mois, \
		           CASE WHEN mois=1 THEN 'jan' \
			            WHEN mois=2 THEN 'feb' \
			            WHEN mois=3 THEN 'mar' \
	                    WHEN mois=4 THEN 'apr' \
			            WHEN mois=5 THEN 'may' \
			            WHEN mois=6 THEN 'jun' \
			            WHEN mois=7 THEN 'jul' \
			            WHEN mois=8 THEN 'aug' \
			            WHEN mois=9 THEN 'sep' \
			            WHEN mois=10 THEN 'oct' \
			            WHEN mois=11 THEN 'nov' \
			            WHEN mois=12 THEN 'dec' \
		            END AS months, \
			        SUM(CASE WHEN type_hedge='CR16' OR type_hedge='CR17' OR type_hedge='CR' OR type_hedge='OA' THEN -p50/1000 END) AS fixed_price, \
			        SUM(CASE WHEN type_hedge='PPA' THEN  -p50/1000 END) AS merchant \
FROM p50_p90_hedge \
GROUP BY année, mois \
ORDER BY année, mois;"
query_results_15 = pd.read_sql(query_15, mssql_engine())

#=====Hedge PPA/year
query_16 = "SELECT année \
	,SUM(- p50) / 1000 AS ppa_year \
FROM p50_p90_hedge \
WHERE type_hedge = 'PPA' \
GROUP BY année \
ORDER BY année;"                
query_results_16 = pd.read_sql(query_16, mssql_engine())

#=====hedge PPA/quarter
query_17 = "SELECT année \
	,trimestre \
	,CASE \
        WHEN LEFT(trimestre, 2) = 'Q1' \
			THEN 'Q1' \
		WHEN LEFT(trimestre, 2) = 'Q2' \
			THEN 'Q2' \
		WHEN LEFT(trimestre, 2) = 'Q3' \
			THEN 'Q3' \
		WHEN LEFT(trimestre, 2) = 'Q4' \
			THEN 'Q4' \
		END AS quarters \
	,SUM(- p50) / 1000 AS ppa_qtr \
FROM p50_p90_hedge \
WHERE type_hedge = 'PPA' \
GROUP BY année \
	,trimestre \
ORDER BY année \
	,trimestre;"
query_results_17 = pd.read_sql(query_17, mssql_engine())

#====hedge PPA/month
query_18= "SELECT année \
	,mois \
	,CASE \
        WHEN mois = 1 \
			THEN 'jan' \
		WHEN mois = 2 \
			THEN 'feb' \
		WHEN mois = 3 \
			THEN 'mar' \
		WHEN mois = 4 \
			THEN 'apr' \
		WHEN mois = 5 \
			THEN 'may' \
		WHEN mois = 6 \
			THEN 'jun' \
		WHEN mois = 7 \
			THEN 'jul' \
		WHEN mois = 8 \
			THEN 'aug' \
		WHEN mois = 9 \
			THEN 'sep' \
		WHEN mois = 10 \
			THEN 'oct' \
		WHEN mois = 11 \
			THEN 'nov' \
		WHEN mois = 12 \
			THEN 'dec' \
		END AS months \
	,SUM(- p50) / 1000 AS ppa_mth \
FROM p50_p90_hedge \
WHERE type_hedge = 'PPA' \
GROUP BY année \
	,mois \
ORDER BY année \
	,mois;"
query_results_18 = pd.read_sql(query_18, mssql_engine())
#=====Prod Merchant/year
query_19= "SELECT année \
	,( \
		ISNULL(SUM(p50), 0) + ( \
			SELECT ISNULL(SUM(p50), 0) \
			FROM p50_p90_hedge AS h \
			WHERE type_hedge IN ( \
					'OA' \
					,'CR' \
					,'CR16' \
					,'CR17' \
					) \
				AND a.année = h.année \
			) \
		) / 1000 AS prod_merchant_year \
FROM p50_p90_asset AS a \
GROUP BY année \
ORDER BY année;"
query_results_19 = pd.read_sql(query_19, mssql_engine())

#=====Prod Merchant/quarter
query_20="SELECT année \
	,trimestre \
	,CASE \
        WHEN LEFT(trimestre, 2) = 'Q1' \
			THEN 'Q1' \
		WHEN LEFT(trimestre, 2) = 'Q2' \
			THEN 'Q2' \
		WHEN LEFT(trimestre, 2) = 'Q3' \
			THEN 'Q3' \
		WHEN LEFT(trimestre, 2) = 'Q4' \
			THEN 'Q4' \
		END AS quarters \
	,( \
		    ISNULL(SUM(p50), 0) + ( \
			SELECT ISNULL(SUM(p50), 0)\
			FROM p50_p90_hedge AS h \
			WHERE type_hedge IN ( \
					'OA' \
					,'CR' \
					,'CR16' \
					,'CR17' \
					) \
				AND a.année = h.année \
				AND a.trimestre = h.trimestre \
			) \
		) / 1000 AS prod_merchant_qtr \
FROM p50_p90_asset AS a \
GROUP BY année \
	,trimestre \
ORDER BY année \
	,trimestre;"
query_results_20 = pd.read_sql(query_20, mssql_engine()) 
#=====Prod Merchant/month
query_21="SELECT année, mois \
	   ,CASE \
           WHEN mois = 1 \
				THEN 'jan' \
			WHEN mois = 2 \
				THEN 'feb' \
			WHEN mois = 3 \
				THEN 'mar' \
			WHEN mois = 4 \
				THEN 'apr' \
			WHEN mois = 5 \
				THEN 'may' \
			WHEN mois = 6 \
				THEN 'jun' \
			WHEN mois = 7 \
				THEN 'jul' \
			WHEN mois = 8 \
				THEN 'aug' \
			WHEN mois = 9 \
				THEN 'sep' \
			WHEN mois = 10 \
				THEN 'oct' \
			WHEN mois = 11 \
				THEN 'nov' \
			WHEN mois = 12 \
				THEN 'dec' \
			END AS months \
	,( \
		ISNULL(SUM(p50), 0) + ( \
			SELECT ISNULL(SUM(p50), 0) \
			FROM p50_p90_hedge AS h \
			WHERE type_hedge IN ( \
					'OA' \
					,'CR' \
					,'CR16' \
					,'CR17' \
					) \
				AND a.année = h.année AND a.mois = h.mois \
			) \
		) / 1000 AS prod_merchant_mth \
FROM p50_p90_asset AS a \
GROUP BY année, mois \
ORDER BY année, mois;"
query_results_21 = pd.read_sql(query_21, mssql_engine())

#=====Prod Merchant hedged with PPA Coverage Ratio per year
query_22 = "SELECT ppa.année \
	,CAST(CAST(ROUND((ppa.ppa_year / prod_merchant.prod_merchant_year) * 100, 2) AS DECIMAL(5, 2)) AS VARCHAR(10)) + '%' AS coverage_ratio \
FROM ( \
	SELECT année \
		,SUM(- p50) / 1000 AS ppa_year \
	FROM p50_p90_hedge \
	WHERE type_hedge = 'PPA' \
	GROUP BY année \
	) AS ppa \
INNER JOIN ( \
	SELECT année \
		,( \
			ISNULL(SUM(p50), 0) + ( \
				SELECT ISNULL(SUM(p50), 0) \
				FROM p50_p90_hedge AS h \
				WHERE type_hedge IN ( \
						'OA' \
						,'CR' \
						,'CR16' \
						,'CR17' \
						) \
					AND a.année = h.année \
				) \
			) / 1000 AS prod_merchant_year \
	FROM p50_p90_asset AS a \
	GROUP BY année \
	) AS prod_merchant ON ppa.année = prod_merchant.année \
ORDER BY année;"
query_results_22 = pd.read_sql(query_22, mssql_engine())
#=====Prod Merchant hedged with PPA Coverage Ratio per quarter
query_23 = "SELECT ppa.année \
	,ppa.trimestre \
	,ppa.quarters \
	,CAST(CAST(ROUND((ppa.ppa_qtr / prod_merchant.prod_merchant_qtr) * 100, 2) AS DECIMAL(5, 2)) AS VARCHAR(10)) + '%' AS coverage_ratio \
FROM ( \
	SELECT année \
		,trimestre \
		,CASE \
            WHEN LEFT(trimestre, 2) = 'Q1' \
				THEN 'Q1' \
			WHEN LEFT(trimestre, 2) = 'Q2' \
				THEN 'Q2' \
			WHEN LEFT(trimestre, 2) = 'Q3' \
				THEN 'Q3' \
			WHEN LEFT(trimestre, 2) = 'Q4' \
				THEN 'Q4' \
			END AS quarters \
		,SUM(- p50) / 1000 AS ppa_qtr \
	FROM p50_p90_hedge \
	WHERE type_hedge = 'PPA' \
	GROUP BY année \
		,trimestre \
	) AS ppa \
INNER JOIN ( \
	SELECT année \
		,trimestre \
		,CASE \
            WHEN LEFT(trimestre, 2) = 'Q1' \
				THEN 'Q1' \
			WHEN LEFT(trimestre, 2) = 'Q2' \
				THEN 'Q2' \
			WHEN LEFT(trimestre, 2) = 'Q3' \
				THEN 'Q3' \
			WHEN LEFT(trimestre, 2) = 'Q4' \
				THEN 'Q4' \
			END AS quarters \
		,( \
			ISNULL(SUM(p50), 0) + ( \
				SELECT ISNULL(SUM(p50), 0) \
				FROM p50_p90_hedge AS h \
				WHERE type_hedge IN ( \
						'OA' \
						,'CR' \
						,'CR16' \
						,'CR17' \
						) \
					AND a.année = h.année \
					AND a.trimestre = h.trimestre \
				) \
			) / 1000 AS prod_merchant_qtr \
	FROM p50_p90_asset AS a \
	GROUP BY année \
		,trimestre \
	) AS prod_merchant ON ppa.année = prod_merchant.année \
	AND ppa.trimestre = prod_merchant.trimestre \
ORDER BY année \
	,trimestre;"
query_results_23 = pd.read_sql(query_23, mssql_engine())

#=====Prod Merchant hedged with PPA Coverage Ratio per month
query_24 = "SELECT ppa.année \
	,ppa.mois \
	,ppa.months \
	,CAST(CAST(ROUND((ppa.ppa_mth / prod_merchant.prod_merchant_mth) * 100, 2) AS DECIMAL(5, 2)) AS VARCHAR(10)) + '%' AS coverage_ratio \
FROM ( \
	SELECT année \
		,mois \
		,CASE \
            WHEN mois = 1 \
				THEN 'jan' \
			WHEN mois = 2 \
				THEN 'feb' \
			WHEN mois = 3 \
				THEN 'mar' \
			WHEN mois = 4 \
				THEN 'apr' \
			WHEN mois = 5 \
				THEN 'may' \
			WHEN mois = 6 \
				THEN 'jun' \
			WHEN mois = 7 \
				THEN 'jul' \
			WHEN mois = 8 \
				THEN 'aug' \
			WHEN mois = 9 \
				THEN 'sep' \
			WHEN mois = 10 \
				THEN 'oct' \
			WHEN mois = 11 \
				THEN 'nov' \
			WHEN mois = 12 \
				THEN 'dec' \
			END AS months \
		,SUM(- p50) / 1000 AS ppa_mth \
	FROM p50_p90_hedge \
	WHERE type_hedge = 'PPA' \
	GROUP BY année \
		,mois \
	) AS ppa \
INNER JOIN ( \
	SELECT année \
		,mois \
		,CASE \
            WHEN mois = 1 \
				THEN 'jan' \
			WHEN mois = 2 \
				THEN 'feb' \
			WHEN mois = 3 \
				THEN 'mar' \
			WHEN mois = 4 \
				THEN 'apr' \
			WHEN mois = 5 \
				THEN 'may' \
			WHEN mois = 6 \
				THEN 'jun' \
			WHEN mois = 7 \
				THEN 'jul' \
			WHEN mois = 8 \
				THEN 'aug' \
			WHEN mois = 9 \
				THEN 'sep' \
			WHEN mois = 10 \
				THEN 'oct' \
			WHEN mois = 11 \
				THEN 'nov' \
			WHEN mois = 12 \
				THEN 'dec' \
			END AS months \
		,( \
			ISNULL(SUM(p50), 0) + ( \
				SELECT ISNULL(SUM(p50), 0) \
				FROM p50_p90_hedge AS h \
				WHERE type_hedge IN ( \
						'OA' \
						,'CR' \
						,'CR16' \
						,'CR17' \
						) \
					AND a.année = h.année \
					AND a.mois = h.mois \
				) \
			) / 1000 AS prod_merchant_mth \
	FROM p50_p90_asset AS a \
	GROUP BY année \
		,mois \
	) AS prod_merchant ON ppa.année = prod_merchant.année \
	AND ppa.mois = prod_merchant.mois \
ORDER BY année \
	,mois;"
query_results_24 = pd.read_sql(query_24, mssql_engine())           

#/*
#=====================================================Prod Solar and Eol
#*/
#-----------------------------------------------------Solar/year
query_25 ="SELECT année \
	,CAST(ROUND((ISNULL(SUM(p50), 0) / 1000), 3) AS DECIMAL(10, 3)) AS prod_solar \
FROM p50_p90_asset \
WHERE projet_id IN ( \
		SELECT DISTINCT (projet_id) \
		FROM asset \
		WHERE technologie = 'solaire' \
		) \
GROUP BY année \
ORDER BY année;"
query_results_25 = pd.read_sql(query_25, mssql_engine()) 
#------------------------------------------------------wind power/year
query_26="SELECT année \
	,CAST(ROUND((ISNULL(SUM(p50), 0) / 1000), 3) AS DECIMAL(10, 3)) AS prod_eol \
FROM p50_p90_asset \
WHERE projet_id IN ( \
		SELECT DISTINCT (projet_id) \
		FROM asset \
		WHERE technologie = 'éolien' \
		) \
GROUP BY année \
ORDER BY année;"
query_results_26 = pd.read_sql(query_26, mssql_engine()) 

#-----------------------------------------------------solar/quarter
query_27="SELECT année \
	,trimestre \
	,CASE \
        WHEN LEFT(trimestre, 2) = 'Q1' \
			THEN 'Q1' \
		WHEN LEFT(trimestre, 2) = 'Q2' \
			THEN 'Q2' \
		WHEN LEFT(trimestre, 2) = 'Q3' \
			THEN 'Q3' \
        WHEN LEFT(trimestre, 2) = 'Q4' \
            THEN 'Q4' \
		END AS quarters \
	,CAST(ROUND((ISNULL(SUM(p50), 0) / 1000), 3) AS DECIMAL(10, 3)) AS prod_solar_qtr \
FROM p50_p90_asset \
WHERE projet_id IN ( \
		SELECT DISTINCT (projet_id) \
		FROM asset \
		WHERE technologie = 'solaire' \
		) \
GROUP BY année \
	,trimestre \
ORDER BY année \
	,trimestre;"
query_results_27 = pd.read_sql(query_27, mssql_engine()) 

#-----------------------------------------------------wind power/quarter
query_28="SELECT année \
	,trimestre \
	,CASE \
        WHEN LEFT(trimestre, 2) = 'Q1' \
			THEN 'Q1' \
		WHEN LEFT(trimestre, 2) = 'Q2' \
			THEN 'Q2' \
		WHEN LEFT(trimestre, 2) = 'Q3' \
			THEN 'Q3' \
		WHEN LEFT(trimestre, 2) = 'Q4' \
			THEN 'Q4' \
		END AS quarters \
	,CAST(ROUND((ISNULL(SUM(p50), 0) / 1000), 3) AS DECIMAL(10, 3)) AS prod_eol_qtr \
FROM p50_p90_asset \
WHERE projet_id IN ( \
		SELECT DISTINCT (projet_id) \
		FROM asset \
		WHERE technologie = 'éolien' \
		) \
GROUP BY année \
	,trimestre \
ORDER BY année \
	,trimestre;"
query_results_28 = pd.read_sql(query_28, mssql_engine()) 

#------------------------------------------------------solar/month
query_29="SELECT année \
    ,mois \
	,CASE \
        WHEN mois = 1 \
			THEN 'jan' \
		WHEN mois = 2 \
			THEN 'feb' \
		WHEN mois = 3 \
			THEN 'mar' \
		WHEN mois = 4 \
			THEN 'apr' \
		WHEN mois = 5 \
			THEN 'may' \
		WHEN mois = 6 \
			THEN 'jun' \
		WHEN mois = 7 \
			THEN 'jul' \
		WHEN mois = 8 \
			THEN 'aug' \
		WHEN mois = 9 \
			THEN 'sep' \
		WHEN mois = 10 \
			THEN 'oct' \
		WHEN mois = 11 \
			THEN 'nov' \
		WHEN mois = 12 \
			THEN 'dec' \
		END AS months \
	,CAST(ROUND((ISNULL(SUM(p50), 0) / 1000), 3) AS DECIMAL(10, 3)) AS prod_solar_mth \
FROM p50_p90_asset \
WHERE projet_id IN ( \
		SELECT DISTINCT (projet_id) \
		FROM asset \
		WHERE technologie = 'solaire' \
		) \
GROUP BY année, mois \
ORDER BY année, mois;"
query_results_29 = pd.read_sql(query_29, mssql_engine())

#------------------------------------------------------wind/month
query_30="SELECT année \
	,mois \
	,CASE \
        WHEN mois = 1 \
            THEN 'jan' \
		WHEN mois = 2 \
			THEN 'feb' \
		WHEN mois = 3 \
			THEN 'mar' \
		WHEN mois = 4 \
			THEN 'apr' \
		WHEN mois = 5 \
			THEN 'may' \
		WHEN mois = 6 \
			THEN 'jun' \
		WHEN mois = 7 \
			THEN 'jul' \
		WHEN mois = 8 \
			THEN 'aug' \
		WHEN mois = 9 \
			THEN 'sep' \
		WHEN mois = 10 \
			THEN 'oct' \
		WHEN mois = 11 \
			THEN 'nov' \
		WHEN mois = 12 \
			THEN 'dec' \
		END AS months \
	,CAST(ROUND((ISNULL(SUM(p50), 0) / 1000), 3) AS DECIMAL(10, 3)) AS prod_eol_mth \
FROM p50_p90_asset \
WHERE projet_id IN ( \
		SELECT DISTINCT (projet_id) \
		FROM asset \
		WHERE technologie = 'éolien' \
		) \
GROUP BY année \
	,mois \
ORDER BY année \
	,mois;"
query_results_30 = pd.read_sql(query_30, mssql_engine())

#/*
#=================================================================================================
#=============================================Exposure Solar and Eol==============================
#=================================================================================================
#*/
#---------------------------------------------exposure solar/year
query_31="SELECT asset.année \
	,asset.prod_asset + hedge.hedges AS exposure_sol_year \
FROM ( \
	SELECT année \
		,CAST(ROUND((ISNULL(SUM(p50), 0) / 1000), 2) AS DECIMAL(10, 1)) AS prod_asset \
	FROM p50_p90_asset \
	WHERE projet_id IN ( \
			SELECT DISTINCT (projet_id) \
			FROM asset \
			WHERE technologie = 'solaire' \
			) \
	GROUP BY année \
	) AS asset \
INNER JOIN ( \
	SELECT année \
		,CAST(ROUND((ISNULL(SUM(p50), 0) / 1000), 2) AS DECIMAL(10, 1)) AS hedges \
	FROM p50_p90_hedge \
	WHERE projet_id IN ( \
			SELECT DISTINCT (projet_id) \
			FROM asset \
			WHERE technologie = 'solaire' \
			) \
	GROUP BY année \
	) AS hedge ON asset.année = hedge.année \
ORDER BY année;"
query_results_31 = pd.read_sql(query_31, mssql_engine())

#----------------------------------------------exposure eol/year
query_32="SELECT asset.année \
	,asset.prod_asset + hedge.hedges AS exposure_eol_year \
FROM ( \
	SELECT année \
		,CAST(ROUND((ISNULL(SUM(p50), 0) / 1000), 3) AS DECIMAL(10, 3)) AS prod_asset \
	FROM p50_p90_asset \
	WHERE projet_id IN ( \
			SELECT DISTINCT (projet_id) \
			FROM asset \
			WHERE technologie = 'éolien' \
			) \
	GROUP BY année \
	) AS asset \
INNER JOIN ( \
	SELECT année \
		,CAST(ROUND((ISNULL(SUM(p50), 0) / 1000), 3) AS DECIMAL(10, 3)) AS hedges \
	FROM p50_p90_hedge \
	WHERE projet_id IN ( \
			SELECT DISTINCT (projet_id) \
			FROM asset \
			WHERE technologie = 'éolien' \
			) \
	GROUP BY année \
	) AS hedge ON asset.année = hedge.année \
ORDER BY année;"
query_results_32 = pd.read_sql(query_32, mssql_engine())

#-----------------------------------exposure solar/quarter
query_33="SELECT asset.année \
	,asset.trimestre \
	,asset.quarters \
	,asset.prod_asset + hedge.hedges AS exposure_sol_qtr \
FROM ( \
	SELECT année \
		,trimestre \
		,CASE \
            WHEN LEFT(trimestre, 2) = 'Q1' \
				THEN 'Q1' \
			WHEN LEFT(trimestre, 2) = 'Q2' \
				THEN 'Q2' \
			WHEN LEFT(trimestre, 2) = 'Q3' \
				THEN 'Q3' \
			WHEN LEFT(trimestre, 2) = 'Q4' \
				THEN 'Q4' \
			END AS quarters \
		,CAST(ROUND((ISNULL(SUM(p50), 0) / 1000), 2) AS DECIMAL(10, 1)) AS prod_asset \
	FROM p50_p90_asset \
	WHERE projet_id IN ( \
			SELECT DISTINCT (projet_id) \
			FROM asset \
			WHERE technologie = 'solaire' \
			) \
	GROUP BY année \
		,trimestre \
	) AS asset \
INNER JOIN ( \
	SELECT année \
		,trimestre \
		,CASE \
            WHEN LEFT(trimestre, 2) = 'Q1' \
				THEN 'Q1' \
			WHEN LEFT(trimestre, 2) = 'Q2' \
				THEN 'Q2' \
			WHEN LEFT(trimestre, 2) = 'Q3' \
				THEN 'Q3' \
			WHEN LEFT(trimestre, 2) = 'Q4' \
				THEN 'Q4' \
			END AS quarters \
		,CAST(ROUND((ISNULL(SUM(p50), 0) / 1000), 2) AS DECIMAL(10, 1)) AS hedges \
	FROM p50_p90_hedge \
	WHERE projet_id IN ( \
			SELECT DISTINCT (projet_id) \
			FROM asset \
			WHERE technologie = 'solaire' \
			) \
	GROUP BY année \
		,trimestre \
	) AS hedge ON asset.année = hedge.année \
	AND asset.trimestre = hedge.trimestre \
ORDER BY année \
	,trimestre;"
query_results_33 = pd.read_sql(query_33, mssql_engine())

#-----------------------------------exposure éolien/quarter
query_34 ="SELECT asset.année \
	,asset.trimestre \
	,asset.quarters \
	,asset.prod_asset + hedge.hedges AS exposure_eol_qtr \
FROM ( \
	SELECT année \
		,trimestre \
		,CASE \
            WHEN LEFT(trimestre, 2) = 'Q1' \
				THEN 'Q1' \
			WHEN LEFT(trimestre, 2) = 'Q2' \
				THEN 'Q2' \
			WHEN LEFT(trimestre, 2) = 'Q3' \
				THEN 'Q3' \
			WHEN LEFT(trimestre, 2) = 'Q4' \
				THEN 'Q4' \
			END AS quarters \
		,CAST(ROUND((ISNULL(SUM(p50), 0) / 1000), 2) AS DECIMAL(10, 1)) AS prod_asset \
	FROM p50_p90_asset \
	WHERE projet_id IN ( \
			SELECT DISTINCT (projet_id) \
			FROM asset \
			WHERE technologie = 'éolien' \
			) \
	GROUP BY année \
		,trimestre \
	) AS asset \
INNER JOIN ( \
	SELECT année \
		,trimestre \
		,CASE \
            WHEN LEFT(trimestre, 2) = 'Q1' \
				THEN 'Q1' \
			WHEN LEFT(trimestre, 2) = 'Q2' \
				THEN 'Q2' \
			WHEN LEFT(trimestre, 2) = 'Q3' \
				THEN 'Q3' \
			WHEN LEFT(trimestre, 2) = 'Q4' \
				THEN 'Q4' \
			END AS quarters \
		,CAST(ROUND((ISNULL(SUM(p50), 0) / 1000), 2) AS DECIMAL(10, 1)) AS hedges \
	FROM p50_p90_hedge \
	WHERE projet_id IN ( \
			SELECT DISTINCT (projet_id) \
			FROM asset \
			WHERE technologie = 'éolien' \
			) \
	GROUP BY année \
		,trimestre \
	) AS hedge ON asset.année = hedge.année \
	AND asset.trimestre = hedge.trimestre \
ORDER BY année \
	,trimestre;"
query_results_34 = pd.read_sql(query_34, mssql_engine())

#-----------------------------------exposure solar/month

query_35 ="SELECT asset.année, asset.mois, asset.months, asset.prod_asset + hedge.hedges AS exposure_sol_mth \
FROM( \
	SELECT année, mois, \
		CASE \
            WHEN mois = 1 \
				THEN 'jan' \
			WHEN mois = 2 \
				THEN 'feb' \
			WHEN mois = 3 \
				THEN 'mar' \
			WHEN mois = 4 \
				THEN 'apr' \
			WHEN mois = 5 \
				THEN 'may' \
			WHEN mois = 6 \
				THEN 'jun' \
			WHEN mois = 7 \
				THEN 'jul' \
			WHEN mois = 8 \
				THEN 'aug' \
			WHEN mois = 9 \
				THEN 'sep' \
			WHEN mois = 10 \
				THEN 'oct' \
			WHEN mois = 11 \
				THEN 'nov' \
			WHEN mois = 12 \
				THEN 'dec' \
			END AS months \
	,CAST(ROUND((ISNULL(SUM(p50), 0)/1000), 2) AS DECIMAL(10, 1)) AS prod_asset \
        FROM p50_p90_asset \
	WHERE projet_id IN ( \
		SELECT DISTINCT (projet_id) \
		FROM asset \
		WHERE technologie = 'solaire' \
		) \
	GROUP BY année, mois \
) AS asset \
INNER JOIN \
( \
	SELECT année, mois, \
		CASE \
            WHEN mois = 1 \
				THEN 'jan' \
			WHEN mois = 2 \
				THEN 'feb' \
			WHEN mois = 3 \
				THEN 'mar' \
			WHEN mois = 4 \
				THEN 'apr' \
			WHEN mois = 5 \
				THEN 'may' \
			WHEN mois = 6 \
				THEN 'jun' \
			WHEN mois = 7 \
				THEN 'jul' \
			WHEN mois = 8 \
				THEN 'aug' \
			WHEN mois = 9 \
				THEN 'sep' \
			WHEN mois = 10 \
				THEN 'oct' \
			WHEN mois = 11 \
				THEN 'nov' \
			WHEN mois = 12 \
				THEN 'dec' \
			END AS months \
	,CAST(ROUND((ISNULL(SUM(p50), 0)/1000), 2) AS DECIMAL(10, 1)) AS hedges \
    FROM p50_p90_hedge \
	WHERE projet_id IN ( \
		SELECT DISTINCT (projet_id) \
		FROM asset \
		WHERE technologie = 'solaire' \
		) \
	GROUP BY année, mois \
) AS hedge ON asset.année = hedge.année AND asset.mois = hedge.mois \
ORDER BY année, mois;"
query_results_35 = pd.read_sql(query_35, mssql_engine())

#-----------------------------------exposure éolien/month
query_36 ="SELECT asset.année, asset.mois, asset.months, asset.prod_asset + hedge.hedges AS exposure_eol_mth \
FROM( \
	SELECT année, mois, \
		CASE \
            WHEN mois = 1 \
				THEN 'jan' \
			WHEN mois = 2 \
				THEN 'feb' \
			WHEN mois = 3 \
				THEN 'mar' \
			WHEN mois = 4 \
				THEN 'apr' \
			WHEN mois = 5 \
				THEN 'may' \
			WHEN mois = 6 \
				THEN 'jun' \
			WHEN mois = 7 \
				THEN 'jul' \
			WHEN mois = 8 \
				THEN 'aug' \
			WHEN mois = 9 \
				THEN 'sep' \
			WHEN mois = 10 \
				THEN 'oct' \
			WHEN mois = 11 \
				THEN 'nov' \
			WHEN mois = 12 \
				THEN 'dec' \
			END AS months \
	,CAST(ROUND((ISNULL(SUM(p50), 0)/1000), 2) AS DECIMAL(10, 1)) AS prod_asset \
    FROM p50_p90_asset \
	WHERE projet_id IN ( \
		SELECT DISTINCT (projet_id) \
		FROM asset \
		WHERE technologie = 'éolien' \
		) \
	GROUP BY année, mois \
) AS asset \
INNER JOIN \
( \
	SELECT année, mois, \
		CASE \
            WHEN mois = 1 \
				THEN 'jan' \
			WHEN mois = 2 \
				THEN 'feb' \
			WHEN mois = 3 \
				THEN 'mar' \
			WHEN mois = 4 \
				THEN 'apr' \
			WHEN mois = 5 \
				THEN 'may' \
			WHEN mois = 6 \
				THEN 'jun' \
			WHEN mois = 7 \
				THEN 'jul' \
			WHEN mois = 8 \
				THEN 'aug' \
			WHEN mois = 9 \
				THEN 'sep' \
			WHEN mois = 10 \
				THEN 'oct' \
			WHEN mois = 11 \
				THEN 'nov' \
			WHEN mois = 12 \
				THEN 'dec' \
			END AS months \
	,CAST(ROUND((ISNULL(SUM(p50), 0)/1000), 2) AS DECIMAL(10, 1)) AS hedges \
    FROM p50_p90_hedge \
	WHERE projet_id IN ( \
		SELECT DISTINCT (projet_id) \
		FROM asset \
		WHERE technologie = 'éolien' \
		) \
	GROUP BY année, mois \
) AS hedge ON asset.année = hedge.année AND asset.mois = hedge.mois \
ORDER BY année, mois;"
query_results_36 = pd.read_sql(query_36, mssql_engine())