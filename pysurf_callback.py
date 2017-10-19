import http.server  
import AjaxHandler
import subprocess
  
PORT = 19810 
  
def AjaxHandlerCallbackFunc(path):  
    content = b"None"  
    contenttype = "text/plain"  
    pathlist = path.split('?', 1)  
    #print (pathlist[0])
    #print (pathlist[1])
    if(pathlist[0] == "/pysurf.html"):  
        if(len(pathlist) == 1):  
            f = open("test.html", "rb")  
            content = f.read()  
            contenttype = "text/html"  
            f.close()  
        else:  
            args = pathlist[1].split('&')  
            cmd = args[0].split('=')  
            print (args)
            print (cmd[0])
            if cmd[0] == "cmd":
                print ("command")
                params = {}
                if len(args) > 1:
                    for arg in args[1:]:
                        param = arg.split(':')
                        val = param[1]
                        try:
                            val = int(val)
                        except ValueError:
                            try:
                                val = int(val)
                            except ValueError:
                                pass
                        params[param[0]] = val
                content = DispatchProcess(cmd[1], params)
            if cmd[0] == "json":
                print ("in json")  
                params = {}  
                if len(args) > 1:  
                    for arg in args[1:]:  
                        param = arg.split('=')  
                        val = param[1]  
                        try:  
                            val = int(val)  
                        except ValueError:  
                            try:  
                                val = float(val)  
                            except ValueError:  
                                pass  
                        params[param[0]] = val  
                content = DispatchCmd(cmd[1], params[0])  
    elif(pathlist[0] == "/favicon.ico"):  
        f = open("manji.png", "rb")  
        content = f.read()  
        contenttype = "image/png"  
        f.close()
    print (content)
    #print (contenttype)  
    return (content, contenttype)  
  
def DispatchCmd(cmd, args):
    print (cmd)
    print ('json: ', args)  
    return str({cmd:args}).encode()
    #return str({ll:}).encode() 

def DispatchProcess(cmd, args):
    print ('command: ' , cmd)
    print ('parameter: ' , args)
    for (k,v) in  args.items(): 
        print ("args[%s]=" % k,v )
    shell_command2 = cmd + ' ' + v
    status2, result2 = subprocess.getstatusoutput(shell_command2)
    shell_command1 = 'snmpwalk -v2c 211.152.50.254 -cpubl1c ifInOctets | grep \'ifInOctets.15\' '
    status, result = subprocess.getstatusoutput(shell_command1)
    
    print (str(result2).encode())
    return str(result2).encode()
    #return str(status2).encode()
    #return str(result).encode()
    #return str({cmd : args}).encode()
    #return str({ll:}).encode()
  
if __name__ == "__main__":  
    try:  
        AjaxHandler.callback = AjaxHandlerCallbackFunc  
        server = http.server.HTTPServer(("", PORT), AjaxHandler.AjaxHandler)  
        print("HTTP server is starting at port "+repr(PORT)+'...')  
        print("Press ^C to quit")  
        server.serve_forever()  
    except KeyboardInterrupt:  
        print("^Shutting down server...")  
        server.socket.close()  
