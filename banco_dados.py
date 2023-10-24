# Inicialize uma lista vazia para armazenar os produtos
lista_de_produtos = []

# Função para adicionar um novo produto à lista
def adicionar_produto(nome, id, preco, peso):
    produto = {
        "nome": nome,
        "id": id,
        "preco": preco,
        "peso": peso
    }
    lista_de_produtos.append(produto)

# Função para listar todos os produtos
def listar_produtos():
    for produto in lista_de_produtos:
        print(f"Nome: {produto['nome']}, ID: {produto['id']}, Preço: {produto['preco']}, Peso: {produto['peso']}")

# Exemplo de uso:
adicionar_produto("Produto A", 1, 10.99, 0.5)
adicionar_produto("Produto B", 2, 25.50, 1.2)

# Listar os produtos
listar_produtos()
