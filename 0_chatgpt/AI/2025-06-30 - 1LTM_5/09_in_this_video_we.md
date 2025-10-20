>[!nexus_user] **User** - 30.06.2025 at 19:08
> In this video, we dive into a recent research paper by Google, titled: "Mixture of Nested Experts: Adaptive Processing of Visual Tokens". While standard Mixture of Experts (MoE) is successfully applied in LLMs, and also in computer vision, to increase computational cost without a proportional increase to model size, it comes with a large memory footprint. The Mixture of Nested Experts (MoNE) which we review in this video tackles that drawback. Mixture of Nested Experts is built on top of the Vision Transformer (ViT) architecture, and offers a dramatic performance improvement, by leveraging the fact that images naturally contain a large amount of information redundancy. So, while ViT (also with MoE), allocates its full compute power for each token, Mixture of Nested Experts (MoNE) learns to allocate compute power to tokens based on their importance.
> Watch the video to learn more.
> 
> Paper page - https://arxiv.org/abs/2407.19985
> Mixture of Experts (MoE) Video - Introduction to Mixture-of-Experts | Origi...
> Post -  https://aipapersacademy.com/mixture-o...
> Original Mixture-of-Experts paper review - https://aipapersacademy.com/mixture-o...
<!-- UID: f5419b05-9583-450a-b527-b08bf942e527 -->




>[!nexus_agent] **Assistant** - 30.06.2025 at 19:08
> The video you're referring to discusses a recent research paper by Google titled **"Mixture of Nested Experts: Adaptive Processing of Visual Tokens"**. Here's a summary of the key points:
> 
> ### Overview of **Mixture of Experts (MoE)**:
> - MoE is a technique used in large language models (LLMs) and computer vision to improve model efficiency. 
> - **Standard MoE** selectively activates different subsets of the model’s parameters (or "experts") during processing, which allows the model to scale up computational power without increasing the number of parameters.
> - However, the trade-off is a **large memory footprint**, which can be a limiting factor.
> 
> ### Introduction to **Mixture of Nested Experts (MoNE)**:
> - **MoNE** is an improvement upon MoE, designed to tackle the **memory footprint issue** while maintaining or even improving performance.
> - Built on the **Vision Transformer (ViT)** architecture, MoNE **dynamically allocates computational resources** to tokens based on their importance, which helps reduce unnecessary computation and memory usage.
> - In standard ViT (and MoE), **each token** gets the full computational power, even if some tokens may not be as important. In MoNE, the model can learn to focus computational resources on the most significant tokens, significantly **increasing performance**.
> 
> ### Benefits of **Mixture of Nested Experts**:
> - MoNE leverages the natural **redundancy in images**, where much of the information is repetitive, allowing the model to allocate resources more efficiently.
> - This leads to a **dramatic performance improvement** while **reducing computational cost** compared to traditional MoE approaches.
> 
> ### Further Reading:
> - **Paper**: [Mixture of Nested Experts: Adaptive Processing of Visual Tokens](https://arxiv.org/abs/2407.19985)
> - **Original MoE Paper Review**: [Mixture-of-Experts Video](https://aipapersacademy.com/mixture-o...)
> 
> This technique presents an innovative step forward in optimizing vision models like ViT, balancing efficiency and computational load. The core idea is to **reduce the memory footprint** without compromising on performance, especially in the context of visual data, where redundant information is abundant.
<!-- UID: c9219e17-8eb4-48c0-890a-3e01ef5dcb74 -->