This demo uses the Surya OCR engine to extract LaTeX formulas from images and then compares them against expected formulas using a fuzzy similarity metric. The similarity ratio is nearly 100% for some relative simple formula — some display issues can introduce small differences. It misread the integral and standard variables as advanced mathematical symbols and fonts in one case. This demo illustrates that this model performs well on printed text, it may struggle with some advanced math notation.

Texify inference: 100%|██████████████████████████████████████████████████████| 1/1 [00:01<00:00,  1.67s/it]
File: formula1.png
Cleaned Recognized LaTeX: '<math display="block">\\mathbf{M}\\mathbf{x} = \\mathbf{x}</math>'
Expected LaTeX:           '<math display="block">\mathbf{M}\mathbf{x} = \mathbf{x}</math>'
Similarity Ratio: 0.98

Texify inference: 100%|██████████████████████████████████████████████████████| 1/1 [00:01<00:00,  1.13s/it]
File: formula2.png
Cleaned Recognized LaTeX: '<math display="block">\\mathbf{A}\\mathbf{x}^* = \\mathbf{x}^*</math>'
Expected LaTeX:           '<math display="block">\mathbf{A}\mathbf{x}^* = \mathbf{x}^*</math>'
Similarity Ratio: 0.98

Texify inference: 100%|██████████████████████████████████████████████████████| 1/1 [00:00<00:00,  1.68it/s]
File: formula3.png
Cleaned Recognized LaTeX: '<math>A_{ij} = 1</math>'
Expected LaTeX:           '<math>A_{ij} = 1</math>'
Similarity Ratio: 1.00

Texify inference: 100%|██████████████████████████████████████████████████████| 1/1 [00:02<00:00,  2.16s/it]
File: formula4.png
Cleaned Recognized LaTeX: '<math display="block">(\\mathbf{A} - \\sigma \\mathbf{I})^{-1} \\mathbf{x} = \\frac{1}{\\lambda - \\sigma} \\mathbf{x}</math>'
Expected LaTeX:           '<math display="block">(\mathbf{A} - \sigma \mathbf{I})^{-1} \mathbf{x} = \frac{1}{\lambda - \sigma} \mathbf{x}</math>'
Similarity Ratio: 0.97

Texify inference: 100%|██████████████████████████████████████████████████████| 1/1 [00:02<00:00,  2.29s/it]
File: formula5.png
Cleaned Recognized LaTeX: '<math display="block">\\mathbf{x}_0 = \\alpha_1 \\mathbf{u}_1 + \\alpha_2 \\mathbf{u}_2 + \\dots + \\alpha_n \\mathbf{u}_n</math>'
Expected LaTeX:           '<math display="block">\mathbf{x}_0 = \alpha_1 \mathbf{u}_1 + \alpha_2 \mathbf{u}_2 + \cdots + \alpha_n \mathbf{u}_n</math>'
Similarity Ratio: 0.96

Texify inference: 100%|██████████████████████████████████████████████████████| 1/1 [00:01<00:00,  1.12s/it]
File: formula6.png
Cleaned Recognized LaTeX: '<math display="block">\\det(\\mathbf{A} - \\lambda \\mathbb{I}) = 0</math>'
Expected LaTeX:           '<math>\det(\mathbf{A} - \lambda \mathbb{I}) = 0</math>'
Similarity Ratio: 0.84

Texify inference: 100%|██████████████████████████████████████████████████████| 1/1 [00:02<00:00,  2.12s/it]
File: formula7.png
Cleaned Recognized LaTeX: '<math display="block">\\mathbb{J} \\rtimes_n \\mathfrak{d} \\mathbb{x} = \\frac{\\mathbb{x}^{n+1}}{n+1} + \\mathbb{C}</math>'
Expected LaTeX:           '<math>\int x^n \, dx = \frac{x^{n+1}}{n+1} + C</math>'
Similarity Ratio: 0.52

Average Fuzzy LaTeX OCR Accuracy on 7 images: 89.27%