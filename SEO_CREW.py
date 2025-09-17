import os
from urllib.parse import urlparse
from crewai import Agent, Task, Crew, Process

from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE")

def get_user_input():
    """Получить URL от пользователя с валидацией"""
    print("=" * 60)
    print("🚀 SEO CrewAI - Анализ сайта с помощью ИИ")
    print("=" * 60)
    
    while True:
        url = input("\n📝 Введите URL сайта для анализа: ").strip()
        
        if not url:
            print("❌ URL не может быть пустым. Попробуйте еще раз.")
            continue
            
        # Добавляем http:// если протокол не указан
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        # Валидация URL
        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                raise ValueError("Неверный формат URL")
            
            print(f"✅ URL принят: {url}")
            return url
            
        except Exception as e:
            print(f"❌ Неверный URL: {e}")
            print("💡 Пример корректного URL: example.com или https://example.com")
            continue

def create_tasks(target_url):
    """Создать задачи с указанным URL"""
    task1 = Task(
        description=f"Получить HTML-код страницы по ссылке {target_url}, распарсить HTML-код и извлечь отдельные слова из содержимого страницы.",
        expected_output="Список слов, извлечённых из HTML-кода страницы.",
        agent=reader
    )

    task2 = Task(
        description="Проанализировать полученные слова и выбрать наиболее релевантные для SEO.",
        expected_output="Список релевантных ключевых слов для SEO с кратким обоснованием выбора.",
        agent=analyst
    )

    task3 = Task(
        description="Сгруппировать выбранные ключевые слова по смыслу и сформировать структуру SEO-ядра сайта.",
        expected_output="Структурированное SEO-ядро: сгруппированные по тематикам ключевые слова для дальнейшего продвижения сайта.",
        agent=core_engineer
    )
    
    return [task1, task2, task3]

reader = Agent( 
    role="HTML Parser",
    goal="Parse HTML text from a given URL and extract words from the code",
    backstory=(
        "Этот агент получает HTML-страницу, извлекает HTML-код, "
        "парсит его и выбирает отдельные слова из содержимого страницы. "
        "Он может использовать BeautifulSoup для парсинга HTML и обработки текста."
    ),
    tools=[],
    verbose=True
)

analyst = Agent(
    role="SEO Analyst",
    goal="Анализировать полученные слова и выбирать наиболее релевантные для SEO",
    backstory=(
        "Этот агент анализирует полученные слова и выбирает наиболее релевантные для SEO. "
        "Он может использовать различные SEO-метрики и инструменты анализа. "
        "Агент оценивает частность, конкурентность и релевантность слов, чтобы предложить оптимальные ключевые слова для продвижения. "
        "Он также может использовать внешние сервисы для проверки позиций и анализа конкурентов."
    ),
    tools=[],
    verbose=True
)

core_engineer = Agent(
    role="SEO Core Developer",
    goal="Разрабатывать SEO-ядро",
    backstory=(
        "Этот агент отвечает за разработку и оптимизацию SEO-ядра сайта. "
        "Он анализирует собранные ключевые слова, группирует их по смыслу и формирует структуру SEO-ядра, "
        "учитывает поисковые запросы, конкуренцию и релевантность. "
        "Агент применяет лучшие практики SEO для создания эффективного семантического ядра, "
        "которое поможет сайту занять высокие позиции в поисковых системах."        
    ),
    tools=[],
    verbose=True
)
def main():
    """Основная функция программы"""
    try:
        # Получаем URL от пользователя
        target_url = get_user_input()
        
        print(f"\n🔍 Начинаем анализ сайта: {target_url}")
        print("⏳ Это может занять несколько минут...\n")
        
        # Создаем задачи с указанным URL
        tasks = create_tasks(target_url)
        
        # Создаем команду агентов
        crew = Crew(
            agents=[reader, analyst, core_engineer],
            tasks=tasks,
            verbose=True,
            process=Process.sequential
        )
        
        # Запускаем анализ
        result = crew.kickoff()
        
        print("\n" + "="*60)
        print("🎉 Анализ завершен успешно!")
        print("="*60)
        
        return result
        
    except KeyboardInterrupt:
        print("\n\n❌ Анализ прерван пользователем.")
        return None
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {e}")
        return None

if __name__ == "__main__":
    main()
