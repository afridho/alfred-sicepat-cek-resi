def get_icon(partner):
    folderIcons = 'icons/'
    icon_name = partner.lower()
    ext = '.png'
    switcher = {
        'tokopedia': ''.join([folderIcons,icon_name,ext]),
    }
    return switcher.get(icon_name, 'icon.png')