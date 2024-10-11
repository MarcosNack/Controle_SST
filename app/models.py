import sqlite3
import pandas as pd

def convert_mes(value):
    meses = {'Jan': '01','Fev': '02','Mar': '03','Abr': '04','Mai': '05','Jun': '06','Jul': '07','Ago': '08','Set': '09','Out': '10','Nov': '11','Dez': '12'}
    month, year = value.split("-")
    return f"{year}-{meses[month.capitalize()]}"

def consulta_valor_periodo():
    with sqlite3.connect(r"db/database.db") as conn:
        query = """
            SELECT PERIODO, SUM(VALOR) AS VALOR 
            FROM MATERIAIS 
            GROUP BY PERIODO
            """
        df = pd.read_sql(query, conn)
        query = """
        SELECT CRITICO, COUNT(CRITICO) AS TOTAL 
        FROM MATERIAIS 
        GROUP BY CRITICO
        """
        df_critico = pd.read_sql(query, conn)
        
    df_critico["TOTAL_STR"] = df_critico["TOTAL"].apply(lambda x : "{:,.0f}".format(x).replace(",", "X").replace(".", ",").replace("X", "."))
    
    df["VrEst"] = df["VALOR"].apply(lambda x : "{:,.2f}".format(x).replace(",", "X").replace(".", ",").replace("X", "."))
    df["PERIODO"] = df["PERIODO"].apply(lambda x : f"{x.split("/")[0].capitalize()}-{x.split("/")[1]}")
    df["MesStr"] = df["PERIODO"].apply(convert_mes)
    
    df.sort_values(by="MesStr", inplace=True)
    
    return df, df_critico