import kivy
kivy.require('1.7.1')

from kivy.app import App
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.lang import Builder, Parser, ParserException
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

class Slide(Screen):
    def __init__(self, **kwargs):
        super(Slide, self).__init__(**kwargs)
        self.get_keyboard()

    def get_keyboard(self):
        self._keyboard = Window.request_keyboard(
                self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        if self._keyboard is not None:
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'n':
            self.manager.current = self.manager.next()
        elif keycode[1] == 'b':
            self.manager.current = self.manager.previous()
        else:
            return False
        return True

class Container(BoxLayout):
    kv = StringProperty('')

    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)

    def on_kv(self, instance, value):
        try:
            parser = Parser(content=value.encode('utf-8'))
        except (SyntaxError, ParserException):
            return

        try:
            widget = Factory.get(parser.root.name)()
        except FactoryException:
            return

        Builder._apply_rule(widget, parser.root, parser.root)
        self.clear_widgets()
        self.add_widget(widget)

class TalkApp(App):
    pass

if __name__ == '__main__':
    TalkApp().run()
