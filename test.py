import PySimpleGUI as sg

sg.theme('DarkAmber')
font = ('Courier New', 11)

headings = ['File', 'Parameter', 'foo', 'bar', 'baz', 'bam', 'biz']
data = []   # Empty data
col_widths = list(map(lambda x:len(x)+2, headings)) # find the widths of columns in character.
max_col_width = len('ParameterNameToLongToFitIntoAColumn')+2  # Set max midth of all columns of data to show

layout = [
    [sg.Table(
        values=data,                # Empty data must be with auto_size_columns=False
        headings=headings,
        auto_size_columns=False,    # For empty data
        #vertical_scroll_only=False,# Required if column widths changed and width of table not changed
        hide_vertical_scroll=True,  # Not required if no more rows of data
        def_col_width=20,
        num_rows=10,
        col_widths=col_widths,      # Define each column width as len(string)+2
        font=font,                  # Use monospaced font for correct width
        key='-TABLE-'),],
    [sg.Button('Update'),],
]
window = sg.Window('Title', layout, finalize=True)

char_width = sg.Text.char_width_in_pixels(font)     # Get character width in pixel
table = window['-TABLE-']
table_widget = table.Widget
table.expand(expand_x=True, expand_y=True)          # Expand table in both directions of 'x' and 'y'
for cid in headings:
    table_widget.column(cid, stretch=True)          # Set column stretchable when window resize

while True:

    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Update':
        data = [['A', 'ParameterNameToLongToFitIntoAColumn', 'C', 'D', 'E', 'F', 'G']]
        all_data = [headings] + data                # All data include headings
        # Find width in pixel and 2 extra characters for each column
        col_widths = [min([max(map(len, columns))+2, max_col_width])*char_width for columns in zip(*all_data)]
        table.update(values=data)                   # update all new data
        # Redraw table to update new size of table if horizontal scrollbar not used, care if widget too large to fit your window or screen.
        table_widget.pack_forget()
        for cid, width in zip(headings, col_widths):    # Set width for each column
            table_widget.column(cid, width=width)
        table_widget.pack(side='left', fill='both', expand=True)    # Redraw table

window.close()