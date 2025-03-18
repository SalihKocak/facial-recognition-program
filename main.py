import os
import cv2
import numpy as np
import face_recognition
import pickle
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk

class FaceAuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Yüz Tanıma Giriş Sistemi")
        self.root.geometry("800x600")
        
        self.users_dir = "users"
        self.encodings_file = "encodings.pkl"
        
        # Create users directory if it doesn't exist
        if not os.path.exists(self.users_dir):
            os.makedirs(self.users_dir)
        
        # Initialize face encodings
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_encodings()
        
        # Initialize camera
        self.cap = None
        self.is_running = False
        
        # Create GUI
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Yüz Tanıma Giriş Sistemi", font=("Arial", 24))
        title_label.pack(pady=20)
        
        # Video frame
        self.video_frame = tk.Label(self.root)
        self.video_frame.pack(pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=20)
        
        # Register button
        self.register_btn = tk.Button(buttons_frame, text="Kayıt Ol", font=("Arial", 14),
                                      command=self.register_user, width=15)
        self.register_btn.grid(row=0, column=0, padx=10)
        
        # Login button
        self.login_btn = tk.Button(buttons_frame, text="Giriş Yap", font=("Arial", 14),
                                   command=self.login_user, width=15)
        self.login_btn.grid(row=0, column=1, padx=10)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Hoş Geldiniz!", font=("Arial", 14))
        self.status_label.pack(pady=10)
    
    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.is_running = True
        self.update_camera()
    
    def stop_camera(self):
        self.is_running = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None
    
    def update_camera(self):
        if self.is_running:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=img)
                self.video_frame.configure(image=img)
                self.video_frame.image = img
            self.root.after(10, self.update_camera)
    
    def load_encodings(self):
        if os.path.exists(self.encodings_file):
            with open(self.encodings_file, "rb") as f:
                data = pickle.load(f)
                self.known_face_encodings = data["encodings"]
                self.known_face_names = data["names"]
    
    def save_encodings(self):
        data = {"encodings": self.known_face_encodings, "names": self.known_face_names}
        with open(self.encodings_file, "wb") as f:
            pickle.dump(data, f)
    
    def register_user(self):
        username = simpledialog.askstring("Kayıt", "Kullanıcı adınızı girin:")
        if not username:
            return
        
        if username in self.known_face_names:
            messagebox.showerror("Hata", "Bu kullanıcı adı zaten kayıtlı!")
            return
        
        self.status_label.config(text="Kayıt için yüzünüzü kameraya gösterin")
        self.start_camera()
        
        # Wait 2 seconds to prepare
        self.root.after(2000, lambda: self.capture_face_for_registration(username))
    
    def capture_face_for_registration(self, username):
        if not self.is_running or self.cap is None:
            messagebox.showerror("Hata", "Kamera başlatılamadı!")
            return
        
        ret, frame = self.cap.read()
        if not ret:
            messagebox.showerror("Hata", "Kamera görüntüsü alınamadı!")
            self.stop_camera()
            return
        
        # Convert to RGB (face_recognition uses RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        face_locations = face_recognition.face_locations(rgb_frame)
        
        if len(face_locations) == 0:
            messagebox.showerror("Hata", "Yüz bulunamadı! Lütfen tekrar deneyin.")
            self.stop_camera()
            return
        
        if len(face_locations) > 1:
            messagebox.showerror("Hata", "Birden fazla yüz algılandı! Lütfen tek başınıza tekrar deneyin.")
            self.stop_camera()
            return
        
        # Encode the face
        face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
        
        # Save the encoding
        self.known_face_encodings.append(face_encoding)
        self.known_face_names.append(username)
        self.save_encodings()
        
        # Save the face image
        user_img_dir = os.path.join(self.users_dir, username)
        if not os.path.exists(user_img_dir):
            os.makedirs(user_img_dir)
        
        cv2.imwrite(os.path.join(user_img_dir, "face.jpg"), frame)
        
        self.stop_camera()
        self.status_label.config(text=f"Kullanıcı {username} başarıyla kaydedildi!")
        messagebox.showinfo("Başarılı", f"Kullanıcı {username} başarıyla kaydedildi!")
    
    def login_user(self):
        self.status_label.config(text="Giriş için yüzünüzü kameraya gösterin")
        self.start_camera()
        
        # Wait 2 seconds to prepare
        self.root.after(2000, self.authenticate_face)
    
    def authenticate_face(self):
        if not self.is_running or self.cap is None:
            messagebox.showerror("Hata", "Kamera başlatılamadı!")
            return
        
        ret, frame = self.cap.read()
        if not ret:
            messagebox.showerror("Hata", "Kamera görüntüsü alınamadı!")
            self.stop_camera()
            return
        
        # Convert to RGB (face_recognition uses RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        face_locations = face_recognition.face_locations(rgb_frame)
        
        if len(face_locations) == 0:
            messagebox.showerror("Hata", "Yüz bulunamadı! Lütfen tekrar deneyin.")
            self.stop_camera()
            return
        
        if len(face_locations) > 1:
            messagebox.showerror("Hata", "Birden fazla yüz algılandı! Lütfen tek başınıza tekrar deneyin.")
            self.stop_camera()
            return
        
        # Encode the face
        face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
        
        # Compare with known faces
        matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.6)
        
        if True in matches:
            # Find the index of the first match
            match_index = matches.index(True)
            username = self.known_face_names[match_index]
            
            self.stop_camera()
            self.status_label.config(text=f"Hoş geldiniz, {username}!")
            messagebox.showinfo("Başarılı", f"Hoş geldiniz, {username}!")
        else:
            self.stop_camera()
            self.status_label.config(text="Kimlik doğrulama başarısız!")
            messagebox.showerror("Hata", "Yüz tanınmadı! Erişim reddedildi.")
    
    def on_closing(self):
        self.stop_camera()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = FaceAuthApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 