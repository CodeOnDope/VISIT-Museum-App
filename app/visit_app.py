# VISIT - Interactive Museum Application
# Developed by Dineshkumar Rajendran
# Version 1.0

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pygame
import mediapipe as mp
import threading
import time
import os
import json
from PIL import Image, ImageTk
import hashlib
from datetime import datetime

class VisitApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("VISIT - Interactive Museum App v1.0 by Dineshkumar Rajendran")
        self.root.geometry("1200x800")
        
        # License verification
        if not self.verify_license():
            return
            
        # Initialize MediaPipe
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_hands = mp.solutions.hands
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Initialize detectors
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.7)
        self.face_mesh = self.mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        
        # Initialize pygame for audio
        pygame.mixer.init()
        
        # Application state
        self.camera = None
        self.is_running = False
        self.is_fullscreen = False
        self.current_frame = None
        
        # Detection states
        self.detection_states = {
            'face': False,
            'eye_movement': False,
            'lip_movement': False,
            'face_approaching': False,
            'face_receding': False,
            'hands': False,
            'pose': False,
            'movement': False
        }
        
        # Media storage
        self.media_config = {
            'default': {
                'image': None,
                'video': None,
                'audio': None
            },
            'face_detection': {
                'image': None,
                'video': None,
                'audio': None
            },
            'eye_movement': {
                'image': None,
                'video': None,
                'audio': None
            },
            'lip_movement': {
                'image': None,
                'video': None,
                'audio': None
            },
            'face_approaching': {
                'image': None,
                'video': None,
                'audio': None
            },
            'face_receding': {
                'image': None,
                'video': None,
                'audio': None
            },
            'hands_detection': {
                'image': None,
                'video': None,
                'audio': None
            },
            'pose_detection': {
                'image': None,
                'video': None,
                'audio': None
            },
            'movement_detection': {
                'image': None,
                'video': None,
                'audio': None
            }
        }
        
        # Previous frame for movement detection
        self.prev_frame = None
        self.face_distance_history = []
        
        self.setup_ui()
        self.bind_shortcuts()
        
    def verify_license(self):
        """Verify the license file"""
        try:
            if not os.path.exists('license.key'):
                messagebox.showerror("License Error", "License file not found. Please contact the developer.")
                self.root.destroy()
                return False
                
            with open('license.key', 'r') as f:
                license_content = f.read().strip()
                
            # Try to parse as JSON
            try:
                license_data = json.loads(license_content)
            except json.JSONDecodeError:
                messagebox.showerror("License Error", "Invalid license file format. Please contact the developer.")
                self.root.destroy()
                return False
                
            # Verify license validity
            if not self.validate_license(license_data):
                messagebox.showerror("License Error", "Invalid license. Please contact the developer.")
                self.root.destroy()
                return False
                
            return True
        except Exception as e:
            messagebox.showerror("License Error", f"License verification failed: {str(e)}")
            self.root.destroy()
            return False
    
    def validate_license(self, license_data):
        """Validate license data"""
        try:
            # Ensure license_data is a dictionary
            if not isinstance(license_data, dict):
                print(f"License data is not a dictionary: {type(license_data)}")
                return False
                
            # Check required fields
            required_fields = ['museum_id', 'expiry', 'hash']
            for field in required_fields:
                if field not in license_data:
                    print(f"Missing required field: {field}")
                    return False
            
            # Check if license has expired
            expiry_date = datetime.strptime(license_data['expiry'], '%Y-%m-%d')
            if datetime.now() > expiry_date:
                print("License has expired")
                return False
                
            # Verify hash using the EXACT same algorithm as generator
            hash_input = f"{license_data['museum_id']}{license_data['expiry']}VISIT_SECRET_KEY"
            expected_hash = hashlib.sha256(hash_input.encode()).hexdigest()
            
            # Debug information (can be removed in production)
            print(f"License validation debug:")
            print(f"Museum ID: {license_data['museum_id']}")
            print(f"Expiry: {license_data['expiry']}")
            print(f"Hash input: {hash_input}")
            print(f"Expected hash: {expected_hash}")
            print(f"License hash: {license_data['hash']}")
            print(f"Hash match: {expected_hash == license_data['hash']}")
            
            return expected_hash == license_data['hash']
        except Exception as e:
            print(f"License validation error: {e}")
            return False
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Dashboard tab
        self.dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_frame, text='Dashboard')
        
        # Media configuration tab
        self.media_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.media_frame, text='Media Configuration')
        
        # Testing tab
        self.testing_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.testing_frame, text='Testing Mode')
        
        self.setup_dashboard()
        self.setup_media_config()
        self.setup_testing_mode()
        
    def setup_dashboard(self):
        """Setup dashboard controls"""
        # Camera controls
        camera_frame = ttk.LabelFrame(self.dashboard_frame, text="Camera Controls")
        camera_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(camera_frame, text="Start Camera", command=self.start_camera).pack(side='left', padx=5)
        ttk.Button(camera_frame, text="Stop Camera", command=self.stop_camera).pack(side='left', padx=5)
        ttk.Button(camera_frame, text="Test Mode", command=self.toggle_testing_mode).pack(side='left', padx=5)
        ttk.Button(camera_frame, text="Full Screen", command=self.toggle_fullscreen).pack(side='left', padx=5)
        
        # Detection status
        status_frame = ttk.LabelFrame(self.dashboard_frame, text="Detection Status")
        status_frame.pack(fill='x', padx=10, pady=5)
        
        self.status_labels = {}
        for detection_type in self.detection_states.keys():
            frame = ttk.Frame(status_frame)
            frame.pack(fill='x', padx=5, pady=2)
            
            ttk.Label(frame, text=f"{detection_type.replace('_', ' ').title()}:").pack(side='left')
            self.status_labels[detection_type] = ttk.Label(frame, text="OFF", foreground='red')
            self.status_labels[detection_type].pack(side='right')
        
        # System info
        info_frame = ttk.LabelFrame(self.dashboard_frame, text="System Information")
        info_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.info_text = tk.Text(info_frame, height=10)
        scrollbar = ttk.Scrollbar(info_frame, orient="vertical", command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        
        self.info_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.log_info("VISIT Application initialized successfully")
        self.log_info("Developed by Dineshkumar Rajendran")
        
    def setup_media_config(self):
        """Setup media configuration interface"""
        # Create scrollable frame
        canvas = tk.Canvas(self.media_frame)
        scrollbar = ttk.Scrollbar(self.media_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Media configuration for each detection type
        for detection_type in self.media_config.keys():
            frame = ttk.LabelFrame(scrollable_frame, text=f"{detection_type.replace('_', ' ').title()} Media")
            frame.pack(fill='x', padx=10, pady=5)
            
            # Image selection
            img_frame = ttk.Frame(frame)
            img_frame.pack(fill='x', padx=5, pady=2)
            ttk.Label(img_frame, text="Image:").pack(side='left')
            ttk.Button(img_frame, text="Browse", 
                      command=lambda dt=detection_type: self.browse_media(dt, 'image')).pack(side='right')
            
            # Video selection
            vid_frame = ttk.Frame(frame)
            vid_frame.pack(fill='x', padx=5, pady=2)
            ttk.Label(vid_frame, text="Video:").pack(side='left')
            ttk.Button(vid_frame, text="Browse", 
                      command=lambda dt=detection_type: self.browse_media(dt, 'video')).pack(side='right')
            
            # Audio selection
            aud_frame = ttk.Frame(frame)
            aud_frame.pack(fill='x', padx=5, pady=2)
            ttk.Label(aud_frame, text="Audio:").pack(side='left')
            ttk.Button(aud_frame, text="Browse", 
                      command=lambda dt=detection_type: self.browse_media(dt, 'audio')).pack(side='right')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Save/Load configuration
        config_frame = ttk.Frame(self.media_frame)
        config_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(config_frame, text="Save Configuration", command=self.save_config).pack(side='left', padx=5)
        ttk.Button(config_frame, text="Load Configuration", command=self.load_config).pack(side='left', padx=5)
        
    def setup_testing_mode(self):
        """Setup testing mode interface"""
        # Camera display
        self.camera_label = ttk.Label(self.testing_frame)
        self.camera_label.pack(padx=10, pady=10)
        
        # Testing controls
        test_controls = ttk.Frame(self.testing_frame)
        test_controls.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(test_controls, text="Test All Detections", command=self.test_all_detections).pack(side='left', padx=5)
        ttk.Button(test_controls, text="Calibrate Sensitivity", command=self.calibrate_sensitivity).pack(side='left', padx=5)
        ttk.Button(test_controls, text="Reset Detections", command=self.reset_detections).pack(side='left', padx=5)
        
    def bind_shortcuts(self):
        """Bind keyboard shortcuts"""
        self.root.bind('<F5>', lambda e: self.reset_application())
        self.root.bind('<F6>', lambda e: self.refresh_camera())
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
        self.root.bind('<Escape>', lambda e: self.exit_fullscreen())
        
    def browse_media(self, detection_type, media_type):
        """Browse and select media files"""
        if media_type == 'image':
            filetypes = [("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        elif media_type == 'video':
            filetypes = [("Video files", "*.mp4 *.avi *.mov *.mkv")]
        else:  # audio
            filetypes = [("Audio files", "*.mp3 *.wav *.ogg")]
            
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.media_config[detection_type][media_type] = filename
            self.log_info(f"Selected {media_type} for {detection_type}: {filename}")
    
    def start_camera(self):
        """Start camera capture"""
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                raise Exception("Cannot open camera")
                
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            self.is_running = True
            self.camera_thread = threading.Thread(target=self.camera_loop)
            self.camera_thread.daemon = True
            self.camera_thread.start()
            
            self.log_info("Camera started successfully")
            
        except Exception as e:
            messagebox.showerror("Camera Error", f"Failed to start camera: {str(e)}")
    
    def stop_camera(self):
        """Stop camera capture"""
        self.is_running = False
        if self.camera:
            self.camera.release()
            self.camera = None
        self.log_info("Camera stopped")
    
    def camera_loop(self):
        """Main camera processing loop"""
        while self.is_running:
            if self.camera is None:
                break
                
            ret, frame = self.camera.read()
            if not ret:
                continue
                
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            self.current_frame = frame.copy()
            
            # Process detections
            self.process_detections(frame)
            
            # Update display in testing mode
            if self.notebook.index(self.notebook.select()) == 2:  # Testing tab
                self.update_camera_display(frame)
                
            # Handle media playback based on detections
            self.handle_media_playback()
            
            time.sleep(0.03)  # ~30 FPS
    
    def process_detections(self, frame):
        """Process all types of detections"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Reset detection states
        for key in self.detection_states:
            self.detection_states[key] = False
        
        # Face detection
        face_results = self.face_detection.process(rgb_frame)
        if face_results.detections:
            self.detection_states['face'] = True
            
            # Face distance calculation for approach/recede detection
            detection = face_results.detections[0]
            bbox = detection.location_data.relative_bounding_box
            face_area = bbox.width * bbox.height
            
            self.face_distance_history.append(face_area)
            if len(self.face_distance_history) > 10:
                self.face_distance_history.pop(0)
                
            if len(self.face_distance_history) >= 5:
                recent_avg = sum(self.face_distance_history[-3:]) / 3
                older_avg = sum(self.face_distance_history[-6:-3]) / 3
                
                if recent_avg > older_avg * 1.1:
                    self.detection_states['face_approaching'] = True
                elif recent_avg < older_avg * 0.9:
                    self.detection_states['face_receding'] = True
        
        # Face mesh for eye and lip movement
        mesh_results = self.face_mesh.process(rgb_frame)
        if mesh_results.multi_face_landmarks:
            # Simplified eye/lip movement detection
            landmarks = mesh_results.multi_face_landmarks[0]
            
            # Eye landmarks (simplified)
            left_eye = landmarks.landmark[33]
            right_eye = landmarks.landmark[263]
            eye_distance = abs(left_eye.x - right_eye.x)
            
            if hasattr(self, 'prev_eye_distance'):
                if abs(eye_distance - self.prev_eye_distance) > 0.001:
                    self.detection_states['eye_movement'] = True
            self.prev_eye_distance = eye_distance
            
            # Lip landmarks (simplified)
            upper_lip = landmarks.landmark[13]
            lower_lip = landmarks.landmark[14]
            lip_distance = abs(upper_lip.y - lower_lip.y)
            
            if hasattr(self, 'prev_lip_distance'):
                if abs(lip_distance - self.prev_lip_distance) > 0.001:
                    self.detection_states['lip_movement'] = True
            self.prev_lip_distance = lip_distance
        
        # Hand detection
        hand_results = self.hands.process(rgb_frame)
        if hand_results.multi_hand_landmarks:
            self.detection_states['hands'] = True
        
        # Pose detection
        pose_results = self.pose.process(rgb_frame)
        if pose_results.pose_landmarks:
            self.detection_states['pose'] = True
        
        # Movement detection
        if self.prev_frame is not None:
            diff = cv2.absdiff(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 
                              cv2.cvtColor(self.prev_frame, cv2.COLOR_BGR2GRAY))
            movement_threshold = 30
            movement_pixels = np.sum(diff > movement_threshold)
            
            if movement_pixels > 1000:  # Adjust threshold as needed
                self.detection_states['movement'] = True
        
        self.prev_frame = frame.copy()
        
        # Update status display
        self.update_detection_status()
    
    def update_detection_status(self):
        """Update detection status in the UI"""
        for detection_type, is_active in self.detection_states.items():
            if detection_type in self.status_labels:
                color = 'green' if is_active else 'red'
                text = 'ON' if is_active else 'OFF'
                self.status_labels[detection_type].config(text=text, foreground=color)
    
    def update_camera_display(self, frame):
        """Update camera display in testing mode"""
        # Draw detection overlays
        if self.detection_states['face']:
            cv2.putText(frame, "FACE DETECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        if self.detection_states['hands']:
            cv2.putText(frame, "HANDS DETECTED", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        if self.detection_states['movement']:
            cv2.putText(frame, "MOVEMENT DETECTED", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Convert to PhotoImage and display
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)
        pil_image = pil_image.resize((640, 480))
        photo = ImageTk.PhotoImage(pil_image)
        
        self.camera_label.configure(image=photo)
        self.camera_label.image = photo
    
    def handle_media_playback(self):
        """Handle media playback based on current detections"""
        # Determine which media to play based on priority
        active_detection = None
        
        # Priority order (highest to lowest)
        priority_order = ['face_approaching', 'face_receding', 'lip_movement', 'eye_movement', 
                         'hands', 'pose', 'movement', 'face']
        
        for detection in priority_order:
            if self.detection_states[detection]:
                active_detection = f"{detection}_detection" if detection != 'face' else 'face_detection'
                break
        
        # If no detection, use default
        if not active_detection:
            active_detection = 'default'
        
        # Play appropriate media
        self.play_media(active_detection)
    
    def play_media(self, detection_type):
        """Play media for specific detection type"""
        media = self.media_config.get(detection_type, {})
        
        # Handle audio
        audio_file = media.get('audio')
        if audio_file and os.path.exists(audio_file):
            try:
                if not pygame.mixer.get_busy():
                    pygame.mixer.music.load(audio_file)
                    pygame.mixer.music.play()
            except Exception as e:
                self.log_info(f"Audio playback error: {str(e)}")
        
        # Handle video/image display would be implemented here
        # For full implementation, you'd need additional video display logic
    
    def toggle_testing_mode(self):
        """Toggle to testing mode"""
        self.notebook.select(2)  # Select testing tab
        if not self.is_running:
            self.start_camera()
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)
        
        if self.is_fullscreen:
            self.log_info("Entered fullscreen mode")
        else:
            self.log_info("Exited fullscreen mode")
    
    def exit_fullscreen(self):
        """Exit fullscreen mode"""
        self.is_fullscreen = False
        self.root.attributes('-fullscreen', False)
        self.log_info("Exited fullscreen mode")
    
    def reset_application(self):
        """Reset application state"""
        self.stop_camera()
        for key in self.detection_states:
            self.detection_states[key] = False
        self.update_detection_status()
        pygame.mixer.stop()
        self.log_info("Application reset completed")
    
    def refresh_camera(self):
        """Refresh camera connection"""
        was_running = self.is_running
        self.stop_camera()
        time.sleep(1)
        if was_running:
            self.start_camera()
        self.log_info("Camera refreshed")
    
    def test_all_detections(self):
        """Test all detection systems"""
        self.log_info("Testing all detection systems...")
        
        # Simulate detection states for testing
        for detection_type in self.detection_states:
            self.detection_states[detection_type] = True
            self.update_detection_status()
            time.sleep(0.5)
            
        time.sleep(2)
        
        # Reset all detections
        for detection_type in self.detection_states:
            self.detection_states[detection_type] = False
        self.update_detection_status()
        
        self.log_info("Detection test completed")
    
    def calibrate_sensitivity(self):
        """Calibrate detection sensitivity"""
        messagebox.showinfo("Calibration", "Sensitivity calibration feature will be implemented based on specific requirements.")
    
    def reset_detections(self):
        """Reset all detection states"""
        for key in self.detection_states:
            self.detection_states[key] = False
        self.update_detection_status()
        self.log_info("All detections reset")
    
    def save_config(self):
        """Save media configuration"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.media_config, f, indent=4)
                messagebox.showinfo("Success", "Configuration saved successfully")
                self.log_info(f"Configuration saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
    
    def load_config(self):
        """Load media configuration"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    self.media_config = json.load(f)
                messagebox.showinfo("Success", "Configuration loaded successfully")
                self.log_info(f"Configuration loaded from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load configuration: {str(e)}")
    
    def log_info(self, message):
        """Log information to the info panel"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.info_text.insert(tk.END, log_message)
        self.info_text.see(tk.END)
    
    def run(self):
        """Start the application"""
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.mainloop()
        except Exception as e:
            print(f"Application error: {str(e)}")
    
    def on_closing(self):
        """Handle application closing"""
        self.stop_camera()
        pygame.mixer.quit()
        self.root.destroy()

if __name__ == "__main__":
    app = VisitApp()
    app.run()