# Reddit Post Title Classification using Machine Learning

## Project Overview
This project focuses on classifying Reddit post titles into multiple categories using supervised machine learning techniques.  
The task is formulated as a **multi-class text classification problem**, where each Reddit post title is assigned to one of the following categories:

- Technology  
- Science  
- Sports  
- Books  
- Fitness  

The project was developed as part of the **Learning from Data** course and follows a complete end-to-end machine learning pipeline, from data preprocessing to model evaluation and analysis.

---

## Dataset
- **Source:** Reddit (scraped using Reddit API / web scraping)
- **Data Type:** Text (post titles)
- **Total Samples:** 4,518
- **Classes:** 5 (Technology, Science, Sports, Books, Fitness)
- **Labels:** Balanced distribution with minor variations
- **Missing Values:** None

Each sample consists of:
- `text` – the Reddit post title  
- `label` – the category of the post  

---

## Problem Definition
This project addresses a **supervised multi-class classification problem**, where the goal is to predict the category of a Reddit post title based solely on its textual content.

---

## Project Structure
reddit-text-classification/
│
├── data/
│ ├── raw/
│ └── processed/
│
├── notebooks/
│ └── 01_full_pipeline.ipynb
│
├── README.md
├── requirements.txt
└── .gitignore

yaml
Copy code

The **entire machine learning pipeline** is implemented in a single Jupyter notebook for clarity and reproducibility.

---

## Text Preprocessing
Text preprocessing is performed primarily through feature extraction methods and includes:

- Lowercasing
- Tokenization
- Stopword removal
- Removal of non-alphabetic characters

Given the short nature of Reddit titles, additional linguistic normalization (e.g., stemming or lemmatization) was not required.

---

## Feature Engineering
The following feature representations were implemented:

### 1. Bag-of-Words (BoW)
- Word frequency-based representation
- Stopwords removed
- Feature dimensionality limited to reduce overfitting

### 2. TF-IDF
- Term Frequency–Inverse Document Frequency
- Captures word importance across documents
- Primary feature representation used for modeling

### 3. Custom Domain-Based Features
Additional handcrafted features were extracted based on domain knowledge:
- Title length
- Number of digits in the title
- Presence of question marks (`?`)
- Presence of exclamation marks (`!`)

These features help capture stylistic patterns across different categories.

---

## Models Implemented
The project compares **four different models**, satisfying both traditional machine learning and deep learning requirements.

### Traditional Machine Learning
1. **Logistic Regression**
2. **Multinomial Naive Bayes**
3. **Linear Support Vector Machine (SVM)**

### Deep Learning
4. **Multi-Layer Perceptron (MLP)**

---

## Training Strategy
- **Train/Test Split:** 80% training, 20% testing (stratified)
- **Cross-Validation:** 5-fold cross-validation (Linear SVM)
- **Hyperparameter Tuning:** Grid search for SVM regularization parameter `C`

---

## Evaluation Metrics
The following metrics were used for model evaluation:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix
- Learning Curves

---

## Results Summary

| Model | Accuracy |
|------|----------|
| Logistic Regression | 0.887 |
| Multinomial Naive Bayes | 0.884 |
| Linear SVM | 0.903 |
| **MLP (Neural Network)** | **0.908** |

The **MLP** achieved the highest accuracy, while Linear SVM performed competitively and demonstrated strong generalization.

---

## Bias–Variance & Overfitting Analysis
- Learning curves show convergence between training and validation accuracy.
- Cross-validation results indicate stable performance.
- Overfitting prevention techniques used:
  - L2 regularization
  - Feature dimensionality control
  - Validation-based model selection
  - Limited training iterations for neural networks

Overall, the models exhibit good generalization with no significant overfitting.

---

## Technologies Used
- Python
- Jupyter Notebook
- scikit-learn
- pandas
- numpy
- matplotlib
- seaborn

---

## How to Run the Project
1. Clone the repository:
   ```bash
   git clone <repository-url>
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Open the notebook:

bash
Copy code
jupyter notebook notebooks/01_full_pipeline.ipynb
Run all cells from top to bottom.

Conclusion
This project demonstrates the effectiveness of both traditional machine learning and deep learning approaches for multi-class text classification. The results show that TF-IDF features combined with linear models and neural networks provide strong performance on short-text classification tasks such as Reddit post titles.

Author
[Your Name]
Learning from Data – University Project