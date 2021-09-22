import os, sys, logging, importlib
import core.globals                                 #＃使用Config Defaults的全局访问DICT  - >创建DICTS（在所有视图中导入此视图以访问数据）# Globally accessible Dicts with config defaults -> create Dicts (import this in all views to have access to the data)
import config.config                                #＃用户配置具有用户特定配置和其他用户数据 - >更改DICTS# User configuration with user specific config and additional User Data -> change Dicts
import core.webapi                                  #＃可以通过浏览器的地址栏访问的功能# Functions that can be accessed via the address bar of the browser
import helpers.connections
import remi



class WebApp(remi.server.App):

    def __init__(self, *args, **kwargs):
        static_path = sys.path[0] + core.globals.config['rel_path_to_static']

        self.logger = logging.getLogger('remi.app')
        self.views = {}                                     #＃应用实例的所有视图都驻留在此处# All views for the App Instance reside here
        self.connection_established = False                 #＃连接标志# Connection Flag
        self.connect_time = None                            #＃时间戳建立连接时# Timestamp when a connection was established
        self.disconnect_time = None                         #＃TimeStamp关闭时# Timestamp when a connection was closed

        super().__init__(static_file_path={'static': static_path}, *args, **kwargs)


    def _process_all(self, func):                   #＃过载_process_all方法路由方法# Overload _process_all method for routing
        print(f'{func}')                            #＃调试在原始URL后记录URL部分# Debug log the Url Part after the origin Url

        #＃跳过URL：在其中，因为这些是REMI Ressources，如Res：img / test.jpg等。# Skip Urls with : in it, because these are remi ressources like res:img/test.jpg etc.
        if not ':' in func:

            ###第一个捕获变量添加到url，如127.0.0.1:8080 /?fbclid=1354546321654# First catch variables added to the url like 127.0.0.1:8080/?fbclid=135454635461321651321654
            temp = func.split('?')
            ##print（str（temp））＃调试#print(str(temp))    # for debug

            for element in temp:                    #＃处理URL中的变量# Handle variables in url
                if 'fbclid' in element:
                    content = element.split('=')
                    self.logger.info(f'Facebook Click ID detected (content: {content[1]})')

                if 'myvar' in element:
                    self.logger.info('Somebody triggered myvar')

            if temp[0] == '/':
                remi.server.App._process_all(self, '/')     #＃当没有给出任何相对URL时，如果没有给出任何URL变量，请调用原始_process_all# Call the original _process_all without all the url variables when no relative url is given
                return

            else:
                rel_path = temp[0].split('/')               #＃沿着斜杠沿着斜线钻取URL，用于从相对URL构建视图名称# drill down the url further along slashes for building view names from relative urls
                ##print（str（rel_path））＃调试#print(str(rel_path))        # for debug

                #＃捕获URL并将其路由到视图# Catch URLS and route them to views
                if rel_path[1] != '' and rel_path[1] != 'favicon.ico' and rel_path[1] != 'api':     #来自规则的例外# Exceptions from rule
                    remi.server.App._process_all(self, '/')                                         #＃呼叫原始_process_all，没有所有的URL添加# Call the original _process_all without all the url additions
                    view_name = ''
                    for url_part in rel_path:                                                       #＃构建应用程序模板视图名称，该名称是模块# Build up the App Template view name which is a module
                        view_name = view_name + url_part
                        if len(view_name) > 0:
                            view_name = view_name + '.'
                    view_name = view_name[:-1]
                    ##print（view_name）＃用于调试#print (view_name)          # for debug
                    helpers.connections.client_route_url_to_view[self.session] = view_name   #＃存储稍后切换的URL扩展名称的视图名称（通过空闲）# Store the view name of url extension for later switching to view (via idle)
                    return

        #＃对于所有其他情况，Origin URL仍然是呼叫原始处理程序# For all other cases the origin URL stays untouched just call the original handler
        remi.server.App._process_all(self, func)


    def main(self):

        #＃调试信息# Debug Infos
        #＃打印（f'session id：{self.session}'）＃直接访问会话ID# print(f'Session ID: {self.session}')        # Direct access to session id
        #＃print（f'{remi.server.clents.items（）}'）＃dict与会话id作为key和webapp实例为值# print(f'{remi.server.clients.items()}')     # Dict with session id as key and WebApp instance as value

        #＃从配置插入磁头数据# Insert the headdata from config
        self.page.children['head'].add_child('additional_headdata', core.globals.config['headdata'])

        #＃通过HTML链接插入API小部件以进行访问# Insert the API Widget for access via HTML Links
        #＃id属性告诉子URL，其中remi可以找到API类。下一个URL部分是方法名称：http：// ip：port / api /方法？para1 = para？para2 = para# The ID attribute tells the sub url where remi can find the API class. Next url part is method name: http://ip:port/api/method?para1=para?para2=para
        self.api = core.webapi.Webapi(attributes={'id': 'api'}, AppInst=self)

        #＃基础窗口小部件是我们返回的GUI的绝对根（内部App Root是Self.root）# The base Widget is our absolute root of the GUI which is returned (Internal App root is self.root)
        #＃边缘：0px自动中心视图，填充：10 px在屏幕上留出10px的视图。盒子尺寸：边境箱力填充只能在容器内部# margin: 0px auto centers the view, padding: 10 px holds a distance of 10px around the screen for the views. box-sizing: border-box forces padding only to be active inside container
        self.base = remi.gui.Container(style={'margin': '0px auto' ,'padding': str(core.globals.config['base_padding']) + 'px', 'box-sizing': 'border-box'})

        #＃加载dict中的所有视图（ - > key =视图名称小写，value =视图容器的实例）# Load all views in Dict (-> key=name of view lowercase, value=instance of the view container)
        self.loadViews('views', self.views)

        #＃阅读所有可用视图后自动构建导航栏# After reading all available views build up the navbar automatically
        #＃每个视图都包含属性定义它应该显示它的菜单和哪个菜单文本# Every view contains attributes which define in which Menu it should be shown and with which Menu Text
        import views._navbar                                        #＃导入导航栏文件# Import the navbar file
        self.navbar = views._navbar.Container(AppInst=self)         #＃创建一个载体实例# Create a navbar Instance
        self.base.append(key='navbar', value=self.navbar)           #＃将纳瓦栏添加到基础窗口小部件# Add the navbar to the base widget

        #＃内容窗口小部件包含视图小部件。View窗口小部件包含视图。# The content Widgets holds the view widget. The view Widget holds the Views.
        #＃当我们切换视图时，我们只需从内容窗口小部件中删除实际视图小部件并从self.views [name]中添加另一个。# When we switch the view, we just remove the actual view widget from content widget and add another one from self.views[name]
        heightdiff = str(core.globals.config['navbar_height'] + 4 * core.globals.config['base_padding']) + 'px'
        self.content = remi.gui.Container(style={'overflow': 'auto', 'min-height': 'calc(100vh - ' + heightdiff + ')'})  #＃100VH = Viewport Height  -  NavBar_Height  -  4 * Base_Padding# 100vh = Viewport height - navbar_height - 4 * base_padding

        #＃将内容小部件附加到基础窗口小部件# Append the content widget to base widget
        self.base.append(key='content', value=self.content)

        #＃将已创建的开始视图附加到会话启动的内容容器# Append the already created Start View to the content Container for Session Startup
        self.content.append(key='view', value=self.views['start'])

        #＃返回基础窗口小部件# Return the base widget
        return self.base


    def idle(self):

        helpers.connections.handle_connections(AppInst=self)                        #＃管理传入和终止连接# Manage incoming and terminating connections

        #＃检查是否有来自URL路由的挂起视图交换机# Check if there is a pending view switch coming from URL routing
        if self.session in helpers.connections.client_route_url_to_view.keys() and self.connection_established == True:
            view = helpers.connections.client_route_url_to_view[self.session]       #＃存储通过URL给出的视图# Store the view given via URL
            del helpers.connections.client_route_url_to_view[self.session]          #＃从DICT中删除切换请求# Delete the switching request from Dict
            self.uiControl(self, view)                                              #＃最后切换到视图# Finally switch to the view

        if self.connection_established == True:                                     #＃如果连接存在，则调用活动视图的UpdateView方法# Call the updateView method of the active view if connection is alive
            self.content.children['view'].updateView()


    def uiControl(self, emittingWidget, view):
        #如果该方法直接绑定到窗口小部件事件，则需要#meplitwidgets# emittingWidgets is needed in Case that the method is bound to an widget event directly

        if hasattr(self, 'base'):
            if 'view' in self.base.children.keys():
                self.content.remove_child(self.content.children['view'])        #＃从内容小部件中删除旧视图# Remove the old view from content widget

        if view in self.views.keys():
            self.logger.info(f'session <{self.session}> switched to view {view}')
            self.content.append(key='view', value=self.views[view])     #＃如果存在视图，则显示它（添加到Content Widget）# If view is existent, show it (add to content widget)
        else:
            self.logger.info(f'session <{self.session}> tried to switch to view {view} which is not available.')
            self.content.append(key='view', value=self.views['error_view_not_found'])  #＃如果不存在视图，则切换到“开始”视图。你也可以留在实际观点# If view is not existent, switch to start view. You could also stay in actual view


    def loadViews(self, relative_src_folder, target_dict):

        #＃从SRC文件夹加载所有视图# Load all Views from src folder
        filelist = os.listdir(sys.path[0] + '/' + relative_src_folder)
        i = len(filelist) - 1

        while i >= 0:
            if filelist[i][0:1] == '_':                                     #＃删除带有前导下划线的元素（例如_UnderDevelopment.py）# Remove Elements with leading Underscore (e.g. _underDevelopment.py)
                del filelist[i]
            i = i - 1

        for element in filelist:
            element = element.lower()                                                        #＃将文件名标准化为小写# Standarize the filename to lowercase
            element = element.replace('.py', '')                                             #＃删除.py结尾# Remove .py ending
            elementClassName ="Container"                                                    #＃新remi编辑器函数始终使用ClassName'容器'导出视图# New Remi Editor Function exports Views always with Classname 'Container'
            importedView = importlib.import_module(relative_src_folder + '.' + element)      #＃从视图导入视图模块# Import the view module from views
            viewClass = getattr(importedView, elementClassName)                              #＃从模块和存储作为参考的容器类#＃从模块和存储作为参考的容器类# get the Container class from module and store as reference
            target_dict[element] = viewClass(AppInst=self)                                   #＃通过参考实例化视图并将其存储在目标区域内。将应用实例传递为arg。# Instanciate the view via the reference and store it in target dict. Pass App Instance as arg.


    def showDialog(self, emittingWidget, dialogname, layercolor='rgba(255, 255, 255, 0.6)', **kwargs):
        #＃显示视图作为对话框# Shows a view as a dialog
        #＃在实际视图上使用透明度插入分离层（在self.base容器的顶部附加）# Insert seperation layer with transparency over the actual view (append it on top of self.base container)
        #＃需要100％的视口，是固定的，这意味着它不会滚动。像这样，我们不必在底层容器中禁用小部件。# It takes 100% of the Viewport and is fixed which means it doesn't scroll. Like this we don't have to disable Widgets in underlying Container.
        self.layer = remi.gui.Container(width='calc(100VW)', height='calc(100VH)',
                                        style={'position': 'fixed', 'top': '0px', 'left': '0px', 'background-color': layercolor})
        self.base.append(key='layer', value=self.layer)                                     #＃在基础容器顶部设置图层# Set layer on top of the base Container
        dialogClassName = 'Container'                                                       #＃您可以使用Remi编辑器绘制对话框。这个班级将被命名为“容器”# You can draw dialogs with remi editor. The Class will be named always 'Container'
        viewmodule = importlib.import_module('dialogs.' + dialogname)                       #＃导入视图模块# Import the view module
        viewclass = getattr(viewmodule, dialogClassName)                                    #＃从模块和存储作为参考的容器类#＃从模块和存储作为参考的容器类# get the Container class from module and store as reference
        self.layer.append(key=dialogname, value=viewclass(AppInst=self, **kwargs))          #＃在图层顶部附加动态对话框# Append the dynamic dialog on top of the layer


    def hideDialog(self):
        self.base.remove_child(self.layer)                                                  #＃从基础容器中删除该图层# Remove the layer from the base Container
        del self.layer                                                                      #＃删除图层和其所有子项（=对话框）# Delete the layer and all of its children (=dialog)



