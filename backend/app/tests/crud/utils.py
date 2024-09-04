
import random
from datetime import datetime, timedelta

especialidades = ['Calistenia',
                    'Treino de força',
                    'Treino de tensão mecânica',
                    'Treino metabólico',
                    'Treino de condicionamento'
                    ]


def random_datetime(start, end):
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)

start_date = datetime(2020, 1, 1)
end_date = datetime(2023, 12, 31)

random_date = random_datetime(start_date, end_date)