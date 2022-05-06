from kivy.metrics import dp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty, DictProperty, ListProperty
import datetime
from datetime import date
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivy.core.window import Window
from kivymd.uix.button import MDFloatingActionButtonSpeedDial
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.snackbar import Snackbar
from import_intents_doc import read_document, write_document
from tkinter import Tk
from tkinter import filedialog

Window.size = (600, 600)

sm = ScreenManager()


class MainScreen(Screen):
    pass


class TagCard(FakeRectangularElevationBehavior, MDFloatLayout, ThreeLineListItem):
    # tag item class
    patterns = ListProperty([])
    responses = ListProperty([])
    context = ListProperty([])
    data = DictProperty({})

    def update_data(self, data_):
        # update the data of current tag instance
        self.data = data_
        self.patterns = data_['patterns']
        self.responses = data_['responses']
        self.context = data_['context']

    def update_card(self):
        # update the data of the tag kv component
        patt_len = len(self.data["patterns"])
        res_len = len(self.data["responses"])
        str_patterns_count = f'patterns x{patt_len}'
        str_responses_count = f'responses x{res_len}'
        patterns_string = '; '.join(self.data["patterns"])
        responses_string = '; '.join(self.data["responses"])
        str_patterns_count += f': {patterns_string}'
        str_responses_count += f': {responses_string}'
        self.text = self.data['tag']
        self.secondary_text = str_patterns_count
        self.tertiary_text = str_responses_count


