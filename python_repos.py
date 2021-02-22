import requests


# Faz uma chamada de API e armazena a resposta
url = "https://api.github.com/search/repositories?q=language:python&sort=stars"

r = requests.get(url)
print("Status code:", r.status_code)

# Armazena a resposta da API em uma variável
response_dict = r.json()

# Processa o resultado
print("Total repositories: ", response_dict["total_count"])

# Explora informações sobre os repositórios
repo_dicts = response_dict["items"]

print("Repositories returned: ", len(repo_dicts))


print("\nSelected information about first repository:")

# Analisa todos os repositorios de items
for repo_dict in repo_dicts:
    print("\nName:", repo_dict["name"])
    print("Owner:", repo_dict["owner"]["login"])
    print("Stars:", repo_dict["stargazers_count"])
    print("Repository:", repo_dict["html_url"])
    print("Description:", repo_dict["description"])

# Pág. 429 - Monitorando os limites
