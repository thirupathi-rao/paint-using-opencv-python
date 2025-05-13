import cv2
import numpy as np
import time
canvas= np.full((1080,1080,3),255,dtype=np.uint8)

toolbar_height = 50
color_buttons = {
    'Black': (0, 0, 0),
    'Red': (0,0,255),
    'Green': (0,255,0),
    'Blue': (255,0,0),
    'Eraser': (200,200,200),
    'clear':(120,120,120),
    "save":(150,255,150)
}

shape_buttons = {
    'Circle': (200, 100, 220),
    'Rect': (200, 200, 100),
    'Ellipse': (100, 200, 200),
    'Line': (150, 150, 200)
}


# Current drawing color (default = black)
color = (b, g, r)=(0,0,0)
drawing = False
ix, iy = -1, -1
brush_size = None
mode = 'Draw'  # or 'Erase'
shape_mode = None
start_point = None
temp_can = None

def update_trackbars_from_color(bgr):
    b, g, r = bgr
    cv2.setTrackbarPos("blue", "Paint", b)
    cv2.setTrackbarPos("green", "Paint", g)
    cv2.setTrackbarPos("red", "Paint", r)


button_positions = {}
x_offset = 10
for name in color_buttons:
    button_positions[name] = (x_offset, x_offset + 60)
    x_offset += 70
for name in shape_buttons:
    button_positions[name] = (x_offset, x_offset + 60)
    x_offset += 70

# Mouse callback function
def draw(event, x, y, flags, param):
    global ix, iy, drawing, color, brush_size, mode, shape_mode, start_point

    if y < toolbar_height:
        if event == cv2.EVENT_LBUTTONDOWN:
            for name, (x1, x2) in button_positions.items():
                if x1 <= x <= x2:
                    if name in color_buttons:
                        selected_color = color_buttons[name]
                        if name == 'clear':
                            canvas[:] = 255
                        elif name == 'save':
                            img_save = canvas[toolbar_height:, :]
                            filename = f"dpaint_{int(time.time())}.png"
                            cv2.imwrite(filename, img_save)
                            print(f"Saved as {filename}")
                        elif name == 'Eraser':
                            mode = 'Erase'
                            shape_mode = None
                        else:
                            update_trackbars_from_color(selected_color)
                            mode = 'Draw'
                            shape_mode = None
                    elif name in shape_buttons:
                        shape_mode = name
                        mode = None

    else:
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = x, y
            start_point = (x, y)
            temp_can=canvas.copy()
        elif event == cv2.EVENT_MOUSEMOVE and drawing:
            if mode == 'Draw':
                cv2.line(canvas, (ix, iy), (x, y), color, brush_size)
                ix, iy = x, y
            elif mode == 'Erase':
                cv2.line(canvas, (ix, iy), (x, y), (255, 255, 255), brush_size)
                ix, iy = x, y
                display = canvas.copy() 
                # Show preview of shape while drawing
                if drawing and shape_mode and start_point:
                    temp_display = display.copy()
                    end_point = (x, y)
                    if shape_mode == 'Rect':
                        cv2.rectangle(temp_display, start_point, end_point, color, brush_size)
                    elif shape_mode == 'Circle':
                        radius = int(((end_point[0] - start_point[0])**2 + (end_point[1] - start_point[1])**2)**0.5)
                        cv2.circle(temp_display, start_point, radius, color, brush_size)
                    elif shape_mode == 'Ellipse':
                        center = ((start_point[0] + end_point[0]) // 2, (start_point[1] + end_point[1]) // 2)
                        axes = (abs(end_point[0] - start_point[0]) // 2, abs(end_point[1] - start_point[1]) // 2)
                        cv2.ellipse(temp_display, center, axes, 0, 0, 360, color, brush_size)
                    elif shape_mode == 'Line':
                        cv2.line(temp_display, start_point, end_point, color, brush_size)
                    display = temp_display
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            if shape_mode and start_point:
                end_point = (x, y)
                if shape_mode == 'Rect':
                    cv2.rectangle(canvas, start_point, end_point, color, brush_size)
                elif shape_mode == 'Circle':
                    radius = int(((end_point[0] - start_point[0])**2 + (end_point[1] - start_point[1])**2)**0.5)
                    cv2.circle(canvas, start_point, radius, color, brush_size)
                elif shape_mode == 'Ellipse':
                    center = ((start_point[0] + end_point[0]) // 2, (start_point[1] + end_point[1]) // 2)
                    axes = (abs(end_point[0] - start_point[0]) // 2, abs(end_point[1] - start_point[1]) // 2)
                    cv2.ellipse(canvas, center, axes, 0, 0, 360, color, brush_size)
                elif shape_mode == 'Line':
                    cv2.line(canvas, start_point, end_point, color, brush_size)

# Create window and bind mouse
cv2.namedWindow("Paint")
cv2.setMouseCallback("Paint", draw)


cv2.createTrackbar("blue","Paint",0,255,lambda x :None)
cv2.createTrackbar("green","Paint",0,255,lambda x :None)
cv2.createTrackbar("red","Paint",0,255,lambda x :None)
cv2.createTrackbar("thickness","Paint",0,10,lambda x :None)




while True:
    b=cv2.getTrackbarPos("blue","Paint")
    g=cv2.getTrackbarPos("green","Paint")
    r=cv2.getTrackbarPos("red","Paint")
    brush_size = cv2.getTrackbarPos('thickness', 'Paint')+1
    color = (b, g, r)
    display = canvas.copy()

    # Show preview of shape while drawing
    if drawing and shape_mode and start_point:
        temp_display = display.copy()
        end_point = (ix, iy)
        if shape_mode == 'Rect':
            cv2.rectangle(temp_display, start_point, end_point, color, brush_size)
        elif shape_mode == 'Circle':
            radius = int(((end_point[0] - start_point[0])**2 + (end_point[1] - start_point[1])**2)**0.5)
            cv2.circle(temp_display, start_point, radius, color, brush_size)
        elif shape_mode == 'Ellipse':
            center = ((start_point[0] + end_point[0]) // 2, (start_point[1] + end_point[1]) // 2)
            axes = (abs(end_point[0] - start_point[0]) // 2, abs(end_point[1] - start_point[1]) // 2)
            cv2.ellipse(temp_display, center, axes, 0, 0, 360, color, brush_size)
        elif shape_mode == 'Line':
            cv2.line(temp_display, start_point, end_point, color, brush_size)
        display = temp_display

    

    # Draw toolbar
    cv2.rectangle(display, (0, 0), (800, toolbar_height), (150, 150, 150), -1)
    x_pos = 10
    for name,col in color_buttons.items():
        cv2.rectangle(display, (x_pos, 5), (x_pos + 60, 45), col, -1)
        cv2.putText(display, name, (x_pos + 5, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 2)
        x_pos += 70
    for name,col in shape_buttons.items():
        cv2.rectangle(display, (x_pos, 5), (x_pos + 60, 45), col, -1)
        cv2.putText(display, name, (x_pos + 5, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 2)
        x_pos += 70

    cv2.putText(display,"Press 'q' to quit",(0,75),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1)

    cv2.imshow("Paint", display)
    if cv2.waitKey(10) == ord("q"):
        break
    elif cv2.waitKey(10) == ord('c'):  # 'c' to clear canvas
        canvas[75:,:] = 255

cv2.destroyAllWindows()
    
