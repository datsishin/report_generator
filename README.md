# 🧪 Test Report Generator

Сервис на FastAPI для генерации отчётов о тестировании в формате PDF.  
Предназначен для интеграции с CI/CD пайплайнами или ручного запуска.

## 🚀 Возможности

- Приём JSON и файла с результатами тестов
- Генерация отчёта в PDF
- Асинхронная обработка запросов
- REST API
- Поддержка запуска через Docker Compose

## 📦 Стек технологий

- Python 3.13+
- FastAPI
- WeasyPrint (для генерации PDF)
- Jinja2 (шаблоны отчётов)
- Docker + Docker Compose

## 🛠️ Установка и запуск

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/your-org/test-report-generator.git
cd test-report-generator
```

```bash
docker-compose up --build
```