##############用户示例的示例代码。模板不需要。############# Example Code for User examples. Not needed for the template.
    def printSentences(self, emittingWidget, amount):
        #＃此方法属于查看'句子'，并且是使用URL中选项的示例，并通过WebAPI.Webapi.sentences（self，金额）调用# This method belongs to view 'sentences' and is an example for using options in URLs and is called by webapi.Webapi.sentences(self, amount)
        output = ''
        sentence = 'THE QUICK BROWN FOX JUMPED OVER THE LAZY DOGS BACK 1234567890'
        i = 1

        while i <= int(amount):
            output = output + sentence + '\n'
            i = i + 1

        self.views['sentences'].textbox_sentences.set_value(output)         #＃全视图实例生活在内存中。您可以从此处更改值# All view Instances live in memory. You can change the value from here
        self.uiControl(emittingWidget, view='sentences')                    #＃将视图切换到句子（视图/句子中）# Switch the view to sentences (in views/sentences.py)


def startApp():
    # Function that starts the REMI App. You can integrate the entire GUI by just calling this function. If you spawn a new thread its non blocking.
    remi.server.start(core.webapp.WebApp,
                      address=core.globals.config['address'],
                      port=core.globals.config['port'],
                      multiple_instance=core.globals.config['multiple_instance'],
                      debug=core.globals.config['debug'],
                      start_browser = core.globals.config['start_browser'],
                      enable_file_cache=core.globals.config['enable_file_cache'],
                      update_interval = core.globals.config['update_interval'],
                      certfile = core.globals.config['rel_path_to_ssl_certfile'],
                      keyfile = core.globals.config['rel_path_to_ssl_keyfile'],
                      ssl_version = core.globals.config['use_ssl_version'])

