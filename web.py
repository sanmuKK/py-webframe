import os
from werkzeug.wrappers import Response, Request
from werkzeug.serving import run_simple
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, MethodNotAllowed
from jinja2 import Environment, FileSystemLoader

"""
定义一个Route类来管理url_map以及请求方式.
并加入__call__函数，使得可以直接对对象使用诸如Route()的操作.
__call__函数中再使用装饰器，这样操作起来就和Flask一样了
endpoint使用了对应的函数名.
从参数中获取并储存HTTP请求方法
"""
class Route:
    def __init__(self):
        self.url_map = Map([])
        self.endpoint_dict = {}
        self.methods_list = []

    def __call__(self, rules,**kwargs):
        def wrapper(func):
            endpoint = func.__name__
            self.url_map.add(Rule(rules, endpoint=endpoint))
            self.endpoint_dict[endpoint] = func
            for key, value in kwargs.items():
                if key == 'methods':
                    self.methods_list = value
            return func
        return wrapper

"""
定义了一个Application类
"""
class Application():

    def __init__(self):
        self.route = Route()#调用Route类

    def __call__(self, environ, start_response):
        return self.application(environ, start_response)

    def run(self,host='127.0.0.1',port=5000,use_reloader=False):#用run_simple定义一个运行方法
        run_simple(host, port, self, use_reloader=use_reloader)
        return

    def url_for(self,a):#返回对应endpoint的url
        return self.urls.build(a)

    @Request.application
    def application(self, request):
        self.urls = self.bind_to_environ(request.environ)
        if request.method not in self.route.methods_list:#如果请求方法不正确则返回MethodNotAllowed页面
            raise MethodNotAllowed
        try:
            endpoint, args = self.urls.match()#匹配请求参数
        except HTTPException as e:#如果找不到url则返回404
            return e
        return Response(self.route.endpoint_dict[endpoint](request), mimetype='text/html')#响应请求，类型为'text/html'

    def bind_to_environ(self, env):#用以绑定环境
        return self.route.url_map.bind_to_environ(env)

    def getdata(self, arg, *instead):#获取数据，如果没有对应数据则返回instead的值，类似flask的request.get('ex1','ex2')
        values = self.urls.match()[1]
        try:
            return values[arg]
        except:
            if instead[0] or instead[0] == '':
                values[arg] = instead[0]
            return values[arg]

"""
依然是render_template
将templates文件夹绑定了jinja2的环境
通过获取templates里html文件的文本并通过Application里方法响应到客户端
"""
def render_template(template_name, **context):
    template_path = os.path.join(os.getcwd(), 'templates')
    jinja_env = Environment(loader=FileSystemLoader(template_path),
                            autoescape=True)
    t = jinja_env.get_template(template_name)
    return t.render(context)