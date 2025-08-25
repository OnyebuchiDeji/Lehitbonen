"""
    For building the aoo, here are BUILDOZER permissions to specify:

        andorid.permisssions = 
            WRITE_EXTERNAL_STORAGE,
            READ_EXTERNAL_STORAGE,
            MANAGE_EXTERNAL_STORAGE
"""

from kivy.app import App
from kivy.config import Config
from kivy.utils import platform
if platform == "android":
    Config.set('graphics', 'fullscreen', 'auto')    ##  Make it fullscreen
from kivy.lang import Builder
from kivy.core.text import LabelBase    #   for registering custom fonts
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
# from kivy.core.image import Image
from kivy.properties import NumericProperty, ListProperty #,ObjectProperty, ReferenceListProperty, ObservableList, DictProperty
from .renderer import OpenglRender, Widget, Window
from .code_widget import CodeArea
from kivy.clock import Clock

Clock.max_iteration = 1000

from kivy.properties import (
    StringProperty,
)
import os
import time

"""
    The android module used in Kivy apps on ANdroid (e.g. android.storage, android.permissions)
    is not available via pip. It's automatically included when one builds their app for Android
    using tools like Buildozer or PyJNIus (Indirectly)

    SO NO NEED TO INSTALL IT MANUALLY VIA PIP

    So when running on Deskop, the below platform check precents the ModuleNotFoundError from being
    raised.
"""
if platform == "android":
    from android.storage import primary_external_storage_path
    from android.permissions import request_permissions, Permission


SHADER_PROGRAMS_PATH = os.path.join(os.path.dirname(__file__), "..", "programs")
g_MOBILE_DOWNLOAD_STORAGE_PATH = os.path.join(SHADER_PROGRAMS_PATH, "..", "_exports") if platform == "android" else ""

def RequestAndroidPermissions():
    request_permissions([
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE
    ])

def PrepareMobileStoragePath():
    global g_MOBILE_DOWNLOAD_STORAGE_PATH
    
    if platform == "android":
        downloads_dir = os.path.join(primary_external_storage_path(), "Download")
    else:
        downloads_dir = os.path.expanduser("~/Downloads")

    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)
    
    g_MOBILE_DOWNLOAD_STORAGE_PATH = downloads_dir

if platform == "android":
    RequestAndroidPermissions()
    PrepareMobileStoragePath()

class TopHeaderbar(BoxLayout):
    ...

class CodingToolbar(GridLayout):
    ...

class RenderScreenToolbar(GridLayout):
    ...

class CreateFileButton(Button):
    ...

class OptionButton(Button):
    action_list = ListProperty()
    ...

class ProgramInfoPopup(Popup):
    text_var1 = StringProperty()
    text_var2 = StringProperty()

class DeleteFilePopup(Popup):
    file_title = StringProperty()

class AboutScreen(Screen):
    about_article = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.oninit()
    
    def read_file(self):
        """Load and Return the About Article from memory"""
        # print("About Screen Read File!")
        target_path = os.path.join(SHADER_PROGRAMS_PATH, "..","_resources", "about_article.txt")
        with open(target_path, "r") as rfs:
            return rfs.read()

class IconButton(OptionButton):
    icon_name_var= StringProperty()
    ...

