"""
    This shows both the rendering and the saving of the image
    properly implemented.
    To render it, I just needed to call Draw on the FBO after rendering
    and to update the `display_texture` RECT attached to the widget's canvas
    so it displays it and stays updated
    
    You can scale the resolution of the FBO width and height
    so the exported image can be at a higher resolution.
"""

from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.resources import resource_find
# from kivy.graphics.transformation import Matrix
# from kivy.graphics.opengl import glEnable, glDisable, GL_DEPTH_TEST, glViewport, GL_VIEWPORT, glGetIntegerv
from kivy.graphics import PushMatrix, PopMatrix, Mesh, Fbo, Rectangle, ClearColor, ClearBuffers, RenderContext , Callback #, Color, Scale, Translate,
# from kivy.properties import ListProperty
# from kivy.core.image import Image as CoreImage
import time
import os
from PIL import Image
from cv2 import VideoWriter, VideoWriter_fourcc, cvtColor, imwrite, COLOR_RGBA2BGR, COLOR_RGBA2RGB, COLOR_RGB2BGR, COLOR_BGR2RGB
import numpy as np

SHADER_PROGRAMS_PATH = os.path.join(os.path.dirname(__file__), "..", "programs")

"""
    Consider the `_int` file or intermediate file. It's where  
"""

