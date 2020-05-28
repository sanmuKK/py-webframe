from web import Application,render_template

app = Application()

@app.route('/',methods=['GET','POST'])
def index(request):#这里的func需要带一个request参数
    id = app.getdata('id','abaa')#因为方法都封装在Application里了，所以使用的时候都得带上app.的前缀
    pid = app.getdata('id','')
    print('id =',id)
    print('pid =',pid)
    return render_template('index.html',aa=id,cc='ddd',list=['1','3','2','4'])

@app.route('/id/<int:id>')
def id(request):
    id = app.getdata('id')
    return ("id is: {id}").format(id=id)

@app.route('/current_url')
def current_url(request):
    url = app.url_for("test")
    return "current url is {url}".format(url=url)

@app.route('/testurl')
def test(request):
    return render_template('index.html')

app.run(use_reloader=True)