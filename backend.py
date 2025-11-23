from flask import Flask, render_template, render_template_string, request
from function import gen_theme, gen_story, gen_prompt_imgs, save_audio, save_img, gen_audio, fiximg
import os

app = Flask(__name__)



@app.route("/")
def who():
    return render_template('name.html')

@app.route("/name", methods=['POST'])
def name():
    global name
    name = request.form['name']

    return render_template('age.html', name=name)

@app.route("/age", methods=['POST'])
def age():                
    global age
    global summary
    age = request.form['age']
    summary = gen_theme(age)
    return render_template('story.html', name=name, age=age, summary=summary)

@app.route("/story", methods=['POST'])
def story():
    global theme
    global story
    global title
    global characters

    theme = request.form['story']
    story= gen_story(theme, age)
    title = story['title']
    characters = story['characters']
    return render_template('style.html', title=title, characters=characters, story=story)


@app.route("/style1", methods=['POST'])
def style1():
    global story_list
    global len_pages

    promptlist=gen_prompt_imgs(story, 0)
    story_list = story['pages']
    len_pages = len(story_list)

    directory_path = f'./books/{title}'
    os.makedirs(directory_path, exist_ok=True)

    with open(f'./books/{title}/{title}.txt', 'w', encoding='utf-8') as file:
            file.write(str(story))
            file.write(str(promptlist))

    with open('./templates/fix_save.html', 'r', encoding='utf-8') as f:
        page = f.read()
    page = render_template_string(page, title=title, characters=characters, name=name, data=story_list)
    with open(f'./books/{title}/{title}_fix.html', 'w', encoding='utf-8') as f:
        f.write(page)
    
    return render_template('fix.html', title=title, characters=characters, name=name, data=story_list)

@app.route("/style2", methods=['POST'])
def style2():
    global story_list
    global len_pages

    promptlist=gen_prompt_imgs(story, 1)
    story_list = story['pages']
    len_pages = len(story_list)

    directory_path = f'./books/{title}'
    os.makedirs(directory_path, exist_ok=True)

    with open(f'./books/{title}/{title}.txt', 'w', encoding='utf-8') as file:
            file.write(str(story))
            file.write(str(promptlist))

    with open('./templates/fix_save.html', 'r', encoding='utf-8') as f:
        page = f.read()
    page = render_template_string(page, title=title, characters=characters, name=name, data=story_list)
    with open(f'./books/{title}/{title}_fix.html', 'w', encoding='utf-8') as f:
        f.write(page)
    
    return render_template('fix.html', title=title, characters=characters, name=name, data=story_list)

@app.route("/result", methods=['POST'])
def result():
     storylist = []
     
     for i in range(len_pages):
          storylist.append(request.form[str(i)])

     gen_audio(storylist)
     save_audio(title)
     save_img(title)

     with open('./templates/result_save.html', 'r', encoding='utf-8') as f:
        page = f.read()
     page = render_template_string(page, name=name, title=title, data=storylist)
     with open(f'./books/{title}/{title}.html', 'w', encoding='utf-8') as f:
        f.write(page)

     return render_template('result.html', name=name, title=title, data = storylist)


if __name__ == '__main__':
    app.run(debug=True, port=5001)


