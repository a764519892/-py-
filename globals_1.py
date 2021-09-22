import remi

config = {}

config['appname'] = 'REMI Template App'
config['author'] = 'Christian Kueken'
config['version'] = '1.0'
config['standalone'] = False
config['multiple_instance'] = True
config['port'] = 8080
config['address'] = '0.0.0.0'
config['start_browser'] = False
config['debug'] = False
config['enable_file_cache'] = False
config['update_interval'] = 0.1
config['rel_path_to_static'] = '/static'
config['base_padding'] = 10
config['navbar_height'] = 25

# SSL Configuration of REMI
config['rel_path_to_ssl_certfile'] = ''
config['rel_path_to_ssl_keyfile'] = ''
config['use_ssl_version'] = None



config['headdata'] = """
<meta name =“viewport”content =“width = device-width，初始刻度= 1”> <meta name =“描述”content =“smarterhouses”> <meta name =“作者”content =“christian kueken“> <链接rel =”stylesh“href =”/ static：css / w3 / w3.css“> <link rel =”stylesheet“href =”/ static：css / fa / css / all.css“> <脚本推迟src =“/ static：css / fa / js / all.js”> </ script> <link rel =“stylesh”href =“/ static：css / bootstrap4 / css / bootstrap.min.css”> <脚本src =“/ static：css / bootstrap4 / js / bootstrap.min.js”> </ script> <script src =“/static:js/jquery/jquery-3.4.1.slim.js"></script > <script src =“/static:js/popper/popper.min.js”> </ script> <script src =“/静态：js / popper / tooltip.min.js“> </ script> <link rel =”stylesheet“href =”https：//fonts.googleapis.com/css?family=roboto|roboto ackcondensed |lobster |tangerine “> <标题> Remi App </ Title> <style> HTML，Body {Padding：0;边缘：0;身高：100％;} .W3-Roboto {Font-Family：“Roboto”，Serif; } .W3-Roboto-Cond {Font-Family：“Roboto Confensed”，Serif; } .w3-lobster {font-family：“龙虾”，serif;字体大小：14px;文字阴影：无;} .w3-tangerine {font-family：“橘子”，serif;字体大小：24px;文字阴影：3px 3px 3px #aaa;} </ style>
"""

UserData = {}
