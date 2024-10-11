# Definir as rotas do site
from flask import Blueprint, render_template
from app.models import consulta_valor_periodo
import plotly.graph_objs as go
import plotly.io as pio


main_bp = Blueprint('main', __name__)

vlr_est, df_critico = consulta_valor_periodo()

@main_bp.route('/')
def index():    
    # Dados do gráfico
    data = [
        go.Bar(
            x=vlr_est["PERIODO"],  # Nomes dos produtos
            y=vlr_est["VALOR"],     # Vendas de cada produto
            text=vlr_est["VrEst"],  # Rótulos (valores) sobre as barras
            textposition='auto',    # Coloca os rótulos automaticamente em uma posição legível  
            textfont=dict(color='white')  # Cor do texto em branco      
        )
    ]
    # Layout do gráfico
    layout = go.Layout(
        title="Total Estoque",
        title_x=0.5,  # Centraliza o título
        title_font=dict(color='white'),
        yaxis=dict(
            showticklabels=False, 
            showgrid=False
        ), 
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color='white'),
        ), 
        xaxis_title='', 
        yaxis_title='', 
        showlegend=False, 
        plot_bgcolor='rgba(0, 0, 0, 0)', 
        paper_bgcolor='rgba(0, 0, 0, 0)',
        legend=dict(
            font=dict(color='white')  # Cor da legenda em branco
        )       
    )
    # Cria o gráfico e converte para JSON
    fig = go.Figure(data=data, layout=layout)
    gr_estJSON = pio.to_json(fig)
    
    # Gráfico de pizza
    pie_data = [
        go.Pie(
            labels=df_critico["CRITICO"],  # Rótulos das fatias
            values=df_critico["TOTAL"],    # Valores para cada fatia
            text=df_critico["TOTAL_STR"],  # Exibe os valores formatados (TOTAL_STR)
            textinfo='text',               # Exibe apenas o texto personalizado
            textposition='inside',          # Texto dentro das fatias
            textfont=dict(color='white')  # Cor do texto em branco
            
        )
    ]

    # Layout do gráfico de pizza
    pie_layout = go.Layout(
        title='Material Crítico',
        title_x=0.5,  # Centraliza o título
        title_font=dict(color='white'),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Fundo transparente
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Fundo transparente
        legend=dict(
            font=dict(color='white')  # Cor da legenda em branco
        )
    )

    # Cria o gráfico de pizza e converte para JSON
    pie_fig = go.Figure(data=pie_data, layout=pie_layout)
    gr_critJSON = pio.to_json(pie_fig)
    
    
    
    return render_template('index.html', gr_estJSON=gr_estJSON, gr_critJSON=gr_critJSON)


@main_bp.route('/cadastrar')
def cadastrar(): 
    return render_template("form.html")