class OpenglRender(Widget):
    def __init__(self, sourceName, resolutionScale=1.0, videoCapture=False, videoCaptureDuration=0.0, videoCapturePath="", videoContainerSize=(0.0, 0.0), **kwargs):


        self.vertex_shader = """\
        ---VERTEX SHADER-------------------------------------------------------\n\
        #version 330 core\n\
        #ifdef GL_ES\n\
        precision highp float;\n\
        #endif\n\
        attribute vec2 in_pos;\n\
        void main (void) {\n\
        gl_Position = vec4(in_pos, 0.0, 1.0);\n\
        }\
        """
        
        self.fragment_shader_head = """\
        ---FRAGMENT SHADER-----------------------------------------------------\n\
        #version 330 core\n\
        #ifdef GL_ES\n\
        precision highp float;\n\
        #endif\n\
        uniform vec2 u_resolution;\n\
        uniform float u_time;\
        """

        self.export_name = sourceName
        
        #   Create the Shader Context
        self.shader = RenderContext(compute_normal_mat=True)
        target_src = self.preprocess_program_file(sourceName)
        self.shader.shader.source = resource_find(target_src)


        #   FBO that Renders Offscreen
        self.fbo = Fbo(size=(int(self.size[0] * resolutionScale),
                            int(self.size[1]*resolutionScale)),
                       with_stencilbuffer=True,
                       compute_normal_mat=True)                    

        self.fbo.shader.source = self.shader.shader.source

        super(OpenglRender, self).__init__(**kwargs)

        self.video_writer = None
        self.video_duration = videoCaptureDuration
        timestamp = time.strftime('%a_%b_%Y__%H_%M_%S')

        if videoCapture:
            video_path = os.path.join(videoCapturePath, sourceName.split(".")[0] + timestamp + ".mp4")
            fourcc = VideoWriter_fourcc(*"mp4v")
            width, height = int(self.size_hint_x * videoContainerSize[0]), int(self.size_hint_y * videoContainerSize[1])
            #   if just the size is incorrect, the capture will fail. The dimensions must be integers too!
            self.video_writer = VideoWriter(video_path, fourcc, 30.0, (width, height))

        #   Setup Rendering
        self._setup_fbo()
        self._setup_display()

        #   Automatically Handle Resize
        self.bind(size=self._resize_fbo, pos=self._update_rect)
            
        #   Run the `update_glsl` every 1/60 seconds
        Clock.schedule_interval(self._update_shader, 1/60.0)
        Clock.schedule_interval(self.update_time, 1/1000.0)

        self.time = 0.0


    def preprocess_program_file(self, src_name):
        """
            Because of the uniqueness of the OpenGL source code used here...
            I need to preprocess the program file
        """
        file_path = os.path.join(SHADER_PROGRAMS_PATH, src_name)

        #   Read File
        code = ""
        
        with open(file_path, "r") as rfs:
            code = rfs.read()
        
        #   Check for Landmarks --- onyl need to check for vertex shader
        if "VERTEX SHADER" in code:
            return f"programs/{src_name}"
        
        #   If No Landmarks, then append them
        
        code = f"{self.vertex_shader.strip()}\n{self.fragment_shader_head.strip()}\n{code}"
        file_path = os.path.join(SHADER_PROGRAMS_PATH, "_int", "int.glsl")
        new_path = f"programs/_int/int.glsl"
        
        #   create a new file in the intermediate path and write the new code into it
        with open(file_path, "w") as wfs:
            wfs.write(code)

        return new_path

    def _setup_fbo(self):
        with self.fbo:
            ClearColor(0, 0, 0, 0)
            ClearBuffers()

            PushMatrix()
            self.setup_quad_scene()
            PopMatrix()
        self.fbo.draw() #   ensure to draw it!
        self.start_time = time.time()

        if self.video_writer:
            # self.save_frame_v1()
            self.save_frame_v2()

    def save_frame_v1(self):
        img_data = self.fbo.pixels
        img = Image.frombytes("RGBA", self.fbo.size, img_data)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)

        #   convert to OpenCV format
        rgb = np.array(img)[:, :, :3]
        #   strip alpha
        bgr = cvtColor(rgb, COLOR_RGB2BGR)
        self.video_writer.write(bgr)
    
    def save_frame_v2(self):
        raw_data = self.fbo.pixels
        img = np.frombuffer(raw_data, dtype='uint8').reshape(
            ((*self.fbo.size[1::-1], 4))
        )
        #   flip vertically since OpenGL's origin is bottom-left
        img = np.flipud(img)    #   or cv2.flip(img, 0)
        bgr = cvtColor(img, COLOR_RGBA2RGB)
        self.video_writer.write(bgr)
    
    def _setup_display(self):
        with self.canvas:
            self.display_texture = Rectangle(texture=self.fbo.texture,
                                            pos=self.pos, size=(self.width, self.height))   #   the last part flups the display vertically

    def _resize_fbo(self, *args):
        self.fbo.size = self.size
        self.display_texture.size = self.size
        # print("Called")
        # print("Widget Size: {}, {}".format(*self.size))
        # print("FBO Size: {}, {}".format(*self.fbo.size))
        # print("Display Texture Size: {}, {}".format(*self.display_texture.size))
        self._update_rect()

    def _update_rect(self, *args):
        self.display_texture.pos = self.pos

    def update_time(self, dt):
        self.time += dt
    
    def _update_shader(self, dt):
        self.time += dt
        self.shader['u_resolution'] = (float(self.fbo.size[0]), float(self.fbo.size[1]))
        self.shader['u_time'] = self.time
        self.fbo['u_resolution'] = self.shader['u_resolution']
        self.fbo['u_time'] = self.shader['u_time']
        self.fbo.ask_update()
        self.fbo.draw()
        self.update_display_texture()

        deltatime = time.time() - self.start_time 
        if self.video_writer and deltatime < self.video_duration:
            # self.save_frame_v1()
            self.save_frame_v2()
            
    def update_display_texture(self, *args):
        self.display_texture.texture = self.fbo.texture

    def save_as_png(self, path):
        """
            This fixes the saving issue
        """
        export_name = self.export_name.split(".")[0]
  
        """
            w3schools.com/python/python_datetime.asp
            a -- day name short
            A -- day name long
            b -- month name short
            B -- month name long
            d -- day of month as number
            m -- month as number
        """
        timestamp = time.strftime('%a_%b_%Y__%H_%M_%S')
        export_path = os.path.join(path, f"{export_name}_{timestamp}.png")
        
        self.fbo.draw()

        #   first method does work; but the image is upside-down
        #   Save as PNG
        # image = CoreImage(self.fbo.texture)
        # print("Path: ", export_path)
        # image.save(export_path)


        #   doesn't work  since the display_texture doesn't even show
        # self.export_to_png(export_path)

        #   Also didn't work for the same reason as `self.export_to_png`
        # image = CoreImage(self.display_texture.texture)
        # print("Path: ", export_path)
        # image.save(export_path)


        #   One good method: using PIL to reload the saved image, flip it properly, and save again
        #   but it requires saving the image twice
        # self.fbo.draw()
        # #   Save as PNG
        # image = CoreImage(self.fbo.texture)
        # image.save(export_path)
        # img = Image.open(export_path)
        # #   flip
        # img = img.transpose(Image.FLIP_TOP_BOTTOM)
        # img.save(export_path)

        """
            Finally:
                second best method is to use the raw FBO pizel data to avoid re-openning the file ans savinf twice
                Get pixel data from FBO
        """
        # pixels = self.fbo.texture.pixels        
        # #   convert to PIL image (RGBA, size = FBO size)
        # img = Image.frombytes("RGBA", self.fbo.size, pixels)
        # img = img.transpose(Image.FLIP_TOP_BOTTOM)
        # img.save(export_path)


        """
            Bonus:
            Saving pixel data with opencv
        """
        pixels = self.fbo.texture.pixels

        image_data = np.frombuffer(pixels, dtype='uint8').reshape(
            ((*self.fbo.size[1::-1], 4))
        )
        image_data = cvtColor(image_data, COLOR_RGBA2BGR)
        image_data = np.flipud(image_data) 
        imwrite(export_path, image_data)
        
        
    def setup_quad_scene(self):
        # Color()
        # PushMatrix()
        self.mesh = Mesh(
            vertices=self.get_vertices(),
            indices= self.get_indices(),
            fmt=self.get_format(),
            mode='triangles',
        )
        # PopMatrix()

    
    def get_vertices(self):
        return [-1, -1, 1, -1, 1, 1, -1, 1]
    
    def get_indices(self):
        return [0, 1, 2, 2, 3, 0]
    
    def get_format(self):
        return [(b'in_pos', 2, 'float')]

    


    # def setup_gl_state(self, *args):
    #     #   save the old viewport
    #     self.prev_viewport = glGetIntegerv(GL_VIEWPORT)

    #     #   Get the widget's position in window coordinates
    #     self.win_x, self.win_y = self.to_window(self.x, self.y, initial=False, relative=False)
    #     # self.win_x, self.win_y = self.to_window(self.fbo_rect.pos[0], self.fbo_rect.pos[1], initial=True, relative=False)

    #     #   Flip y-xis because OpenGL origin is bottom-left, Kivy's is top-left
    #     self.flipped_win_y = Window.height - self.win_y - self.height

    #     # Optional: enable depth testing or other GL options
    #     # glEnable(GL_DEPTH_TEST)

    #     #   Set OpenGL viewport to match widget area
    #     # glViewport(int(self.win_x), int(self.flipped_win_y), int(self.width), int(self.height))
    #     # glViewport(int(self.win_x), int(self.flipped_win_y), int(Window.width), int(Window.height))
    #     # glViewport(int(self.win_x), int(self.win_y), int(Window.width), int(Window.height))
    #     glViewport(int(0), int(0), int(Window.width), int(Window.height))
    #     # glViewport(int(self.fbo_rect.pos[0]), int(self.fbo_rect.pos[1]), int(self.fbo_rect.size[0]), int(self.fbo_rect.size[1]))

    #     self.update_fbo()
    #     self.update_fbo_rect()



    # def reset_gl_state(self, *args):
    #     # Restore previous viewport (important!)
    #     glViewport(*self.prev_viewport)

    #     # Optional: disable anything you enabled
    #     # glDisable(GL_DEPTH_TEST)
    
