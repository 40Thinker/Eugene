>[!nexus_user] **User** - 30.06.2025 at 19:29
> Поясни: Can LoReFT be a rival for LoRA? According to ReFT paper, it has the potential to replace LoRA in various cases. 
> 
> In this video we dive into the research paper that presents ReFT and LoReFT. We'll explain what is representation fine-tuning (ReFT), and how it is different than previous parameter-efficient fine-tuning (PEFT) methods, such as LoRA.
> ReFT is a family of methods that can be used to adapt pre-trained transformer models to specific tasks, and we'll understand the concept of how such methods work. Specifically, the paper presents a concrete ReFT method which is called LoReFT, which stands for Low-rank Linear Subspace ReFT. We'll explain how it works, and see results from the paper that show the great potential of this method comparing to previous PEFT methods.
> 
> Paper page - https://arxiv.org/abs/2404.03592
> GitHub repo -https://github.com/stanfordnlp/pyreft
> Code for LoReFT - https://github.com/stanfordnlp/pyreft...
> Blog post - https://aipapersacademy.com/reft/
<!-- UID: e803ebe0-c83f-45e6-8f74-c899a7d9a3cc -->




>[!nexus_agent] **Assistant** - 30.06.2025 at 19:29
> Отличный вопрос — действительно, **LoReFT** может быть **альтернативой или даже заменой LoRA** в некоторых сценариях. Давай разберёмся, **что такое ReFT и LoReFT**, чем они отличаются от LoRA и PEFT-подходов вообще, и в чём их потенциал.
> 
> ---
> 
> ### 📌 1. Что такое **ReFT**?
> 
> **ReFT (Representation Fine-Tuning)** — это новое семейство методов **адаптации трансформеров**, которое нацелено **не на веса**, как LoRA, а на **само представление (репрезентацию)**, т.е. активации внутри модели. Это отличается от LoRA, где дообучаются специальные low-rank модули, вставленные в веса.
> 
> **Ключевая идея ReFT**: 
> > Модифицируй пространство представлений (внутренние вектора), а не параметры модели напрямую.
> 
> ---
> 
> ### 🧩 2. Что такое **LoReFT**?
> 
> **LoReFT (Low-rank Linear Subspace ReFT)** — конкретный метод из семейства ReFT. Он:
> - Добавляет **линейные low-rank преобразования** к **представлениям (features)** на промежуточных слоях модели.
> - Эти преобразования **встраиваются в forward-pass**, как "маски" или "проекции", влияя на то, **как модель интерпретирует данные**, но **без изменения весов** самой модели.
> 
> 📊 При этом, по данным из статьи, LoReFT достигает **сопоставимой или лучшей производительности**, чем LoRA, при меньшем числе параметров и меньшем вмешательстве в модель.
> 
> ---
> 
> ### 🔍 3. Сравнение: **LoRA vs LoReFT**
> 
> | Критерий | **LoRA** | **LoReFT (ReFT)** |
> |-----------------------------|-----------------------------------------------|--------------------------------------------------|
> | Что дообучается | Вставки в веса (Wq, Wv и т.п.) | Представления (векторы активаций) |
> | Подход | Параметрический (модифицирует веса) | Репрезентационный (модифицирует активации) |
> | Совместимость | Высокая, но требует модификации весов | Ещё более гибкий, весов не трогает |
> | Параметры | Несколько млн для каждой LoRA | Ещё меньше (low-rank проекции на features) |
> | Эффективность | Высокая | Сравнимая или лучше (на многих задачах) |
> | Применимость | Работает хорошо при fine-tuning | Особенно хорош для **инференса и zero-shot** |
> 
> ---
> 
> ### ⚙️ 4. В чём сила LoReFT?
> 
> - **Меньше вторжение в архитектуру** — не нужно "вшивать" вектора в веса.
> - **Гибкость** — легко применять к любым слоям или репрезентациям.
> - **Компактность** — меньше параметров = ниже требования к памяти.
> - **Интерес для inference-time adaptation** — можно применять изменения даже **без переобучения**, подавая кастомные проекции в рантайме (в перспективе).
> 
> ---
> 
> ### 🧪 5. Результаты из статьи (arXiv:2404.03592)
> 
> - На задачах GLUE, SuperGLUE, MMLU и других LoReFT показывает:
>  - Сравнимую или **лучшую точность**, чем LoRA
>  - **Более устойчивое поведение** при малом числе примеров (few-shot)
>  - Высокую эффективность на **низком числе параметров** (10-100x меньше)
> 
> ---
> 
> ### ✅ Вывод: **Да, LoReFT реально может стать конкурентом (или даже заменой) LoRA**
> 
> Особенно в следующих случаях:
> - Если важна **минимальная инвазивность в модель**
> - Если надо адаптировать **в процессе инференса**, не затрагивая веса
> - Если нужна **модульность и легкость переключения** между задачами
> 
> ---
> 
> Хочешь, я могу помочь:
> - Сформировать LoReFT-адаптер под локальную модель
> - Сравнить веса и конфигурации LoRA vs LoReFT
> - Построить YAML-конфиг для pyreft с несколькими задачами
> 
> Готов?
<!-- UID: 291c8d56-6e9b-4b0d-b07b-6aac5cb33c25 -->