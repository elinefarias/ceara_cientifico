from fastapi import APIRouter
from use_case.news_brasil import news_brasil
from use_case.summary import summary

router = APIRouter(
    prefix="/headlines",
    tags=['HEADLINES']
)


@router.post('/get_news_brasil')
def get_news_brasil_controller():
    return news_brasil()


@router.post('/get_summary')
def get_summary_controller():
    return summary()
