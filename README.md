# paint-using-opencv-python
# 🎨 OpenCV Paint Application

This is a **Python-based paint/drawing application** built using **OpenCV**, offering an intuitive interface to draw freehand, shapes, and more using your mouse — all inside a resizable canvas.

## 🖼️ Features

- 🖌️ Freehand Drawing with adjustable brush thickness and custom color
- 🔲 Shape Drawing: Rectangle, Circle, Ellipse, Line
- 🧽 Eraser Tool
- 🎨 Custom Color Picker via trackbars (BGR values)
- 💾 Save drawings locally as `.png` files
- 🧼 Clear canvas with a click
- 🖱️ Interactive toolbar for quick tool and color switching

## 📸 UI Overview

- **Top Toolbar** includes:
  - Color buttons: Black, Red, Green, Blue
  - Utility buttons: Eraser, Clear, Save
  - Shape tools: Rectangle, Circle, Ellipse, Line
- **Bottom Area** is your drawing canvas
- **Trackbars** let you fine-tune:
  - Brush color (B, G, R)
  - Brush thickness
Then draw using your mouse! ✏️

**Controls**
🖱️ Left Click – Draw shapes or freehand

💾 Save – Saves canvas excluding toolbar

🧼 Clear – Clears drawing area

❌ q – Quit application

🔁 c – Clear canvas (alternate

## 🚀 How to Run

```bash
pip install opencv-python numpy
python paint.py

