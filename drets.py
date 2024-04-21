import streamlit as st
import pandas as pd
from playsound import playsound


################ View  ################
def view(model):

    # Inicialització de les variables de sessio
    if 'iniciat' not in st.session_state:
        st.session_state['iniciat']=True
        st.session_state['level']=0
        st.session_state['score']=0
        st.session_state['radio_disabled']=False

    levels =[':large_orange_circle:',':large_yellow_circle:',':large_green_circle:']
    ### Titol
    titol=f":blue[{model.title}]"
    #st.title(titol)
    #st.image('HumanRightsLogo.png')

    col1, mid, col2 = st.columns([1,1,20])
    with col1:
        st.image('HumanRightsLogo.png', width=85)
    with col2:
        st.title(titol)
    st.text(' ')

    question = model.get_question(st.session_state['level'])
    col1,col2 = st.columns ([1,10])
    with col1:
       st.image(question[0]+'.png', width=80) 
    with col2:
       col3,col4 = st.columns([1,1])
       with col3:
          st.header('Free and Equal')
       with col4:
          st.subheader(levels[st.session_state['level']])   

    st.subheader(question[2])  
    
    answer = st.radio(' ',question[3:],index=None,disabled = st.session_state['radio_disabled'],on_change=radio_toggle)    
    if answer :
        selected_index = question[3:].index(answer)
        if selected_index == question[1]-1 :
            st.subheader(":green[Correcte!!]")
            playsound('right.wav')
        else:
            st.subheader('la resposta correcte era: '+question[question[1]+2])
            playsound('wrong.wav')
    
    st.button('next question',on_click=radio_toggle)
def radio_toggle():
   if st.session_state['radio_disabled']:
    st.session_state['radio_disabled'] = False
   else:
    st.session_state['radio_disabled'] = True
       
       
################ Model ################
class Model:
   def __init__(self):
      self.id = 1
      self.title = 'Human Rights'
   
   def get_question(self,level):
      return ['01',2,'how old are you?','I am very young','I am dead','I am 55 yo']



################ Start  ################

## el set page s'ha nomes un cop i abans de qualsevol instrucció
st.set_page_config( page_title='Human Rights',
                    layout="wide",
                    initial_sidebar_state="expanded")

if 'model' not in st.session_state:
  st.session_state['model'] = Model()

view(st.session_state['model'])


