import streamlit as st
import random
import json
import matplotlib.pyplot as plt



st.set_page_config( page_title='Human Rights',
                    layout="wide",
                    initial_sidebar_state="expanded")

################ Model ################
class Model:

    def __init__(self):
       self.title = 'Human Rights'
       self.current_level = 1
       self.score = 0
       self.questions_level1, self.questions_level2, self.questions_level3 = self.read_questions('questions.json','human_rights.json')
       self.score_level1 = 0
       self.score_level2 = 30
       self.score_level3 = 60
       self.final_score = 90


    def read_questions(self,f1, f2):
        ''' Reads all the questions and separates them by level and adds the article title and the explanation acording to the level'''
        with open(f1, 'r') as f:
            questions = json.load(f)
        with open(f2, 'r') as f:
            articles = json.load(f)
        
        level1 = []
        level2 = []
        level3 = []

        for question in questions:
            if question[1] == 1:
                question.remove(question[1])
                question.append(articles[question[0]][0])
                question.append(articles[question[0]][1])
                level1.append(question)
            elif question[1] == 2:
                question.remove(question[1])
                question.append(articles[question[0]][0])
                question.append(articles[question[0]][2])
                level2.append(question)
            else:
                question.remove(question[1])
                question.append(articles[question[0]][0])
                question.append(articles[question[0]][3])
                level3.append(question)

        return level1,level2,level3
   

    def get_question(self):
        '''Depending on the current level, returns a random question from that level'''
        if self.current_level == 1:
           return random.choice(self.questions_level1)
        elif self.current_level == 2:
           return random.choice(self.questions_level2)
        elif self.current_level == 3:
           return random.choice(self.questions_level3)

    def get_levels(self):
        '''Gets the amount of score from each level'''
        if self.score <= self.score_level2:
            level1 = self.score
            level2 = 0
            level3 = 0
        elif self.score > self.score_level2 and self.score <= self.score_level3:
            level1 = self.score_level2
            level2 = self.score - level1
            level3 = 0
        else:
            level1 = self.score_level2
            level2 = self.score_level2
            level3 = self.score - (level1 + level2)

        return level1, level2, level3
    
    def get_score(self):
        "Returns current score"
        return self.score
    
    def get_level(self):
        "Returns current level"
        return self.current_level
    

    def right_answer(self):
        '''Sums 3 to the score and checks if we have to change the level'''
        self.score += 3
        if self.score >= self.score_level2:
            self.current_level = 2
        if self.score >= self.score_level3:
            self.current_level = 3    

    def wrong_answer(self):
        '''Subtracts 1 to the score and checks if we have to change the level'''
        self.score -= 1
        if self.score <= self.score_level3:
            self.current_level = 2
        if self.score <= self.score_level2:
            self.current_level = 1
        self.score = max(0,self.score)



    def new_game(self):
        "Restarts the score and level"
        self.score = 0
        self.current_level = 1

    def end_game(self):
        "Chekcs if you have reach the end of the game"
        return self.score >= self.final_score
    


################ View  ################

def radio_chosen():
    st.session_state['radio_disabled'] = True
    st.session_state['new_question'] = False
   

def next_question():
    st.session_state['radio_disabled'] =  False
    st.session_state['new_question'] = True
    st.session_state['key'] += 1

def new_game():
    st.session_state['model'].new_game()
    st.session_state['next_question_disabled']=False
    next_question()

# Inicialitzation of session variables
if 'iniciat' not in st.session_state:
    st.session_state['iniciat']=True
    st.session_state['radio_disabled']=False
    st.session_state['new_question']=False
    st.session_state['next_question_disabled']=False
    st.session_state['model'] = Model()
    st.session_state['question'] = st.session_state['model'].get_question()
    st.session_state['key']=0

levels =['Level 1','Level 2','Level 3']

### Title
titol=f":blue[{st.session_state['model'].title}]"
col1, mid, col2 = st.columns([1,1,20])
with col1:
    st.image('HumanRightsLogo.png', width=85)
with col2:
    st.title(titol)
st.text(' ')


if st.session_state['new_question']:
    st.session_state['question'] = None
    st.session_state['question'] = st.session_state['model'].get_question()




col3,col4 = st.columns ([1,10])
with col3:
    st.image(st.session_state['question'][0]+'.png', width=80) 
with col4:
    col5,col6 = st.columns([3,1])
    with col5:
        st.header(st.session_state['question'][-2])
    with col6:
        st.header('You are on '+levels[st.session_state['model'].get_level()-1])


# Score and questions columns
col1, col2 = st.columns([4,1])

with col1 :  

    with st.expander(f"Explanation {levels[st.session_state['model'].get_level()-1]} 📚"):
                    st.write(st.session_state["question"][-1])

    st.subheader(st.session_state['question'][2])  
    answer = None
    answer = st.radio(' ',st.session_state['question'][3:6], index = None, disabled = st.session_state['radio_disabled'],on_change=radio_chosen, key=st.session_state['key'])    
    if answer :
        selected_index = st.session_state['question'][3:6].index(answer)
        if selected_index == st.session_state['question'][1]-1 :
            st.subheader(":green[Right answer!!]")
            st.session_state['model'].right_answer()
            if st.session_state['model'].end_game():
                st.balloons()
                st.session_state['next_question_disabled']=True
           
        else:
            msg = f':red[{st.session_state["question"][st.session_state["question"][1]+2]}]'
            st.subheader(msg)
            st.session_state['model'].wrong_answer()
            
        

    st.button('next question',on_click=next_question,disabled=st.session_state['next_question_disabled'])

# Stacked barplot
with col2 :
    fig, ax = plt.subplots()
    l1,l2,l3 = st.session_state['model'].get_levels()


    ax.bar(' ', l1, color='g')
    ax.bar(' ', l2, bottom = l1, color='yellow')
    ax.bar(' ', l3, bottom = l1+l2, color='r')
    ax.axis('off')  
    ax.set_yticks([30,60,90])
    st.pyplot(fig)
    st.button('new game',on_click=new_game)





