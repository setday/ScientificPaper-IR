# ScientificPaper-IR

## 📖 Описание

**ScientificPaper-IR** — это система для извлечения ключевой информации из pdf-документов научного содержания. Кроме стандартного извлечения таблиц, система также будет поддерживать извлечение информации из графиков и схем, а также связанных ресурсов.
Система будет работать без внешних серверов, что обеспечит её конфиденциальность.

## ⭐️ Цели проекта

Целью проекта является создание системы, которая:

- Помогает в извлечении основной информации из статей.
- Повышает эффективность анализа статей.
- Эффективно работает на локальных мощностях.

## ⚙️ Функциональные возможности

- Извлечении таблиц с помощью методов машинного зрения.
- Извлечение основной информации из статьи (генерация `abstract`, поиск ключевых данных, поиск связанных данных).
- Извлечение дат, названий и прочей информации из графиков и рисунков.

## 🖥️ Стек технологий

### Backend
- **Python** для разработки основного функционала.
- **PyTorch** для создания и обучения моделей машинного обучения.
- **LLaMA v3.2** для извлечения основной информации из текста.
- **gpt-4o-mini** для анализа изображений и извлечение данных из них.

### Frontend
- **Angular** в качестве основы **Tauri**.
- **Tauri** для создания кросс платформенного интерфейса.

## 🔧 Структура проекта

### Backend
- **`backend/extract_pdf_info.py`** — скрипт для извлечения информации из pdf.
- **`backend/run_server.py`** — скрипт для запуска сервера, для работы с `extract_pdf_info.py`.
- **`requirements.txt`** — список зависимостей бэкенд части проекта.
- **`models/`** — папка моделями.

### Frontend
- **`package.json`** и **`package-lock.json`** — список зависимостей фронтенд части проекта.

### Общее
- **`README.md`** — файл с информацией о проекте.
- **`CONTRIBUTING.md`** — файл с информацией о внесении внешних изменений в проект.
- **`LICENSE`** — файл с информацией о распространении проекта.

## ⬇️ Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/setday/ScientificPaper-IR.git
2. Перейдите в каталог проекта:
    ```bash
    cd ScientificPaper-IR
3. Установите зависимости:
    ```bash
    pip install -r requirements.txt

## Дополнительная информация

- Данный репозиторий не является основным для разработки. Здесь находятся лишь release-версии проекта. 

- На данный момент frontend часть не является основополагающей и заморожена до окончания разработки backend части.
