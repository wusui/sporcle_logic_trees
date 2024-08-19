# Copyright (C) 2024 Warren Usui, MIT License
"""
Create html file using homegrown template
"""
import copy

def save_colors(template, cchart):
    """
    Set colors in the style section
    """
    color_chrt = ''
    for figv in cchart:
        color_chrt += f'.{figv}color '
        color_chrt += '{ background-color: '
        color_chrt += f'{cchart[figv]}; '
        color_chrt += '}\n'
    return color_chrt.join(template.split('TL_COLORCHART'))

def make_table(olayout, layout, finale=False):
    """
    Make table inside html body
    """
    def fichk(flabel):
        if finale:
            if flabel != '-':
                return 'T'
        return flabel
    if len(layout) == 0:
        return ''
    otable = '<table border="1" class="dataframe">\n\t<tbody>\n'
    if not finale:
        otable += '\t\t<tr>\t\t\t<th></th>'
        for count in range(1, len(layout) + 1):
            otable += f'\t\t\t<th>{count}</th>'
        otable +='\t\t<tr>\n'
    for linfo in enumerate(layout):
        otable += '\t\t<tr>\n'
        if not finale:
            otable += '\t\t\t<th><div class="content">'
            otable += f'{linfo[0] + 1}</div></th>\n'
        for entry in enumerate(list(layout[linfo[0]])):
            otable += f'\t\t\t<td class="{olayout[linfo[0]][entry[0]]}color">'
            otable += f'<div class="content">{fichk(entry[1])}</div></td>\n'
        otable += "\t\t</tr>\n"
    otable += '\t</tbody>\n</table>\n'
    return otable

def set_font_size(template, sq_count):
    """
    Adjust fonts for different grid sizes
    """
    parts = template.split('TL_FONTSIZE')
    sizev = '40'
    if sq_count == 5:
        sizev = '80'
    if sq_count == 6:
        sizev = '60'
    return sizev.join(parts)

def make_html_file(in_data):
    """
    Main html creation function
    """
    with open('template.aard', 'r', encoding='utf-8') as fd_in:
        template = fd_in.read()
    template = save_colors(template, in_data[0])
    cntrl_data = in_data[1].split('\n')
    state = ''
    olayout = []
    layout = []
    hbody = ''
    gnumb = 0
    sfinal = False
    for in_cmd in cntrl_data:
        if in_cmd.startswith('<'):
            state = in_cmd
            if state != "<TITLE>":
                hbody += '<br>\n'
            continue
        if state == "<TITLE>":
            gnumb = in_cmd.split(' ')[-1]
            template = gnumb.join(template.split('TL_TITLE'))
        if state == "<BOARD>":
            if in_cmd != '':
                layout.append(in_cmd)
            else:
                if 'TL_FONTSIZE' in template:
                    template = set_font_size(template, len(layout))
                if not olayout:
                    olayout = copy.deepcopy(layout)
                hbody += make_table(olayout, layout, finale=sfinal)
                layout = []
        if state.startswith('<TEXT'):
            hbody += f'<p>{in_cmd}</p>\n'
            if in_cmd.startswith('Final Grid'):
                sfinal = True
    hbody += '<br><br>'
    new_html = hbody.join(template.split('TL_BODY'))
    with open(f'html/logic_tree_{gnumb}.html', 'w', encoding='utf-8') as ofd1:
        ofd1.write(new_html)
