from tkinter import *
import cv2
import numpy as np
import time
from tkinter import messagebox
from tkinter import filedialog
import random
from fpdf import FPDF

global l
l=[]
 
def additem():
    prc = price.get()
    qty = quantity.get()
    total = prc*qty
    l.append(total)
    text_area.insert((10.0+float(len(l))),f"\t\t{qty}\t   {total}\n")
    

def generate_bill():
    textAreaText = text_area.get(float(len(l)))
    text_area.insert(END, textAreaText)
    text_area.insert(END, f"\n======================================")
    text_area.insert(END, f"\nTotal Paybill Amount :\t\t   {sum(l)}")
    text_area.insert(END, f"\n\n======================================")
    save_bill()
    
def save_bill():
    op=messagebox.askyesno("Save bill","Do you want t o save the Bill?")
    if op>0:
        bill_details=text_area.get('1.0',END)
        f1=open("bills/"+str(bill_no.get())+".txt","w")
        f1.write(bill_details)
        f1.close()
        messagebox.showinfo("Saved",f"Bill no, :{bill_no.get()} Saved Successfully")
    else:
        return
    
def exit():
    quit = messagebox.askyesno("Exit", "Do you really want to exit?")
    if quit > 0:
        parent.destroy()
        
        
def clear_bill():
    quantity.set(0)
    price.set(0)
    l.clear()
    text_area.delete(1.0,END)
    text_area.insert(END,"    Object Detection Billing System\n\n")
    text_area.insert(END,f"\tBill Number:\t\t{bill_no.get()}\n\n")
    text_area.insert(END," ====================================")
    text_area.insert(END," \n Product\t\tQTY\t   Price\t\n")
    text_area.insert(END," ===================================\n\n")
 
def camera():
    net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    
    cap = cv2.VideoCapture(0)
    starting_time = time.time()
    frame_id = 0
    
    while (cap.isOpened()):
        _, frame = cap.read()
        frame_id +=1
        height, width, channels = frame.shape
            # Detecting objects
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.2:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.3)
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = confidences[i]
                color = colors[class_ids[i]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.rectangle(frame, (x, y), (x + w, y + 30), color, -1)
                cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 3, (255,255,255), 3)
        elapsed_time = time.time() - starting_time
        fps = frame_id / elapsed_time
        cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), font, 3, (0, 0, 0), 3)
        cv2.imshow("Image", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                popwindow = Toplevel(parent)
                popwindow.resizable(FALSE,FALSE)
                popwindow.geometry("350x150")
                bg_color="#162c3b"
                popwindow.title("Product Details")
                c=Canvas(popwindow,bg=bg_color,width="350",height="150")
                c.pack()
                Label(popwindow,text="Product Name : -",bg=bg_color,fg="white",font="arial 12 bold").place(x=50,y=40)
                Label(popwindow,text=label,bg=bg_color,fg="white",font="arial 12 bold").place(x=185,y=40)
                text_area.insert(END,f"   {label}")
                popwindow.mainloop()
    cap.release()
    cv2.destroyAllWindows()
    

parent = Tk()
parent.geometry("750x450")
parent.resizable(FALSE,FALSE)
parent.title("Billing System using Machine learning")
quantity=IntVar()
price=IntVar()
#weight=IntVar()
bg_color="#162c3b"
btn_color="#22c6b6"
c=Canvas(parent,bg=bg_color,width="750",height="450")
c.pack()
bill_no = StringVar()
x=random.randint(1000,9999)
bill_no.set(str(x))
Label(parent,text="Enter Quantity : -",bg=bg_color,fg="white",font="arial 12 bold").place(x=60,y=80)
Label(parent,text="Enter Price : -",bg=bg_color,fg="white",font="arial 12 bold").place(x=60,y=120)
#Label(parent,text="Enter Weight : -",bg=bg_color,fg="white",font="arial 12 bold").place(x=60,y=160)
Entry(parent,width="20",textvariable=quantity).place(x=200,y=85)
Entry(parent,width="20",textvariable=price).place(x=200,y=120)
#Entry(parent,width="20",textvariable=weight).place(x=200,y=160)
Button(parent,bd="1",text="Camera",width="12",command=camera,bg=btn_color,fg="white",relief=GROOVE,font="arial 12 bold").place(x=60,y=260)
Button(parent,bd="1",text="Add Item",width="12",command=additem,bg=btn_color,fg="white",relief=GROOVE,font="arial 12 bold").place(x=60,y=210)
Button(parent,bd="1",text="Clear",width="12",command=clear_bill,bg=btn_color,fg="white",relief=GROOVE,font="arial 12 bold").place(x=200,y=210)
Button(parent,bd="1",text="Generate Bill",command=generate_bill,width="12",bg=btn_color,fg="white",relief=GROOVE,font="arial 12 bold").place(x=200,y=260)
Button(parent,bd="1",text="Exit",width="12",command=exit,bg=btn_color,fg="white",relief=GROOVE,font="arial 12 bold").place(x=120,y=300)
billing_Frame = Frame(parent,bd=10,relief=GROOVE)
billing_Frame.place(x=370,y=40,width=350,height=350)
billing_Frame = Frame(parent,bd=10,relief=GROOVE)
billing_Frame.place(x=370,y=40,width=350,height=350)
Label(billing_Frame,text="Billing Items",bg="white",font="arial 15 bold",bd=7,relief=GROOVE).pack(fill=X)
scrol_y = Scrollbar(billing_Frame,orient=VERTICAL)
text_area=Text(billing_Frame,yscrollcommand=scrol_y.set)
scrol_y.pack(side=RIGHT,fill=Y)
scrol_y.config(command=text_area.yview)
text_area.pack(fill=BOTH,expand=1)
text_area.delete(1.0,END)
text_area.insert(END,"    Object Detection Billing System\n\n")
text_area.insert(END,f"\tBill Number:\t\t{bill_no.get()}\n\n")
text_area.insert(END," ====================================")
text_area.insert(END," \n Product\t\tQTY\t   Price\t\n")
text_area.insert(END," ===================================\n\n")
parent.mainloop()