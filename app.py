import os 

import streamlit as st
import cohere
#from dotenv import load_dotenv
#load_dotenv()
from utils import get_video_info
from utils import get_image

co = cohere.Client(os.getenv('COHERE_API_KEY')) 
#https://youtu.be/Q0A35ZfgwHA
#TODO (VIDEO Info->Thumbnail prompt): use embeeding
#to extract the most relevant text from the captions
#compare video title with chunks of the captions 
#TODO use real examples, train the generative mode (image generation) with the concept of a thumbnail. Maybe collect and label several (thumbnail, description) pairs.
#  
BASE_PROMPT ="""
This program will create a prompt, describing the video from his information, the prompt must highlight the core topic of the video in order to create a piece of visual art from it. 
Given the video title, the tags and the transcript of a youtube video this program will generate a prompt to create an attractive  and eye-catching image (a thumbnail)  related to the video content.

Video Title: How I Would Learn to be a Data Analyst.

Tags: data viz by luke,business intelligence,data science,bi,computer science,data nerd,data analyst,data scientist,how to,data project,data analytics.

Transcript: what up done nerds i m luke a data analyst and my channel is all about tech and skills for data science and in this video today i wanted to cover my pathway for becoming a data analyst if i had to start over again and for this i m not going to be only sharing the skills that i recommend learning but also my process for learning different skills which i ve applied and refined over my time in school learning engineering to my time in the navy learning how to drive a nuclear powered submarine and then more recently to learning all the different skills of a data analyst in order to continue to gress further in my job this process has also been refined by my interactions from others that have not only gotten jobs as data analysts but also hired others for these roles as well my journey was filled with a lot of wasted time and effort and so i m hoping that this video helps save you effort and also time and learning the skills you need to know for your job so let s break into my recipe for learning anything and it.

Prompt: A man showing his career path  in a map, showing the technologies he learn with it, like excel, SQL and python. Bright and realistic scene, inspirational art, beautiful and eye-catching. 
--

Video Title: A Day in the Life of a Project Manager | Indeed.

Tags: Career Advice,Job Search,Career Coach,Career Path,Job Seeker,Worker,Work force,Interview,Job Interview,Interview tips,career tips,project manager,project management,motivation,inspire,motivate,day in the life,what does a project manager do,project manager skills,project management skills,project manager job duties,project management environment,project manager education,project management job duties.

Transcript: MUSIC PLAYING Hi I m Gillian and welcome to a day in the life of a project manager Come on MUSIC PLAYING So a project manager is really just focused on the full project lifecycle So I m kind of the person that gets everything kicked off and I m the last person that sees a project So I work in an agency called RPM which is focused on Broadway clients in the advertising space And I ve been there for a couple of years now and I really work across all of our different teams to get the project all the way completed through the agency I ve worked at a couple of different advertising agencies and this is definitely the most fun because it s such a great group of clients Our office has instated a work from home policy and a hybrid being able to go into the office So a lot of times I ll go in if I have something that s really important that I need a lot of people in that I know that they ll be in the office for Otherwise I can work from home and just be in my sweatpants.

Prompt: A woman on her office, showing her desk, with one macbook pro at the background and a PC in first plane. Bright and realistic scene, inspirational art, beautiful and eye-catching.
--

Video Title: Careers Have Changed Forever.

Tags: careers,highest paying careers,how to progress career,40 year career,how to get a promotion,highest paying jobs,highest paying jobs with no skills,working two jobs at once,career path,side hustles,starting your own business,easiest businesses to start,most demanding jobs,easiest jobs,how many hours per week to work,highest paying entry level jobs,how to set up a company,how money works,business,career,finance.

Transcript: you were born you are nurtured up to whatever your six then you get sent in the kindergarten and school and by the time you re 18 you come out and you go to college by the time you get out of college you get a job and then you retire with whatever 65 or so and then you enjoy your time and somewhere at a hot place right that s been the model of the past is that s not working that is absolutely not working anymore and in every respect go to school get your grades get into college become a professional and work your way up the corporate ladder until you can retire with your savings or a pension that s the plan for a lot of people and despite what a lot of hustle Bros on the internet might tell you now that s __ insane it s a good plan if you can stick to it nine to five jobs are picked on a lot usually by people that need a way to sell a get rich quick scheme the standard 40 year professional career has let millions of people enjoy very comfortable lives free.

Prompt: A photo of people going up the stairs in a train station, above view, bright and realistic scene.
Bright and realistic scene, inspirational art, beautiful and eye-catching.

--
"""
# Initialization
if 'output' not in st.session_state:
    st.session_state['output'] = 'Output:'

if 'gen_image' not in st.session_state:
    st.session_state['gen_image']= "Generated image"

if 'prompt' not in st.session_state:
    st.session_state['text'] = ''

def get_info(url:str)->tuple[str,str,str]:
    video_title, tags, transcript= get_video_info(url)
    return video_title,tags,transcript 

def generate_prompt(url:str):
    if len(url) == 0:
        return None
    video_title, tags, transcript = get_info(url)
    video_title+="."
    tags+="."
    transcript+="."
    new_request="\n"
    new_request +=f"Video Title: {video_title}\n"
    new_request += f"Tags: {tags}\n\n"
    new_request += f"Transcript: {transcript}\n\n"
    new_request += f"Prompt: "

    prompt = BASE_PROMPT + new_request
    #print("New Prompt: ", prompt)

    response = co.generate( 
    model='xlarge', 
    prompt=prompt, 
    max_tokens=50, 
    temperature=0.1, 
    k=0, 
    p=1, 
    frequency_penalty=0.6, 
    presence_penalty=0.5, 
    stop_sequences=["--"], 
    return_likelihoods='NONE') 

    thumbnail_prompt = response.generations[0].text
    #print("GENERATED PROMPT: ", thumbnail_prompt)

    #st.balloons()
    return thumbnail_prompt 

def generate_image(prompt:str):
    
    #print("GENERATED PROMPT: ", prompt)
    image_url = get_image(
    prompt= prompt)[0]
    #print("Image url:",image_url )

    st.session_state['output'] = image_url
    st.image(image_url, caption=prompt)
    

st.title('Thumbnail Generator')
st.subheader('Create thumbnails easily with AI')
#st.write('''This is a simple **Streamlit** app that generates hashtags from a small Post title caption.''')

#TODO add support for video files
input = st.text_area('Enter your youtube video url here:', height=100)
prompt = None 

#st.button('Generate Thumbnail', on_click = generate_image(input))
prompt = None 
if st.button('Generate Prompt'):
    prompt = generate_prompt(input)[:-2]
    st.session_state['prompt'] = prompt 
    st.text_area(label = "Prompt:",value = prompt,key = 'prompt', height=220 )
    #print("PROMPT: ",prompt)

print("PROMPT MIDDLE: ", prompt)
if st.button('Generate Image'):
    #print("PROMPT BEFORE:_ ", st.session_state['prompt'])
    generate_image( st.session_state['prompt'])
    
    



