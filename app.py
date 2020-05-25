from web import Application,render_template

app = Application()

@app.route('/',methods=['GET','POST'])
def index(request):
    id = app.getdata('id','abaa')
    pid = app.getdata('id','')
    print('id =',id)
    print('pid =',pid)
    return render_template('index.html',aa=id,cc='ddd',list=['1','3','2','4'])

@app.route('/id/<int:id>')
def id(request):
    id = app.getdata('id')
    return "id is: %s" % id

@app.route('/current_url')
def current_url(request):
    url = app.urls.build("current_url")
    return "current url is %s" % url

app.run(use_reloader=True)