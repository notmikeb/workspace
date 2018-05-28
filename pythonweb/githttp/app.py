#!/usr/bin/env python
# This is an example Git server. http://blog.nerds.kr/post/106956608369/implementing-a-git-http-server-in-python
# Stewart Park <stewartpark92@gmail.com> 

from flask import Flask, make_response, request, abort
from io import *
from dulwich.pack import PackStreamReader
import subprocess, os.path
#from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
#auth = HTTPBasicAuth()

users = {
    "john": "hello",
    "susan": "bye"
}

#@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None
    
@app.route('/<string:project_name>/info/refs')
#@auth.login_required
def info_refs(project_name):
    service = request.args.get('service')
    if service[:4] != 'git-': 
        abort(500)
    p = subprocess.Popen([service, '--stateless-rpc', '--advertise-refs', os.path.join('.', project_name)], stdout=subprocess.PIPE)
    packet = '# service=%s\n' % service
    length = len(packet) + 4
    _hex = '0123456789abcdef'
    prefix = ''
    prefix += _hex[length >> 12 & 0xf]
    prefix += _hex[length >> 8  & 0xf]
    prefix += _hex[length >> 4 & 0xf]
    prefix += _hex[length & 0xf]
    data = prefix + packet + '0000'
    data += p.stdout.read().decode('utf8')
    res = make_response(data)
    res.headers['Expires'] = 'Fri, 01 Jan 1980 00:00:00 GMT'
    res.headers['Pragma'] = 'no-cache'
    res.headers['Cache-Control'] = 'no-cache, max-age=0, must-revalidate'
    res.headers['Content-Type'] = 'application/x-%s-advertisement' % service
    #p.wait()
    print("end")
    import sys
    sys.stdout.flush()
    return res

@app.route('/<string:project_name>/git-receive-pack', methods=('POST','GET'))
#@auth.login_required
def git_receive_pack(project_name):
    p = subprocess.Popen(['git-receive-pack', '--stateless-rpc', os.path.join('.', project_name)], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    data_in = request.data
    print('data_in is ', type(data_in))
    print('data_in is ', data_in)
    pack_file = data_in[data_in.index('PACK'.encode('utf8')):]
    print('pack_file is ', pack_file)
    objects = PackStreamReader(BytesIO(pack_file).read)
    for obj in objects.read_objects():
        if obj.obj_type_num == 1: # Commit
            print(obj)
    print('before data_in')
    import sys
    sys.stdout.flush()
    p.stdin.write(data_in)
    p.stdin.flush()
    p.stdin.close()
    print('before data_out')
    import sys
    sys.stdout.flush()
    data_out = p.stdout.read()
    print('after stdout.read()')
    import sys
    sys.stdout.flush()
    res = make_response(data_out)
    res.headers['Expires'] = 'Fri, 01 Jan 1980 00:00:00 GMT'
    res.headers['Pragma'] = 'no-cache'
    res.headers['Cache-Control'] = 'no-cache, max-age=0, must-revalidate'
    res.headers['Content-Type'] = 'application/x-git-receive-pack-result'
    #p.wait()
    print("end")
    import sys
    sys.stdout.flush()
    return res

@app.route('/<string:project_name>/git-upload-pack', methods=('POST',))
#@auth.login_required
def git_upload_pack(project_name):
    p = subprocess.Popen(['git-upload-pack', '--stateless-rpc', os.path.join('.', project_name)], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.stdin.write(request.data)
    p.stdin.flush()
    p.stdin.close()
    data = p.stdout.read()
    res = make_response(data)
    res.headers['Expires'] = 'Fri, 01 Jan 1980 00:00:00 GMT'
    res.headers['Pragma'] = 'no-cache'
    res.headers['Cache-Control'] = 'no-cache, max-age=0, must-revalidate'
    res.headers['Content-Type'] = 'application/x-git-upload-pack-result'
    #p.wait()
    return res

if __name__ == '__main__':
    app.run()
