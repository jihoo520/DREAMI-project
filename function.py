from openai import OpenAI
import os
import json
import urllib.request
from pathlib import Path
import warnings
import shutil
from PIL import Image 

warnings.filterwarnings("ignore", category=DeprecationWarning)

client = OpenAI(api_key="sk-AIzaSyDJ_CaGMzsGHyMzwyvkkht4BCtcqfRMFac")

def clearr():
    folder_path = "./static/images/"
    files = os.listdir(folder_path)
    
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

def gen_theme(age):
    print("추천 주제 생성중\n")
    response = client.chat.completions.create(
            model="gpt-4o",
            response_format={ "type": "json_object" },
            messages=[
                
                {"role": "system", "content": """ """},
                {"role": "user", "content": f""" 아동발달학을 기반으로 {age}세를 위한 교육적이고 창의적이고 흥미롭고 재밌고 교훈을 줄수있는 자세한 동화 summary 텍스트 300자 이내로 5개 생성해서 'summary'라는 이름의 리스트에 담아줘 title은 필요없어 리스트 안에 딕셔너리 넣지말고 텍스트만 넣어줘. json형식으로 답변해줘. """}
            ],
            temperature = 0.7
        )
    summary = response.choices[0].message.content
    print("\n\n",summary)
    summary = json.loads(summary)
    summary = summary['summary']
    summarys = ''

    for idx, i in enumerate(summary):
        if idx==4:
              summarys += f'추천 주제 {idx+1}.\n{i}'
        else:
            summarys += f'추천 주제 {idx+1}.\n{i}\n\n'

    print(summarys)

    return summarys
    



def gen_story(theme,age):
    print("스토리 생성 중\n\n")
    response = client.chat.completions.create(
            model="gpt-4o",
            response_format={ "type": "json_object" },
            messages=[
                
                {"role": "system", "content": """ """},
                {"role": "user", "content": f""" 
                   너는 세계적으로 유명한 동화 작가야. {age}살 아이도 이해할만한 "{theme}"라는 내용을 바탕으로 표현이 풍부하고 감성적이고 창의적이고 재밌고 짜임새있고 교육적인 동화를 1000글자 작성해줘. 처음부분에는 주인공을 소개하는 내용을 넣어줘. 각 등장인물의 이름을 반복적으로 사용하고 "친구들"과 같은 대명사 표현은 사용하지 마세요 등장인물의 이름을 반복적으로 사용하세요. 그리고 텍스트를 8개로 나눠서 pages 리스트에 담아줘. 그리고 주인공의 이름이 들어가면서 동화 내용에 어울리고 재밌는 동화 제목을 생성해서 title로 해줘 특수기호는 넣지마. 모든 characters의 key값에는 character의 이름을 넣고 value값은 한줄로 작성해줘 character가 무생물이라면 무생물 이름, 색깔을 중심으로 설명한 자세한 외형 설명을 자세히 한줄로 생성해줘. 동물이라면 동물 이름, 색깔을 중심으로 하는 자세한 외형 설명을 한줄로 자세히 생성해줘. 사람이라면 이름, 성별, 나이, 눈동자 색깔 헤어스타일과 옷스타일의 색깔을 중심으로 자세히 한줄로 생성해줘. 성격이나 역할같은 설명은 필요없어. title, pages, characters의 내용을 정리해서 json형식으로 답변해줘 """}
                
            ],
            temperature=0.5
        )
    story = response.choices[0].message.content
    print("스토리 생성 완료\n\n",story)
    story = json.loads(story)
    return story



