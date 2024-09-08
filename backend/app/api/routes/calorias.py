from sqlalchemy.orm import Session
from sqlmodel import select
from app.models import PlanoBase, Avaliacao, dieta_refeicoes

def calculate_imc(peso: float, altura: float) -> float:
    if altura <= 0:
        return 0
    return peso / (altura ** 2)

def calculate_calories(avaliacao: Avaliacao) -> int:
    imc = calculate_imc(peso=avaliacao.peso,altura=avaliacao.altura)
    # Example logic based on IMC ranges
    if imc < 18.5:
        return 2500  # Example calories for underweight
    elif imc < 24.9:
        return 2000  # Example calories for normal weight
    elif imc < 29.9:
        return 1800  # Example calories for overweight
    else:
        return 1600  # Example calories for obesity

