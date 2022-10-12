from random import randint
import PySimpleGUI as sg

def random_color():
    return '#%02X%02X%02X' % (randint(0,255), randint(0,255), randint(0,255))

size = (640, 480)
layout = [
    [sg.Graph(size, (0, 0), size, background_color='green', expand_x=True, expand_y=True, pad=(0, 0), key='Graph')],
    [sg.Push(), sg.Button('Plot')],
]
window = sg.Window('Title', layout, resizable=True, margins=(0, 0), finalize=True)
graph, plot = window['Graph'], window['Plot']

## Change the pack order of Graph (row frame) to laste one.
# graph_row_frame_pack_info = graph.widget.master.pack_info()
# plot_row_frame_pack_info = plot.widget.master.pack_info()
# plot_row_frame_pack_info['side'] = 'bottom'
# plot.widget.master.pack(**plot_row_frame_pack_info)
# graph.widget.master.pack(**graph_row_frame_pack_info)

graph.bind('<Configure>', ' Configure')

while True:

    event, values = window.read()
    print(event)
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Graph Configure':
        e = graph.user_bind_event
        w0, h0 = graph.CanvasSize
        # Update the canvas size for coordinate conversion
        w1, h1 = graph.CanvasSize = e.width, e.height
        w_scale, h_scale = w1/w0, h1/h0
        graph.widget.scale("all", 0, 0, w_scale, h_scale)
        print(graph.CanvasSize)
    elif event == 'Plot':
        graph.erase()
        graph.draw_rectangle((100, 100), (540, 380), fill_color=random_color())
        graph.draw_arc((100, 380), (540, 430), 180, 180, fill_color=random_color())
        graph.draw_circle((320, 240), 140, fill_color=random_color())
        graph.draw_image(data=sg.EMOJI_BASE64_HAPPY_LAUGH, location=(100, 380))
        graph.draw_text('Hello World', location=(320, 240))

window.close()