def gen_prompt_imgs(story,stylenum):
        clearr()
        print("\n오디오/프롬프트/이미지 생성 시작\n\n")
        pages = story['pages']
        characters = story['characters']
        character_name = list(characters.keys())
        promptlist = [0,0,0,0,0,0,0,0]

        for idx, page in enumerate(pages):

            response = client.chat.completions.create(
                    model="gpt-4o",
                    response_format={ "type": "json_object" },
                    messages=[
                        {"role": "system", "content": """ """},
                        {"role": "user", "content": f""" 
                        key가 prompt인 json형식으로 답변해줘. "{page}"를 잘 설명하는 중요한 한 문장을 캐릭터를 중심으로 그림을 그리고 싶어 시각적인것만 설명해줘 대사는 사용하지마. 배경을 먼저 설명하고 캐릭터의 위치와 표정, 행동을 중심으로 시각적인것만 설명해줘 모든 주어는 등장하는 캐릭터 이름만을 사용해줘. 캐릭터의 외형은 설명하지마. 한국어로 작성해줘. """}
                    ],
                    temperature=0.1
                )
            prompt = response.choices[0].message.content
            prompt = json.loads(prompt)
            prompt = prompt['prompt']
            for i in character_name:
                    prompt = prompt.replace(i,str(i+":"+"["+characters[i]+"]"))
            print(page,'\n',prompt)

            try:
                style=[f" '{prompt}'의 장면을 3D 애니메이션 스타일, 몽환적이고 환상적인 분위기의 디즈니 영화 같은 느낌으로 캐릭터들은 큰 눈과 둥글고 부드러운 얼굴로 매우 귀엽게 묘사하고 캐릭터의 디테일을 매우 사실적으로 묘사한 디지털 아트 일러스트 ",
                   f" '{prompt}'의 장면을 사실주의 스타일, 몽환적이고 환상적인 분위기의 실제와 비슷하게 디테일을 매우 사실적으로 묘사한 밝은 색감의 수채화 물감으로 그린 그림  스타일의 일러스트 " ]
                prompt = style[stylenum]

                response = client.images.generate(
                            model="dall-e-3",
                            prompt=f"{prompt}",
                            size="1024x1024",
                            quality="standard",
                            n=1,
                            )
                url = response.data[0].url
                img_dest = "./static/images"
                urllib.request.urlretrieve(url, img_dest + f"/{idx}.jpg")
                print(f"({(idx)}/{len(pages)}) 완료\n\n")
                promptlist[idx] = prompt

            except:
                print("error")
        return promptlist
                
        
def gen_audio(list):
    for idx, page in enumerate(list):
            speech_file_path = Path(__file__).parent / f"./static/audio/{idx}.mp3"
            response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=f"{page}"
            )
            response.stream_to_file(speech_file_path)
        


def save_img(title):
    source_folder = './static/images'
    target_folder = f'./books/{title}/images'

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for item in os.listdir(source_folder):
        item_path = os.path.join(source_folder, item)

        if os.path.isfile(item_path):
            try:
                Image.open(item_path)
                target_path = os.path.join(target_folder, item)
                shutil.copy(item_path, target_path)
            except:
                pass



def save_audio(title):
    source_folder = './static/audio'
    target_folder = f'./books/{title}/audio'

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for item in os.listdir(source_folder):
        item_path = os.path.join(source_folder, item)

        if os.path.isfile(item_path):
            if item.endswith('.mp3'):
                target_path = os.path.join(target_folder, item)
                shutil.copy(item_path, target_path)





def fiximg(nn,prompt,n):
    print('이미지 재생성 시작')
    style=[ f" '{prompt}'의 장면을 3D 애니메이션 스타일, 몽환적이고 환상적인 분위기의 디즈니 영화 같은 느낌으로 캐릭터들은 큰 눈과 둥글고 부드러운 얼굴로 매우 귀엽게 묘사하고 캐릭터의 디테일을 매우 사실적으로 묘사한 디지털 아트 일러스트 ",
            f" '{prompt}'의 장면을 사실주의 스타일, 몽환적이고 환상적인 분위기의 실제와 비슷하게 디테일을 매우 사실적으로 묘사한 밝은 색감의 수채화 물감으로 그린듯한 그림 스타일 일러스트 " ]
    prompt = style[nn]

    response = client.images.generate(
                            model="dall-e-3",
                            prompt=f"{prompt}",
                            size="1024x1024",
                            quality="standard",
                            n=1,
                            )
    url = response.data[0].url
    img_dest = "./static/images/"
    urllib.request.urlretrieve(url, img_dest + f"{n}_fix.jpg")
    print("완료")
