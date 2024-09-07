from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models import User, UserCreate
from sqlmodel import SQLModel,text
# from app.core.engine import engine
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines

    # This works because the models are already imported and registered from app.models
    SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)

    create_procedure_sql = """
        CREATE OR REPLACE FUNCTION get_dieta_by_max_calories(calories NUMERIC)
        RETURNS TABLE(id_dieta INT) AS $$
        BEGIN
            RETURN QUERY
            SELECT dr.id_dieta
            FROM dieta_refeicoes dr
            JOIN refeicao r_manha ON dr.id_ref_manha = r_manha.id
            JOIN refeicao r_tarde ON dr.id_ref_tarde = r_tarde.id
            JOIN refeicao r_noite ON dr.id_ref_noite = r_noite.id
            GROUP BY dr.id_dieta
            HAVING SUM(r_manha.calories + r_tarde.calories + r_noite.calories) <= calories
            ORDER BY SUM(r_manha.calories + r_tarde.calories + r_noite.calories) DESC
            LIMIT 1;
        END;
        $$ LANGUAGE plpgsql;
        """
    with engine.connect() as connection:
        connection.execute(text(create_procedure_sql))