class OptionPopup(Popup):
    buttons_name_list = ListProperty()
    # buttons_dict = DictProperty()
    def __init__(self, callerScreenRef=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #   screen ref
        self.screen_ref = callerScreenRef
        self.container_ref = self.ids['id_option_popup_button_container']

        # self.pure_oninit()


        if str(type(self.screen_ref)).find("Editor") != -1:
            self.edit_screen_oninit()
        else:
            self.main_screen_oninit()

    # def action(self, *args):
    #     for action in args[0].action_list:
    #         eval(action)

    #     # eval(args[0].action_var)
    # def pure_oninit(self):
    #     print("In Pure Init")
    #     print("Size: ", len(self.buttons_dict))
    #     for k, v in self.buttons_dict.items():
    #         print("Key: ", k)
    #         print("Val: ", v)
    #         new_button = OptionButton(text=k)
    #         new_button.action_list = v
    #         new_button.bind(on_release=self.action)
    #         self.container_ref.add_widget(new_button)

    #     print("Container Size: ", len(self.container_ref.children))

    
    def edit_screen_oninit(self):
        # print("Edit Screen Oninit Called!")
        for name in self.buttons_name_list:
            new_button = OptionButton(text=name)
            match name.lower():
                case "save":
                    new_button.bind(on_release=self.screen_ref.option_save_file)
                case _:
                    new_button.bind(on_release=self.screen_ref.open_action_popup)

            self.container_ref.add_widget(new_button)

    def main_screen_oninit(self):
        # print("Main Screen Oninit Called!")
        self.container_ref = self.ids['id_option_popup_button_container']
        for name in self.buttons_name_list:
            new_button = OptionButton(text=name)
            match name.lower():
                case "":
                    new_button = IconButton(text="", icon_name_var="sunfill_icon.png")
                    new_button.bind(on_release=self.screen_ref.toggle_theme)
                case "choose theme":
                    new_button.bind(on_release=self.screen_ref.choose_theme_popup)
                # case "recycle bin":
                #     new_button = IconButton(text="", icon_name_var="trashbinfill_icon.png")
                #     new_button.bind(on_release=self.screen_ref.to_recycle_screen)
                case "about":
                    new_button.bind(on_release=self.screen_ref.to_about_screen)

            self.container_ref.add_widget(new_button)


class ActionPopup(Popup):
    title_var = StringProperty()
    button_text_var = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        

class ProgramInfoButtonWidget(Widget):
    title = StringProperty()
    date_created = StringProperty()
    date_last_modified = StringProperty()
    y_val = NumericProperty()
    min_height = NumericProperty()

    # def __init__(self, title="", dateCreated="", dateLastModified="", **kwargs):
    #     super().__init__(**kwargs)
    #     self.title = title
    #     self.date_created = dateCreated
    #     self.date_last_modified = dateLastModified

class MainScreen(Screen):
    """
        This is the entry point screen
        where there will be the options
        icon, the name of the app
        and in the MainContent area
        there will be the list of all
        the glsl programs in the `programs`
        directory.

        When one is selected, it opens the next
        screen, the Editor Screen
        

    """
    main_content_height_var = NumericProperty()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.program_info_widgets_list = []
        self.theme_flag = True  # true means light | false means dark
        self.max_num = 6 #  the screen can only fit six of said widgets
        self.gap = 15
        self.y_increment = ((Window.height - 70) / self.max_num) + self.gap

        self.mid_semantic_method = self.sort_program_list 
    
    def oninit(self, *args):
        self.program_list = self.read_programs_info()
        content_container_ref =  self.ids['id_main_screen_main_content']
        #   Update Container Height
        self.main_content_height_var = len(self.program_list) * self.y_increment + self.gap
        # print("Main Content Height: ", self.main_content_height_var)
        self.stack_y = content_container_ref.height - 120
        self.append_to_content_area(content_container_ref)
        
    
    def read_programs_info(self):
        output_list = []
        target_path = SHADER_PROGRAMS_PATH

        for file in os.scandir(target_path):
            if file.is_file():
                info = {}
                info['name'] = file.name
                stats = file.stat()
                #   date created -- st_ctime - index 9
                info['date_created'] = time.ctime(stats[9])
                #   date last modified -- st_mtime - index 8
                info['date_last_modified'] = time.ctime(stats[8])
                #   date last accessed -- st_atime - index 7
                # ot = time.ctime(stats[7])
                output_list.append(info)
        return output_list

    def program_button_action(self, *args):
        editorScreenRef = None   #   Editor
        for screen in self.manager.screens:
            if screen.name == "Editor_Screen":
                editorScreenRef = screen
                break
        callerRef = args[0]
        #   The parent is the ProgramInfoButtonWidget that has the attributes to access
        title =  callerRef.parent.parent.title
        editorScreenRef.prepare_editor(title)
        self.manager.current = "Editor_Screen"
        self.manager.transition.direction = "left"

    def determine_mid_semantic_method(self):
        search_input = self.ids['id_main_screen_search_textinput'].text
        if search_input:
            self.mid_semantic_method = self.filter_and_sort_program_list
            return
        self.mid_semantic_method = self.sort_program_list
        
    def filter_and_sort_program_list(self):
        search_input = self.ids['id_main_screen_search_textinput'].text
        search_input = search_input.lower().strip()

        def filter_func(v:str):
            v = v['name'].lower()
            if (v.startswith(search_input)):
                return True
            return False

        #   filter the program list according to the search input
        self.program_list = list(filter(filter_func, self.program_list))
        print("Filtered:\n",self.program_list)
        self.sort_program_list()


    def sort_program_list(self):
        def sort_criterion(v):
            return time.mktime(time.strptime(v['date_last_modified']))
        self.program_list.sort(key=sort_criterion, reverse=True)



    def append_to_content_area(self, containerRef):
        """
            Sort by Date Last Modified
        """
        if len(containerRef.children) > 0:
            containerRef.clear_widgets()
            
        self.mid_semantic_method()

        for idx, item in enumerate(self.program_list):
            widget = ProgramInfoButtonWidget(
                title=item['name'],
                date_created=item['date_created'],
                date_last_modified=item['date_last_modified'],
                y_val = self.stack_y - (self.y_increment * idx)
            )
            button = widget.children[0].children[1]  #   the second child within the grid layout
            button.bind(on_release=self.program_button_action)
            containerRef.add_widget(widget)


    def delete_file(self, fileName):
        target_path = os.path.join(SHADER_PROGRAMS_PATH, fileName)
        os.remove(target_path)
        

    def open_menu_popup(self, *args):
        self.menu_popup = OptionPopup(
            self,
            title="Menu",
            buttons_name_list=["About"]
        )
        self.menu_popup.open()

    def open_settings_popup(self, *args):
        self.settings_popup = OptionPopup(
            self,
            title="Settings",
            buttons_name_list=["", "Choose Theme"]
        )
        self.settings_popup.open()

    def toggle_theme(self, *args):
        self.theme_flag = not self.theme_flag
        theme_button_ref = args[0]
        if self.theme_flag:
            theme_button_ref.icon_name_var = "sunfill_icon.png"
        else:
            theme_button_ref.icon_name_var = "moonfill_icon.png"


    def choose_theme_popup(self, *args):
        print("Choose Theme Popup")
    
    # def to_recycle_screen(self, *args):
    #     print("Screen Change")
    #     ...

    def to_about_screen(self, *args):
        self.manager.current = "About_Screen" 
        self.manager.transition.direction = "left"
        self.menu_popup.dismiss()
        
        
class EditorScreen(Screen):
    """
        This is the screen that shows the code editor
    """
    title = StringProperty()
    action_popup_output = StringProperty()
    # code = StringProperty()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_path = SHADER_PROGRAMS_PATH

    def create_new_file(self, title):
        if not title:
            title = "NewFile.glsl"
        target_path = os.path.join(self.target_path, title)

        exists = True
        while exists:
            if os.path.exists(target_path):
                title = str(os.path.basename(target_path))
                title = title.split(".")
                name = title[0]

                #   check if the file name already has a number:
                last_char = name[len(name)-1]
                if last_char.isnumeric():
                    num = int(name[len(name) - 1]) +1
                    name = name[0:len(name)-1:] + str(num)
                else:
                    name +="0"
                    
                title = ".".join([name, title[1]])

                target_path = os.path.join(self.target_path, title)
            else:
                exists = False
                self.title = title

        with open(target_path, "w") as wfs:
            wfs.write("")


    def prepare_editor(self, title):
        self.title = title
        #   reference to CodeArea Widget
        codeArea = self.ids['id_code_area']
        target_path = self.target_path
        for file in os.scandir(target_path):
            if file.is_file():
                if file.name == title:
                    target_path = os.path.join(target_path, file.name)
                    break
        with open(target_path,"r") as rfs:
            codeArea.text = rfs.read()
    

    def save_file(self):
        if not self.title:
            return
        codeArea = self.ids['id_code_area']
        target_path = os.path.join(self.target_path, self.title)
        with open(target_path, "w") as wfs:
            wfs.write(codeArea.text)
        # print("File {0} saved to {1}".format(self.title, self.target_path))
    
    def export_file(self, title=""):
        """
            Simply writes out the file to the FILE_EXPORT_PATH
        """
        target_path = os.path.join(g_MOBILE_DOWNLOAD_STORAGE_PATH, self.title)
        if title:
            target_path = os.path.join(g_MOBILE_DOWNLOAD_STORAGE_PATH, title)

        codeArea = self.ids['id_code_area']
        with open(target_path, "w") as wfs:
            wfs.write(codeArea.text)
    
    def option_save_file(self, *args):
        self.option_popup.dismiss()
        self.save_file()
    
    def option_save_file_as(self, *args):
        """Can save the file as a new extension. It's essentially creating a new file"""
        self.option_popup.dismiss()
        #   caller action button text input 
        # caller = args[0]
        #   for some reason, it's the fourth parent
        # caller_root = caller.parent.parent.parent.parent
        new_name = self.action_popup.ids['id_action_popup_textinput'].text
        target_path = os.path.join(self.target_path, new_name)
        codeArea = self.ids['id_code_area']
        with open(target_path, "w") as wfs:
            wfs.write(codeArea.text)
        self.action_popup.dismiss()
        

    def option_rename_file(self, *args):
        self.option_popup.dismiss()
        #   caller action button text input 
        # caller = args[0]
        # caller_root = caller.parent.parent.parent.parent
        
        new_name = self.action_popup.ids['id_action_popup_textinput'].text
        old_name_ext = self.title.split(".")[1] if len(self.title.split(".")) > 1 else self.title 

        old_path = os.path.join(self.target_path, self.title)
        print("Old File Name and Path: ", old_path)
        target_path = os.path.join(self.target_path, new_name.split(".")[0] + "." + old_name_ext)
        print("New File Name and Path: ", target_path)
        os.rename(old_path, target_path)
        
        #   dismiss popup
        self.action_popup.dismiss()

        #   update title
        self.title = new_name

    def open_options_popup(self, *args):
        self.option_popup = OptionPopup(
            self,
            buttons_name_list=["Save", "Rename", "Save As"]
        )
        self.option_popup.open()
    
    def open_action_popup(self, *args):
        #   accesses the text of the button that called
        option_name = args[0].text
        name_split = option_name.split(" ")
        self.action_popup = ActionPopup(
            title_var = option_name + "File" if len(name_split) == 1 else f"{name_split[0]} File {name_split[1]}",
            button_text_var = "Save"
        )
        # print(self.action_popup.ids['id_action_popup_submit_button'])
        match option_name.lower():
            case "rename":
                self.action_popup.ids['id_action_popup_submit_button'].bind(on_release=self.option_rename_file)
            case "save as":
                self.action_popup.ids['id_action_popup_submit_button'].bind(on_release=self.option_save_file_as)
            # case "save":
            #     self.action_popup.ids['id_action_popup_submit_button'].bind(on_release=self.option_save_file)

        self.action_popup.open()
    
    def open_video_save_popup(self):
        self.action_popup = ActionPopup(
            title_var = "Save as Video",
            button_text_var = "Save",
            auto_dismiss=False
        )
        self.action_popup.open()
        
        self.action_popup.ids['id_action_popup_submit_button'].bind(on_release=self.save_video_render)
    
    def save_video_render(self, *args):
        # caller_root = args[0].parent.parent.parent.parent
        text = self.action_popup.ids['id_action_popup_textinput'].text
        duration = 0
        if text.isnumeric():
            duration = float(text)

        #   call the Render Screen's render function
        render_screen_ref = self.manager.ids['id_render_screen']
        optional_args = {'videoCapture':True, 'videoCaptureDuration':duration,
                         'videoCapturePath':g_MOBILE_DOWNLOAD_STORAGE_PATH,
                         'videoContainerSize':render_screen_ref.size}
        render_screen_ref.render(self.title, kwargs=optional_args)
        self.action_popup.dismiss()
    

class RenderScreen(Screen):
    """
        This is the screen that displays the OpenGL Screen
    """
    code = StringProperty()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """
           This is the reference the keeps the OpenGL render
           object alive
        """
        self.render_object = None
        self.window_mode = 0

        #   to store the toolbar so it can be removed and appended
        self.toolbar_buttons_reference = []

    def render(self, srcCodeTitle: str, kwargs={}):
        #   get container reference
        render_container = self.ids['id_render_screen_container']

        #   Get source code path reference from the Editor Screen
        self.render_object = OpenglRender(srcCodeTitle, size_hint=(1.0, 0.5), **kwargs)
        render_container.add_widget(self.render_object)
    
    def release_render_object(self):
        render_container = self.ids['id_render_screen_container']
        render_container.remove_widget(self.render_object)
        self.render_object = None
        
    def maximize_window(self):
        #   first, store the toolbar widgets
        render_container = self.ids['id_render_screen_container']

        if len(self.toolbar_buttons_reference) == 0:
            for child in render_container.children:
                if str(type(child)).find("Button") != -1:
                    self.toolbar_buttons_reference.append(child)
                    
        #   flip and fullscreen
        self.window_mode = (self.window_mode + 1) % 3
        match self.window_mode:
            case 0:
                Window.size = Window.size[::-1]
                self.render_object.size_hint = (1.0, 0.5)
                for widget in self.toolbar_buttons_reference:
                    render_container.add_widget(widget)
            case 1:
                self.render_object.size_hint = (1.0, 1.0)
                for widget in self.toolbar_buttons_reference:
                    render_container.remove_widget(widget)
            case 2:
                self.render_object.size_hint = (1.0, 1.0)
                Window.size = Window.size[::-1]
            
        # print("Mode: ", self.window_mode)

    def on_touch_down(self, touch):
        """Callback for when the render screen is touched in FullScreen"""
        if self.window_mode != 0:
            self.maximize_window()
        return super().on_touch_down(touch)
    
    def save_snapshot(self):
        """
            Snapshot the render of the Opengl screen
            and save as png.
            The name is unique according to date and time
            It writes out the image to the IMAGE_EXPORT_PATH
        """
        target_path = os.path.join(os.getcwd(), "_exports")
        self.render_object.save_as_png(g_MOBILE_DOWNLOAD_STORAGE_PATH if g_MOBILE_DOWNLOAD_STORAGE_PATH else target_path)

class AppScreenManager(ScreenManager):
    """
        The root is the manager
    """
    def __init__(self, *args, **kwargs):
        super(AppScreenManager, self).__init__(*args, **kwargs)
        self.oninit()

    def oninit(self):
        self.init_main_screen()
    
    def init_main_screen(self):
        main_screen_ref = self.ids['id_main_screen']
        main_screen_ref.oninit()


class Lehitbonen(App):
    background_color = (0.07, 0.09, 0.13)
    
    def build(self):
        self.title = "Lehitbonen"
        Window.clearcolor = self.background_color
        Window.size = (324, 666)
        LabelBase.register(name="AtomicAge", fn_regular="./_resources/fonts/AtomicAge-Regular.ttf")
        LabelBase.register(name="Agbalumo", fn_regular="./_resources/fonts/Agbalumo-Regular.ttf")
        LabelBase.register(name="Baumans", fn_regular="./_resources/fonts/Baumans-Regular.ttf")
        LabelBase.register(name="Offside", fn_regular="./_resources/fonts/Offside-Regular.ttf")
        self.icon = "./icon.png"
        Builder.load_file("./base_style.kv")
        self.root = AppScreenManager() 
        self.root.width, self.root.height = Window.size

        return self.root


# if __name__ == "__main__":
#     output_list = []
#     target_path = os.path.join(os.path.dirname(__file__), "..", "programs")

#     for file in os.scandir(target_path):
#         info = {}
#         info['name'] = file.name
#         print(file.stat)
        