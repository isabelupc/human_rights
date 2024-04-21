import streamlit as st
import pandas as pd
from model import CBR



################ View  ################
def view(model):

    # Inicialització de les variables de sessio
    if 'iniciat' not in st.session_state:
        st.session_state['iniciat']=True
        st.session_state['max_id']=model.last_user()
        st.session_state['primer']=1
        st.session_state['idx_recomanacio']=0
        st.session_state['mostrar_recomanacions']=False
        st.session_state['ha_comprat']=False

    # Funcions auxiliars i callbacks   
    def treure_recomanacions():
            st.session_state['mostrar_recomanacions']=False
            st.session_state['idx_recomanacio']=0

    def nou_call():  
        model.add_user()
        st.session_state['primer'] = model.last_user()
        st.session_state['max_id'] = st.session_state['primer']
        treure_recomanacions()

    def comprar_call(idx):
        model.afegir_rating(st.session_state['recomanacions'][idx][3],st.session_state['recomanacions'][idx][4])
        st.session_state['ha_comprat']=True

    def calcula_index_recomanacions():
        maxim = len(st.session_state['recomanacions'])
        if st.session_state['ha_comprat']:
            idx1 = st.session_state['idx_recomanacio']-3
            if idx1<0:
                idx1 += maxim
        else: 
            idx1 = st.session_state['idx_recomanacio']
        idx2 = idx1+1
        if idx2 >= maxim:
            idx2 = idx2%maxim
        idx3 = idx2+1
        if idx3 >= maxim:
            idx3 = idx3%maxim
        nou = idx3+1
        if nou >= maxim:
            nou = nou%maxim
        st.session_state['idx_recomanacio']=nou
        st.session_state['ha_comprat']=False
        return idx1,idx2,idx3

    ### Titol
    titol=f":blue[{model.title}]"
    st.title(titol)

    ### Usuari
    col1,col2,col3 = st.columns([2,1,8],gap='small')

    with col1:
        lector = st.number_input('Entra codi de Lector (o clica NOU) 👤',1,st.session_state['max_id'],st.session_state['primer'],on_change=treure_recomanacions)
        nom, dades = model.user_data(lector)
  
    with col2:
        st.write(' ')
        st.write(' ')
        st.button('Nou',on_click=nou_call)

    with st.form('formulari1'): 
        col1,col2,col3 = st.columns([4,1,2],gap='medium')

        with col1:
            nom = st.text_input(label='Nom ✍🏼',value=nom)

        with col2:
            year = st.number_input('Any de naixement 🗓️',1900,2030,dades['year'])

        with col3:
            st.radio('Gènere ',model.get_sex_options(),horizontal=True)

        col4,col5 = st.columns([5,4],gap='small')
        with col4:
            st.write('') 
            llegits,configuracio = model.read(lector)
            new_config = {}
            for key,value in configuracio.items():
                if len(value)==1:
                    new_config[key] =value[0]
                else:
                    new_config[key] = st.column_config.NumberColumn(value[0],min_value=value[1],max_value=value[2],step=1)
            nous_llegits = st.data_editor(llegits,column_config=new_config,hide_index=True)
   
        with col5:
            print(dades['genre'])
            st.multiselect("Gèneres Literaris ",model.get_genre_options(),default=dades['genre'])
            st.radio('Vols llibres adaptats al cinema? 🎥',model.get_film_options(),horizontal=True)
            st.radio('Vols un Best Seller? 🎖️',model.get_bestseller_options(),horizontal=True)
            st.radio("Vols que el llibre formi part d'una saga? ",model.get_saga_options(),horizontal=True)
            st.radio('Quin tipus de lectura?',model.get_reading_options(),horizontal=True)
        
        submitted = st.form_submit_button("Desa Canvis i Recomana",type='primary')
        if submitted:
            model.change_name(lector,nom)
            st.session_state['mostrar_recomanacions']=True  
            st.session_state['idx_recomanacio'] = 0 

    ### Recomanacions     
    
    if st.session_state['mostrar_recomanacions']:
        with st.container(border=True):
            st.session_state['recomanacions'] = model.recomanacions(lector)
            if len(st.session_state['recomanacions'])==0 :
                st.subheader(':blue[Amb les dades que em dones, no et puc recomenar cap llibre]')
            else:
                st.subheader(':blue[Les teves recomanacions]')
                index = calcula_index_recomanacions()
                columnes = st.columns([2,2,2])
                noms_butons = ['Comprar','Comprar ','Comprar  ']
                for idx,col,buto in zip(index,columnes,noms_butons):
                    with col:
                        book = st.session_state['recomanacions'][idx][0]
                        writer = st.session_state['recomanacions'][idx][1]
                        st.write(f':red[***#{idx+1} {book}***]')
                        st.write(f':red[*{writer}*]')
                        with st.expander('Raonament'):
                            st.write(st.session_state['recomanacions'][idx][2])
                        st.button(buto,on_click=comprar_call,args=[idx])

            st.button('Mes Recomanacions',type='primary')


################ Model ################




################ Start  ################

## el set page s'ha nomes un cop i abans de qualsevol instrucció
st.set_page_config( page_title='Llibres',
                    layout="wide",
                    initial_sidebar_state="expanded")

if 'model' not in st.session_state:
  st.session_state['model'] = CBR()

view(st.session_state['model'])