class IntentsManager(MDApp):
    # the list of dict objects representing imported data items
    document = ListProperty([])
    # the path the document is imported from and exported to
    doc_path = StringProperty(None)
    # to manage state in order to know if a selected doc of 'id' is being edited or a new tag is being added
    edit_state = DictProperty({
        "bool": False,
        "id": None,
    })
    # icons before import
    button_icon_empty = DictProperty({
        'Import': 'file-import',
    })
    # icons after import
    button_icon = DictProperty({
        'New': 'plus',
        'Import': 'file-import',
    })

    def build(self):
        # build the app screens
        main_screen = Builder.load_file('main.kv')
        new_tag_screen = Builder.load_file('new_tag.kv')

        # handle speed dial button
        speed_dial = MDFloatingActionButtonSpeedDial()
        speed_dial.id = 'speed_dial'
        speed_dial.data = self.button_icon_empty
        speed_dial.bg_hint_color = self.theme_cls.primary_light
        speed_dial.root_button_anim = True
        speed_dial.callback = self.speed_dial_callback
        speed_dial.on_open = self.speed_dial_open
        speed_dial.on_close = self.speed_dial_close
        speed_dial.on_leave = self.speed_dial_on_leave
        speed_dial.on_enter = self.speed_dial_on_enter

        # add screens and speed dial button to main app
        main_screen.add_widget(speed_dial)
        sm.add_widget(main_screen)
        sm.add_widget(new_tag_screen)

        # app caption
        self.title = 'Intents Manager'
        return sm

    def file_chooser(self):
        print(f"choosing file...")
        # file chooser to file import
        # filechooser.open_file(on_selection=self.handle_selected)
        chooser_tk = Tk()
        # hide the separate Tk window
        chooser_tk.withdraw()
        # the caption of the file chooser window
        chooser_tk.title('File Viewer')
        file_path = filedialog.askopenfilename(
            initialdir='./',
            title='Select JSON file',
            filetypes=(('json files', '*.json'), ('all files', '*.*'))
        )
        print(f'file_path: {file_path}')
        self.handle_selected([file_path])

    @staticmethod
    def parse_file_ext(full_path):
        # given a full path, return the extension type of the chosen file
        path_list = str(full_path).split('\\')
        full_path_list = path_list
        file_name = full_path_list[len(full_path_list) - 1]
        file_name_list = file_name.split('.')
        extension = file_name_list[len(file_name_list) - 1]
        return extension

    def reset_doc_data(self):
        # reset app's data
        self.document = ListProperty([])
        self.doc_path = StringProperty(None)

    def handle_selected(self, selection):
        try:
            # confirm file type is valid(JSON)
            if self.parse_file_ext(selection[0]) != 'json':
                error_txt = 'The file type selected is not supported. Only JSON files are supported.'
                raise TypeError(error_txt)
            # retrieve full path of selected file
            self.doc_path = selection[0]
            # read selected file and store data in app
            self.document = read_document(self.doc_path)
        except IndexError as e:
            self.reset_doc_data()
            print(f'You did not choose any file')
        except TypeError as e:
            self.reset_doc_data()
            print(f'{e}')
        finally:
            if self.doc_path is None:
                # no file was chosen or the file type was invalid
                error_txt = 'The file type selected is not supported. Only JSON files are supported.'
                Snackbar(
                    text=error_txt,
                    snackbar_x='10dp',
                    snackbar_y='10dp',
                    size_hint_y=.08,
                    size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                    bg_color=(1, 20 / 255, 100 / 255, 1),
                    font_size='18sp'
                ).open()
            return

    def handle_import_doc(self):
        # import button triggers this method
        print(f'importing...')
        self.file_chooser()

    @staticmethod
    def parse_ml_input(doc_str):
        # parse the multiline input to return a per-line, list of sentences
        ls = doc_str.split('\n')
        if len(ls) == 1 and ls[0] == '':
            ls = list()
        return ls

    @staticmethod
    def add_item(data):
        # add a new TagCard instance to the list view
        patt_len = len(data["patterns"])
        res_len = len(data["responses"])
        str_patterns_count = f'patterns x{patt_len}'
        str_responses_count = f'responses x{res_len}'
        patterns_string = '; '.join(data["patterns"])
        responses_string = '; '.join(data["responses"])
        str_patterns_count += f': {patterns_string}'
        str_responses_count += f': {responses_string}'
        sm.get_screen('main').tags_list \
            .add_widget(
            TagCard(
                text=data['tag'],
                patterns=data['patterns'],
                responses=data['responses'],
                context=data['context'],
                data=data,
                secondary_text=str_patterns_count,
                tertiary_text=str_responses_count
            ))

    def display_doc_data(self):
        # append as many TagCard instances as there are data items, to the list view
        for doc in self.document:
            self.add_item(doc)

    def speed_dial_callback(self, instance):
        selected_icon = instance.icon
        # speed dial pluas icon selected
        if selected_icon == 'plus':
            instance.parent.parent.parent.transition.direction = 'left'
            instance.parent.parent.parent.current = 'add_tag'
            # set the edit state to imply a new tag is to be added
            self.set_edit_state(None, False)
        elif selected_icon == 'file-import':
            # attempt to import an intents file
            self.handle_import_doc()
            # if a file was selected show the add tag button
            if self.doc_path is not None:
                instance.parent.data = self.button_icon
                # update the scroll view display
                self.display_doc_data()

    def speed_dial_open(self):
        pass

    def speed_dial_close(self):
        pass

    def speed_dial_on_leave(self, instance):
        pass

    def speed_dial_on_enter(self, instance):
        pass

    def on_start(self):
        # display current date at the top
        today = date.today()
        wd = date.weekday(today)
        days = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().strftime('%b'))
        day = str(datetime.datetime.now().strftime('%d'))
        sm.get_screen('main').date.text = f'{days[wd]}, {day} {month} {year}'

    @staticmethod
    def get_child(tag_name, exception=None):
        # return None or the TagCard component that has the given 'tag_name'
        for child_comp in sm.get_screen('main').tags_list.children:
            if exception != child_comp.text:
                if child_comp.text == tag_name:
                    return child_comp
        return None

    def get_child_doc_id(self, tag_name):
        # return the requested tag card of tag_name's index from within self.document
        for idx, doc in enumerate(self.document):
            if doc['tag'] == tag_name:
                return idx
        return -1

    def delete_tag(self, tag_name):
        # handle delete selected tag card
        child_id = self.get_child_doc_id(tag_name)
        child = self.get_child(tag_name)
        self.delete(child_id, child)

    def delete(self, tag_idx, child):
        # delete selected tag card component, passed as 'child'
        del self.document[tag_idx]
        sm.get_screen('main').tags_list.remove_widget(child)
        sm.transition.direction = "right"
        sm.current = "main"

    def set_edit_state(self, component, bool_val, tag_name=None):
        # handle edit/add state switching
        self.edit_state['bool'] = bool_val
        self.edit_state['id'] = tag_name

        if tag_name is None:
            # add new
            sm.get_screen('add_tag').ids['edit_page_label'].text = "New"
            sm.get_screen('add_tag').ids['tag_name_input'].text = ""
            sm.get_screen('add_tag').ids['patterns'].text = ""
            sm.get_screen('add_tag').ids['responses'].text = ""
            sm.get_screen('add_tag').ids['submit_change_btn'].text = "Add"
            self.show_delete_btn(False)
        else:
            sm.get_screen('add_tag').ids['edit_page_label'].text = "Edit"
            child = self.get_child(tag_name)
            sm.get_screen('add_tag').ids['tag_name_input'].text = child.data['tag']
            sm.get_screen('add_tag').ids['patterns'].text = "\n".join(child.data['patterns'])
            sm.get_screen('add_tag').ids['responses'].text = "\n".join(child.data['responses'])
            sm.get_screen('add_tag').ids['submit_change_btn'].text = "Save"
            self.show_delete_btn(True)

    @staticmethod
    def show_delete_btn(is_showing=True):
        # hide/show the delete button
        if is_showing:
            sm.get_screen("add_tag").ids['delete_tag_btn'].size_hint = (.20, .08)
            sm.get_screen("add_tag").ids['delete_tag_btn'].pos_hint = {"center_x": .5, "center_y": .9}
        else:
            sm.get_screen("add_tag").ids['delete_tag_btn'].size_hint = (None, None)
            sm.get_screen("add_tag").ids['delete_tag_btn'].pos_hint = {"center_x": -0.5, "center_y": -0.5}

    def handle_tag(self, deleting=False):
        if self.edit_state['id'] is None:
            # if not in editing state, then add new tag
            self.add_tag_item()
            self.reset_edit_state()
        else:
            # else in editing state so edit selected tag with id of self.edit_state['id']
            if not deleting:
                # show delete button
                self.edit_tag_item()
                self.reset_edit_state()
            else:
                # delete tag
                self.delete_tag(self.edit_state['id'])
        write_document(self.doc_path, self.document)

    def reset_edit_state(self):
        self.edit_state['bool'] = False
        self.edit_state['id'] = None

    def validate_tag_name(self, label, exception=None):
        # return None else the validated name if validated name is unique and is not the exception 'tag_name'
        # the exception is used in the edit state
        # to check every other tag name except the exception 'tag_name' itself
        if not label:
            return None
        tag_name = None
        temp = '_'.join(label.split(' '))
        child = self.get_child(temp, exception)
        is_duplicate = False if child is None else True
        if not is_duplicate:
            tag_name = temp
        return tag_name

    def add(self, new_tag_obj, tag):
        # add a new tag car comp based on the passed tag obj data and append to self.document this new data item
        new_tag_obj['tag'] = tag
        new_tag_obj['patterns'] = self.parse_ml_input(sm.get_screen('add_tag').ids['patterns'].text)
        new_tag_obj['responses'] = self.parse_ml_input(sm.get_screen('add_tag').ids['responses'].text)
        new_tag_obj['context'] = list()

        self.document.append(new_tag_obj)
        self.add_item(new_tag_obj)
        sm.transition.direction = "right"
        sm.current = "main"

    def edit(self, new_tag_obj, tag, orig_tag, child):
        # modify the chose tag component's data as well as its corresponding self.document item
        new_tag_obj['tag'] = tag
        new_tag_obj['patterns'] = self.parse_ml_input(sm.get_screen('add_tag').ids['patterns'].text)
        new_tag_obj['responses'] = self.parse_ml_input(sm.get_screen('add_tag').ids['responses'].text)
        new_tag_obj['context'] = list()
        doc_idx = self.get_child_doc_id(orig_tag)
        self.document[doc_idx] = new_tag_obj

        child.update_data(new_tag_obj)
        child.update_card()
        sm.transition.direction = "right"
        sm.current = "main"

    def add_tag_item(self, exception=None):
        # handle the adding and editing of tag component instancess
        new_tag_obj = dict()
        tag = self.validate_tag_name(sm.get_screen('add_tag').ids['tag_name_input'].text, exception)
        if tag is None:
            error_txt = 'This tag name already exists. Please try a different tag name.'
            Snackbar(
                text=error_txt,
                snackbar_x='10dp',
                snackbar_y='10dp',
                size_hint_y=.08,
                size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                bg_color=(1, 20 / 255, 100 / 255, 1),
                font_size='18sp'
            ).open()
        else:
            if exception is None:
                self.add(new_tag_obj, tag)
            else:
                self.edit(new_tag_obj, tag, exception, self.get_child(exception))

    def edit_tag_item(self):
        # handle edit tag component
        self.add_tag_item(self.edit_state['id'])
        sm.transition.direction = "right"
        sm.current = "main"


if __name__ == '__main__':
    app = IntentsManager()
    app.run()
# eof
