# Lucky_Number_AI
[Lucky Numbers](https://boardgamegeek.com/boardgame/118247/lucky-numbers) app using an AI. <br>
Developped during our fifth year of engineering classes at *ENSIM* school in Le Mans, France. <br>
Made by Gallien FRESNAIS, Zineb KABBAB, Lilian VALLEE

## Pre-requisites
- A webcam if you want to try the OCR
- [tesseract](https://github.com/tesseract-ocr/tesseract/releases/latest)
- [tessdata](https://github.com/tesseract-ocr/tessdata/releases/latest) (additional data for tesseract)
- [Python 3.8](https://wiki.python.org/moin/BeginnersGuide/Download)
- The following Python libraries
    - [python-opencv](https://pypi.org/project/opencv-python/)
    - [numpy](https://numpy.org/install/)
    - [pygame](https://www.pygame.org/wiki/GettingStarted)
    - [threading](https://docs.python.org/3/library/threading.html)
    - [Jupyter Notebook](https://jupyter.org/install)
    - [pytesseract](https://pypi.org/project/pytesseract/)
    - [easyOCR](https://pypi.org/project/easyocr/) (to test the associated Jupyter Notebook)
    - [Tensorflow](https://www.tensorflow.org/install)

*You can also use an IDE such as [Pycharm Community](https://www.jetbrains.com/help/pycharm/installation-guide.html)*

## How to use
- You can launch **OCR_tesseract.ipynb** with Jupyter Notebook to learn how OCR with tesseract works
- You can launch **OCR_easyOCR.ipynb** with Jupyter Notebook to learn how OCR with easyOCR works
- ~~You can launch **App/src/main.py** to use the main program with a GUI (and play the game!)~~ being reworked
- **App/src/webcam/main_webcam.py** to use your webcam and try some OCR
- To train the AI, check **App/src/JoueurIA.py**

## License
Released under the [MIT license](LICENSE)