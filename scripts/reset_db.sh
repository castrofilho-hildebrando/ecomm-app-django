#!/bin/bash

echo "⚠️  ATENÇÃO: Isso vai apagar todos os dados!"
read -p "Deseja continuar? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]
then
    # Dropar e recriar banco
    dropdb ecommerce
    createdb ecommerce
    
    # Rodar migrações
    python manage.py migrate
    
    # Criar superusuário
    python manage.py createsuperuser
    
    echo "✅ Banco resetado!"
fi