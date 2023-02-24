import re  
from urllib import parse
import pytube 
from youtube_transcript_api import YouTubeTranscriptApi
import validators
import replicate

#set the  REPLICATE_API_TOKEN as en env variable
model = replicate.models.get("stability-ai/stable-diffusion")
version = model.versions.get("db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf")


def get_n_words(input_str:str, n:int = 100) ->str:
    result = re.findall(r'\w+', input_str)[:n]
    result = " ".join(result)
    return result 

#TODO: Preproccess the captions and  description to get only
#valid words and remove stop words.
def get_captions(url:str)->str:
    """
    url: a yt video url
    return the captions for the video as plain text
    Only the first 250 words

    """
    #get video id
    video_id = pytube.extract.video_id(url)
    #each element is {text:x, start:y, duration:z}
    srt_list = YouTubeTranscriptApi.get_transcript(video_id)
    
    plain_text = get_plain_text(srt_list)
    #Get only n words
    result = get_n_words(plain_text, n = 200)

    return result    

def get_plain_text(srt_list:list[dict])->str:
    lines = ''

    for sub in srt_list:
        lines += sub.get('text',None) + '\n'
    
    return lines 

def get_video_name(url:str)->str:
    yt= pytube.YouTube(url)
    return yt.title 
def get_video_description(url):
    yt= pytube.YouTube(url)
    return yt.description

def get_keywords(url):
    yt= pytube.YouTube(url)
    return yt.keywords

def get_video_info(url:str)-> str:
    if not validators.url(url):
        raise Exception(f"Invalid url {url}")

    video_title = get_video_name(url)
    tags = ''.join(x+"," for x in get_keywords(url))[:-1]
    captions = get_captions(url)

    return video_title,tags,captions

def get_image(
    prompt:str= "a vision of paradise. unreal engine"):
    # https://replicate.com/stability-ai/stable-diffusion/versions/db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf#input
    inputs = {
        # Input prompt
        'prompt':prompt ,

        # pixel dimensions of output image
        'image_dimensions': "768x768",

        # Specify things to not see in the output
        # 'negative_prompt': ...,

        # Number of images to output.
        # Range: 1 to 4
        'num_outputs': 1,

        # Number of denoising steps
        # Range: 1 to 500
        'num_inference_steps': 50,

        # Scale for classifier-free guidance
        # Range: 1 to 20
        'guidance_scale': 7.5,

        # Choose a scheduler.
        'scheduler': "DPMSolverMultistep",

        # Random seed. Leave blank to randomize the seed
        # 'seed': ...,
    }

    # https://replicate.com/stability-ai/stable-diffusion/versions/db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf#output-schema
    output = version.predict(**inputs)
    return output 
if __name__ == "__main__":
    urls_test = ["https://youtu.be/-a_wDBYNZzk"]
    urls_prompt = ["https://youtu.be/CC66RXeTn_4","https://youtu.be/AzQ3Xso7sLA","https://youtu.be/gs8mBQkdQ8Q",'https://youtu.be/sONZNcqiofQ']
    for url in urls_prompt:
        print("Video info: ",get_video_info(url))
        print()
        
    
    
