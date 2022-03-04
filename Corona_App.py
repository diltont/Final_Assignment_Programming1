


#%%

import pandas as pd



import plotly.express as px

from plotly.subplots import make_subplots
import plotly.graph_objects as go

import streamlit as st

st.set_page_config(page_title="Corona App", page_icon="🧊", layout="wide")

covid_df=pd.read_csv('C:\Dilton G\Hanze_University\Q2 Hanze\Programming 1\Final Assignment\coviddata.csv')
covid_df.drop(covid_df.columns[[6,9,12,23,23,24,25,26,27,28,29,30,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,59,63,64,65,66]], axis=1,inplace=True)


@st.cache
def preprocess(df):
  columns=df.select_dtypes(include=['object']).columns# finding objects data types
  # changing location to category
  df['location']=df['location'].astype('category')

  # changing date to datetime
  try:
    df['date']=pd.to_datetime(df['date'],format='%d/%m/%Y')
  except:
    df['date']=pd.to_datetime(df['date'],format='%Y/%m/%d')
    
  # create months for plotting if needed
  df['month']=df['date'].dt.month_name()
  df['day']=df['date'].dt.day_name()
  df['week']=df['date'].dt.isocalendar().week
  # the most data is avaialble upto 29-09-2021
  df=df.loc[df['date']<'2021-09-30 00:00:00']
  return df

covid_df=preprocess(covid_df)


#%%
# getting the covid information of europe
covideu_df=covid_df[covid_df['continent'].str.contains('Europe',na=False)].reset_index(drop=True)

#getting the covid information of Asia
covidasia_df=covid_df.query('continent == "Asia"').reset_index(drop=True)


#%% 

#Exploratory data analysis of covid 

@st.cache
def explorecovid(var,continent,df):
  """var:Column name, continent: Europe or Asia
     df: Dataframe of Europe or Asia"""
     
  total_covidvar = df.groupby('location').max().sort_values(var, ascending=False)
  
  total_covidvar=total_covidvar[total_covidvar['continent']==continent]
  total_covidvar= total_covidvar.iloc[:10]
  return total_covidvar

total_covideu=explorecovid('total_cases','Europe',covideu_df)#total_cases_per_million
total_covidasia=explorecovid('total_cases','Asia',covidasia_df)

total_deatheu=explorecovid('total_deaths','Europe',covideu_df)
total_deathasia=explorecovid('total_deaths','Asia',covidasia_df)


#%%
#Barplot plots total deaths or cases of europe and asia

@st.cache
def barplot(df,var,cont):
  '''df : dataframe from explorecovid function of europe
     var: column name, '''
  title='Countries with most '+var+' '+ 'in'+' '+ cont +' ' + 'till November 2021'
  
  fig = px.bar(df, x=var,title=title, color=df.index)

  #plot(fig, auto_open=True)
  return fig

#%%
#"Barplot1 plots the top 10 countries of Asia and Europe "

@st.cache
def barplot1(eu,asia,var):

  fig = make_subplots(rows=1, cols=2)
  title='Countries with most '+ var+' '+ 'in' +' '+ ' Asia and Europe till November 2021'
  
  fig.add_trace(go.Bar(x=eu[var], name='Europe',text=eu.index,
      marker_color=px.colors.qualitative.Dark24[0]),row=1, col=1)
  
  fig.add_trace(go.Bar(x=asia[var] ,name='Asia',text=asia.index,
      marker_color=px.colors.qualitative.Dark24[1]),row=1, col=2)
      
  fig.update_layout(height=500, width=1000,
    
    legend_title="Continents", title_text=title)
  fig['layout']['xaxis']['title']=var
  fig['layout']['xaxis2']['title']=var
  fig['layout']['yaxis']['title']='Countries'
  fig['layout']['yaxis2']['title']='Countries'
  return fig
  #plot(fig, auto_open=True)

#%%
#'''world plot for total deaths'''

world=covid_df.groupby('location').agg({'total_cases':max,'total_deaths':max,'total_cases_per_million':max,'total_deaths_per_million':max}).reset_index()
@st.cache
def country_map(df, column, pal):
    df = df[df[column]>0]
    fig = px.choropleth(df, locations="location", locationmode='country names', 
                  color=column, hover_name="location", 
                  title=column, hover_data=[column], color_continuous_scale=pal)
    fig.update_layout(height=500, width=1000)
    return fig



#%%

st.title('Simple Corona App ')

st.sidebar.header('Select continent')

sel_cont=st.sidebar.selectbox('Continent',('World','Europe','Asia','Asia & Europe'))


st.sidebar.header('Select variable')
variables=['total_cases','total_deaths','total_cases_per_million','total_deaths_per_million']
covars = st.sidebar.selectbox(
    "Select the variable:",
    options=variables)


st.sidebar.markdown('🦠 **Covid-19 App** 🦠 ')
st.sidebar.markdown(''' 
This app shows different corona virus cases and deaths of the World, Europe and Asia.
The data considerd for this analysis is betwwen  01-02-2020 to 31-09-2021.
Select the different options to vary the Visualization.'Continent' selection box
gives the option to select between World,Europe and Asia. When world is selected,
world map is shown with the varaiable selected from 'select the variable' 
selection box. Plots are made in plotly and are interactive.
                    
Made by : 
**Dilton Thomas**  ''')                                                        

st.write(sel_cont)
tt=pd.Series(covars).isin(variables)
if (sel_cont == 'Europe') & (tt.bool()==True):
  
  tempeu=explorecovid(covars,'Europe',covideu_df)
  tfig=barplot(tempeu,covars,cont='Europe')
  st.plotly_chart(tfig,use_container_width=True)

elif (sel_cont == 'Asia') & (tt.bool()==True):
  tempasia=explorecovid(covars,'Asia',covidasia_df)
  tfig=barplot(tempasia,covars,cont='Asia')
  st.plotly_chart(tfig,use_container_width=True)
  
elif(sel_cont == 'Asia & Europe') & (tt.bool()==True):
  tempeu=explorecovid(covars,'Europe',covideu_df)
  tempasia=explorecovid(covars,'Asia',covidasia_df)
  tfig= barplot1(tempeu,tempasia,var=covars)
  
  st.plotly_chart(tfig,use_container_width=True)
  
elif(sel_cont == 'World') & (tt.bool()==True):
  
  fig=country_map(world,covars , pal='twilight')
  st.plotly_chart(fig,use_container_width=True)
  
  




