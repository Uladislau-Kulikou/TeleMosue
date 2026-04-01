# TeleMouse
### Control your PC with gestures using a webcam

TeleMouse was created mainly for web surfing, but it’s flexible enough to be used in many other scenarios where a mouse is needed. It doesn’t aim to replace a keyboard entirely, but it already supports a range of built-in key combinations through gestures.

It’s especially useful in situations where using a physical mouse is inconvenient — for example, when you’re leaning back in your chair or lying in bed and want to switch a series on Netflix or scroll through YouTube. Or even when your hands are dirty (e.g. eating chips or chicken) and you don’t want to touch your devices. Most users will find their own use case.

---

## Features

- Hand tracking via webcam  
- Cursor movement using open hand  
- Click actions using gestures  
- Built-in keyboard shortcuts  
- Smooth and responsive control  
- Minimalistic Discord-like UI  

![](assets/Interface.png)
---

##  Tech Stack

- Python  
- OpenCV (`cv2`)  
- MediaPipe
- Tauri + Rust, JS, HTML, CSS

---

## Installation

Currently available only for **Windows** via MSI installer.

> UI source is not public.

---

##  Gestures

| Gesture | Action |
|--------|--------|
| ![](assets/palm.png) Right |  | Mouse moving mode |
| ![](assets/r_fist.png) Right | Scrolling mode (supports horizontal scroll). |
| ![](assets/l_fist.png) Left | Volume regulation. |
| ![](assets/lmb.png) Right | Left mouse button. Supports drag and double click. |
| ![](assets/rmb.png) Right | Right mouse button. Supports drag and double click. |
| ![](assets/back.png) Right | Emulates Alt+Left (Go to the previous page in browsers.) |
| ![](assets/f.png) Right | Emulates F key (Fullscreen on media players. Sometimes doesn't work). |
| ![](assets/horns.png) Right | Disables the reaction to all gestures except for itself. |
| ![](assets/ring.png) Right | Presses Alt+Tab allowing you to navigate to any opened program. |
| ![](assets/ring_l.png) Left | Emulates Ctrl+Tab allowing you to navigate to any opened website. |


---
