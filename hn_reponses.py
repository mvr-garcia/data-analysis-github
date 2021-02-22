import requests
from operator import itemgetter
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

# Faz uma chamada de API e armazena a resposta
url = "https://hacker-news.firebaseio.com/v0/topstories.json"

r = requests.get(url)
print("Status Code: ", r.status_code)

# Processa informações sobre cada artigo submetido
submission_ids = r.json()

submission_dicts = []
title, plot_dicts = [], []

for submission_id in submission_ids[:30]:
    # Cria uma chamada de API separada para cada artigo submetido
    url = ("https://hacker-news.firebaseio.com/v0/item/" + str(submission_id) + ".json")

    submission_r = requests.get(url)
    # Imprime o resultado da "request", 200 significa sucesso.
    print("Status Code: ", submission_r.status_code)

    # Processa informações sobre cada artigo
    response_dict = submission_r.json()

    # Pode ser que algum artigo não contenha as info que estamos precisando
    # para o programa não travar, colocamos as instruções em um try_except
    try:
        plot_dict = {"title": response_dict["title"], "value": int(response_dict["descendants"]) or 0, "xlink":
                     "http://news.ycombinator.com/item?id=" + str(response_dict["id"])}
        # Pode ser que alguns artigos não apresentem comentário, nesse caso o "or 0" entra e atribui 0 a esse artigo
        plot_dicts.append(plot_dict)
    except KeyError:
        print("Key doesn't found.")

# Organiza em ordem decrescente pelo numero de comentários
plot_dicts = sorted(plot_dicts, key=itemgetter("value"), reverse=True)

# Desempacota o titulo de cada artigo em uma lista de titulos, que irá representar as barras do grafico
for d in plot_dicts:
    title.append(d["title"])

# Cria a visualização
my_style = LS("#00FF7F", base_style=LCS, opacity=".3")
my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 24
my_config.label_font_size = 14
my_config.major_label_font_size = 18
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000

chart = pygal.Bar(my_config, style=my_style)
chart.title = "Most-Commented on HackerNews"
chart.x_labels = title
chart.add("", plot_dicts)
chart.render_to_file("hn_repos.svg")
