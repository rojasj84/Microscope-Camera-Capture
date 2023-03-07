import tkinter as tk
import cv2

from threading import Thread
from PIL import ImageTk, Image, ImageFont, ImageDraw

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Microscope Camera Image Saver')
        self.geometry('1200x560')
        self.configure(bg=win_color)

        camera_display_frame = DisplayCamera()       

class DisplayCamera(tk.Frame):
    def __init__(self):
        super().__init__()
        self.config(background=win_color)
        self.place(x=10,y=10,height = 540,width = 1190)

        self.capture_number = 1
        
        
        # Label to display camera image
        self.image_display_label = tk.Label(self, text="", relief=tk.RIDGE)
        self.image_display_label.place(x=0,y=0)        

        # Button to capture image 
        self.capture_image_button = tk.Button(self, text = "Capture Image", command=self.capture_image)
        self.capture_image_button.place(x=1000,y=10,height = 50,width = 150)

        # Button to update scale information
        # self.update_scale_button = tk.Button(self, text = "Update Scale")
        # self.update_scale_button.place(x=1000,y=60,height = 50,width = 150)

        self.scale_size_label = tk.Label(self, text = "Scale Size in Microns", bg = win_color)
        self.scale_size_label.place(x=1000,y=90,height = 20,width = 150)

        # Texbox for the scale
        self.update_scale_text = tk.Text(self)
        self.update_scale_text.place(x = 1000, y = 110, height = 30, width = 150)
        self.update_scale_text.insert(tk.INSERT, "100")

        
        show_camera_thread = Thread(target=self.show_camera)
        show_camera_thread.start()

    def show_camera(self):
        # get frame
        ret, frame = cap.read()
        
        if ret:
            # cv2 uses `BGR` but `GUI` needs `RGB`
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # frame = cv2.flip(frame, 1) #Mirror the image

            # convert to PIL image
            img = Image.fromarray(frame)

            scale_length = 300
        

            g_width, g_height = img.size
            # print(g_width)
            line_tuple_1 = [(g_width-scale_length,g_height-20),(g_width-10,g_height-20)]
            line_tuple_2 = [(g_width-10,g_height-30),(g_width-10,g_height-10)]
            line_tuple_3 = [(g_width-scale_length,g_height-30),(g_width-scale_length,g_height-10)]
            ImageDraw.Draw(img).line(line_tuple_1,fill="Yellow", width=5)
            ImageDraw.Draw(img).line(line_tuple_2,fill="Yellow", width=5)
            ImageDraw.Draw(img).line(line_tuple_3,fill="Yellow", width=5)
            
            font = ImageFont.truetype("font/arial.ttf", size=48);
            text_val = int(self.update_scale_text.get("1.0","end"))
            ImageDraw.Draw(img).text((g_width-200,g_height-75), text = str(text_val) + "μm", fill="Yellow", font=font)

            newsize = (960,540)
            image_to_display = img.resize(newsize)

            # convert to Tkinter image
            converted_to_tkinter = ImageTk.PhotoImage(image=image_to_display)

            # solution for bug in `PhotoImage`
            self.image_display_label.photo = converted_to_tkinter
            self.image_display_label.configure(image=converted_to_tkinter)            
            

        # run again after 20ms (0.02s)
        self.after(10, self.show_camera)

    def capture_image(self):
            
            #Get input from camera
            self.capture_camera_input()
            
            #Save image to file
            self.save_image_to_file()

    def capture_camera_input(self):
        # get frame
        ret, frame = cap.read()

        if ret:
            # cv2 uses `BGR` but `GUI` needs `RGB`
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # convert to PIL image
            self.img = Image.fromarray(frame)

            scale_length = 300
        

            g_width, g_height = self.img.size
            # print(g_width)
            line_tuple_1 = [(g_width-scale_length,g_height-20),(g_width-10,g_height-20)]
            line_tuple_2 = [(g_width-10,g_height-30),(g_width-10,g_height-10)]
            line_tuple_3 = [(g_width-scale_length,g_height-30),(g_width-scale_length,g_height-10)]
            ImageDraw.Draw(self.img).line(line_tuple_1,fill="Yellow", width=5)
            ImageDraw.Draw(self.img).line(line_tuple_2,fill="Yellow", width=5)
            ImageDraw.Draw(self.img).line(line_tuple_3,fill="Yellow", width=5)
            
            font = ImageFont.truetype("font/arial.ttf", size=48);
            text_val = int(self.update_scale_text.get("1.0","end"))
            ImageDraw.Draw(self.img).text((g_width-200,g_height-75), text = str(text_val) + "μm", fill="Yellow", font=font)


    def save_image_to_file(self):
        self.img.save("capture-" + str(self.capture_number)+ ".tiff")
        self.capture_number = self.capture_number + 1



if __name__ == "__main__":
    win_color = "light gray"
    cap = cv2.VideoCapture(0)
    cap.set(3,1920)     #horizontal pixels
    cap.set(4,1080)     #vertical pixels
    cap.set(5, 15)      #Camera frame rate

    
    window = MainWindow()
    window.mainloop()