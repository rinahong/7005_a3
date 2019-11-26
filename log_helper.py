import datetime

log_file = None

def log(data, has_error, highlight):
    style_log = ''
    now = '[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + '] '

    if has_error:
        style_log = 'color:red;'
    if highlight:
        style_log += 'background-color: ' + highlight

    html_data = '<p style="' + style_log + '">' + now + data + '</p>'
    log_file.write(html_data.encode())

def init_log_file(file_name):
    global log_file
    log_file = open(file_name,'wb')
    html_data = '<ul>\n<li style="background-color:Yellow">Set timer</li>\n<li style="background-color:pink">Set timer due to retransmission</li>\n<li style="color:red">Undesirable ACK</li>\n<li style="background-color:grey">Retransmit packet</li>\n</ul>'
    html_data += '<h1>======================== Log file =====================</h1>\n'
    log_file.write(html_data.encode())

def terminate_log_file():
    log_file.close()
