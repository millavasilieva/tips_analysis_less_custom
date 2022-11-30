import streamlit as st
import pandas as pd 

import numpy as np 

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

@st.cache
def get_data(path):
    tips = pd.read_csv(path)
    return tips

tips = get_data('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv')

st.title("""
Визуализация данных по TIPS

Анализ корелляции полученнных чаевых в сравнении с общим счетом и полом людей
""")

st.header("Таблица данных по чаевым")

fig = go.Figure(data=go.Table(
    header=dict(values=list(tips[['total_bill', 'tip', 'sex', 'smoker', 'day', 'time','size']].columns), 
        align='center'),
    cells=dict(values=[ tips.total_bill,tips.tip, tips.sex, tips.smoker, tips.day, tips.time,tips['size']],
        align = 'left')))
fig.update_layout(margin=dict(l=5,r=5,b=10,t=10),font=dict(color="#000000"))

st.write(fig)

option = st.selectbox ('Выберите тип анализа',('По общему счету','По размеру группы посетителей', 
    "По дню недели и времени", 'По полу человека'))


if option == 'По общему счету':

    st.header('Гистограмма по общему счету')
    st.write('Значение общего счета и его распределение')

    fig1=px.histogram(tips,x='total_bill')
    fig1.update_traces(marker_color='slateblue', 
                        selector=dict(type='histogram'))

    fig1.update_layout(margin=dict(l=5,r=5,b=10,t=10))
    st.write(fig1)



    st.header('Корреляция между общим счетом и суммой чаевых')
    fig2= px.scatter(tips,x='tip',y= 'total_bill',
    size='tip', hover_name='total_bill')
    fig2.update_layout(margin=dict(l=5,r=5,b=10,t=10))
    st.write(fig2)


if option == 'По размеру группы посетителей':
    st.header('Корреляция между общим счетом, суммой чаевых и размером группы посетителей')
    fig2= px.scatter(tips,x='tip',y= 'total_bill',
        size='tip', color='size', hover_name='total_bill')
    fig2.update_layout(margin=dict(l=5,r=5,b=10,t=10))
    st.write(fig2)


if option == "По дню недели и времени":
    st.header("Корреляция между днем недели и размером счета")
    fig3 = px.box(tips, x='day', y='total_bill',color='day')
    fig3.update_layout(margin=dict(l=5,r=5,b=10,t=10))
    st.write(fig3)



    st.header("Сравнение общего счета с количеством посетителей по дням недели и времени суток")
    fig5 = px.box(tips, x='total_bill', y='day',color='time')
    fig5.update_layout(margin=dict(l=5,r=5,b=10,t=10))
    st.write(fig5)



    dinner = tips[tips['time'] == 'Dinner']['tip']
    lunch = tips[tips['time'] == 'Lunch']['tip']

    st.header("Распределение чаевых в зависимости от времени суток")

    fig6 = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Во время обеда", "Во время ужина"))

    fig6.add_trace(go.Histogram(x=lunch),
                row=1, col=1)

    fig6.add_trace(go.Histogram(x=dinner),
                row=1, col=2)

    fig6.update_layout(margin=dict(l=30,r=30,b=30,t=30),
    showlegend=False)
    st.write(fig6)




if option == 'По полу человека':
    st.header("Сравнение количества мужчин и женщин по дням недели")
    fig4 = px.scatter(tips, x='tip', y='day',color='sex')
    fig4.update_layout(margin=dict(l=5,r=5,b=10,t=10))
    st.write(fig4)


    male = tips[tips['sex'] == 'Male']
    male['smoker'] = male['smoker'].replace({'No': 'Nonsmoker', 'Yes':'Smoker'})
    female = tips[tips['sex'] == 'Female']
    female['smoker'] = female['smoker'].replace({'No': 'Nonsmoker', 'Yes':'Smoker'})

    st.header("Распределение чаевых и общего счета в зависимости от курящего/некурящего человека")

    st.write('Мужчины')
    fig7 = px.scatter(male, x='tip', y='total_bill',color='smoker')
    fig7.update_layout(margin=dict(l=5,r=5,b=10,t=10))
    st.write(fig7)

    st.write('Женщины')
    fig8 = px.scatter(female, x='tip', y='total_bill',color='smoker')
    fig8.update_layout(margin=dict(l=5,r=5,b=10,t=10))
    st.write(fig8)



