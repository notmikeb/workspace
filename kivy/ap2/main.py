from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import *

class TreeWidget(FloatLayout):
    def __init__(self, **kwargs):
        super(TreeWidget, self).__init__(**kwargs)

        tv = TreeView(root_options=dict(text='Tree One'),
                      hide_root=False,
                      indent_level=4)

        populate_tree_view(tv, None, tree)

        self.add_widget(tv)

class PongGame(Widget):
    def PongGame(self):
        self.add_widget(TreeWidget())


class MyPaintApp(App):
    def build(self):
        return PongGame()


if __name__ == '__main__':
    MyPaintApp().run()