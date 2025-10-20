>[!nexus_user] **User** - 27.05.2025 at 12:46
> 2.1.3. CUDA + cuDNN (NVIDIA)
>  • Версия должна совпадать с PyTorch
>  • Инсталляция через .run или .deb пакеты
>  • Проверка связки: nvcc --version, torch.cuda.is_available()
<!-- UID: c5c162ba-0cab-4399-afba-0620e5d0c01f -->




>[!nexus_agent] **Assistant** - 27.05.2025 at 12:46
> Вот полная развертка узла **2.1.3. CUDA + cuDNN (NVIDIA)** — 
> одного из важнейших шагов при сборке локальной AGI-среды, 
> в котором ты **синхронизируешь модель, драйвер и фреймворк**, 
> чтобы GPU стал **физическим ускорителем смысловой развёртки.**
> 
> ---
> 
> ## 🔧 2.1.3. CUDA + cuDNN (NVIDIA)
> 
> ---
> 
> ### 📌 КОНТЕКСТ
> 
> > PyTorch = мозг 
> > GPU-драйвер = тело 
> > **CUDA + cuDNN = нервная система AGI**
> 
> Без CUDA фреймворк не сможет передавать данные с CPU на GPU, 
> а без cuDNN — не будет ускорения сверточных операций внутри модели.
> 
> ⚠️ **Ошибки в версиях между ними — причина 80% сбоев запуска.**
> 
> ---
> 
> ### 🎯 ЦЕЛЬ
> 
> 🔹 Установить версию CUDA + cuDNN, 
> 🔹 Совместимую с текущей версией PyTorch, 
> 🔹 Так, чтобы `torch.cuda.is_available()` → `True`
> 
> ---
> 
> ### 🔢 ШАГ 1. ВЫБОР ВЕРСИЙ
> 
> #### 📘 Где посмотреть совместимость:
> https://pytorch.org/get-started/previous-versions/
> 
> Пример:
> 
> | PyTorch Версия | CUDA Версия |
> |----------------|-------------|
> | 2.1.0 | 12.1 |
> | 2.0.1 | 11.8 |
> | 1.13.1 | 11.7 |
> 
> ---
> 
> ### 📦 ШАГ 2. УСТАНОВКА CUDA
> 
> #### ✅ Способ 1: `.deb` (для Ubuntu)
> 
> ```bash
> wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-repo-ubuntu2204_12.1.105-1_amd64.deb
> sudo dpkg -i cuda-repo-ubuntu2204_12.1.105-1_amd64.deb
> sudo apt-key add /var/cuda-repo-ubuntu2204*/7fa2af80.pub
> sudo apt update
> sudo apt install cuda
> ```
> 
> #### ✅ Способ 2: `.run` (ручная установка)
> 
> ```bash
> chmod +x cuda_12.1.105_*.run
> sudo ./cuda_12.1.105_*.run
> ```
> 
> ➡️ Указать: **не устанавливать драйвер**, если он уже есть (`nvidia-smi` работает)
> 
> ---
> 
> ### 📥 УСТАНОВКА cuDNN
> 
> 1. Зарегистрируйся на [NVIDIA cuDNN](https://developer.nvidia.com/cudnn)
> 2. Скачай `cudnn-linux-x86_64-x.x.x_cuda12-x_archive.tar.xz`
> 3. Распакуй и скопируй вручную:
> ```bash
> sudo cp include/* /usr/local/cuda/include/
> sudo cp lib64/* /usr/local/cuda/lib64/
> ```
> 
> ---
> 
> ### 🧪 ШАГ 3. ПРОВЕРКА СВЯЗКИ
> 
> #### ✅ Проверка CUDA:
> ```bash
> nvcc --version
> ```
> 
> Ожидаемый вывод:
> ```text
> Cuda compilation tools, release 12.1, V12.1.105
> ```
> 
> #### ✅ Проверка доступности из PyTorch:
> ```python
> import torch
> print(torch.cuda.is_available())
> print(torch.cuda.get_device_name(0))
> ```
> 
> Ожидаемый вывод:
> ```text
> True
> NVIDIA GeForce RTX 3080
> ```
> 
> ---
> 
> ### 📦 ПРОБЛЕМЫ И РЕШЕНИЯ
> 
> | Проблема | Причина | Решение |
> |-------------------------------------|------------------------------------------|----------------------------------|
> | `torch.cuda.is_available() → False`| Несовпадение версий CUDA / PyTorch | Переустановить PyTorch с нужной версией |
> | `nvcc` not found | CUDA не в `$PATH` | Добавить `export PATH=/usr/local/cuda/bin:$PATH` |
> | Ошибка при установке cuDNN | Недостаточно прав | Использовать `sudo` и `tar`-метод |
> 
> ---
> 
> ### ✅ ВЫВОД
> 
> > **CUDA + cuDNN — это не "библиотеки", 
> > а мост между мышлением и материей.**
> 
> Когда связка правильна:
> - AGI разворачивается быстро 
> - Модель отвечает без лагов 
> - Ты можешь запускать RECURSIA, SIMPLICIO, ERROR-FOLD без задержки
> 
> ---
> 
> Хочешь:
> - перейти к `2.1.4` — *Установка PyTorch с поддержкой CUDA* 
> - или собрать `install_cuda.sh` под твой дистрибутив?
> 
> Ты решаешь.
<!-- UID: e1453245-0789-4688-b99e-d129e0221daf -->