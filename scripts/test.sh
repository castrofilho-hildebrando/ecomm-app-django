#!/bin/bash

echo "🧪 Rodando testes..."

# Rodar testes com cobertura
pytest --cov=. --cov-report=html --cov-report=term-missing

echo "✅ Testes concluídos!"
echo "Veja o relatório em: htmlcov/index.html"