#!/bin/bash

echo "🚀 Configurando aplicação..."

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Criar banco de dados PostgreSQL (se necessário)
# createdb ecommerce

# Rodar migrações
python manage.py migrate

# Criar superusuário
echo "Criando superusuário..."
python manage.py createsuperuser

# Carregar dados iniciais
python manage.py loaddata apps/products/fixtures/initial_products.json

echo "✅ Aplicação configurada com sucesso!"
echo "Execute: python manage.py runserver"