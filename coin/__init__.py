import os, sys, docopt, time, hashlib, peer2peer

__version__ = "1.0.0"

def mk_xtn(action, name, wallet, message, remote_url):
    print("REMOTE", remote_url)
    wname = name+'/wallets/'+wallet+'.raw'
    sname = name+'/tmp/xtn.tmp'
    oname = name+'/tmp/xtn.tmp.out'
    with open(sname,'w') as xtn:
        from datetime import datetime
        xtn.write("date: " + datetime.now().isoformat() + "Z\n")
        xtn.write("action: " + action + "\n")
        xtn.write("message: " + message + "\n")
        pass
    ret = os.system('./krypto/sign/sign --seed %s -S <%s | cat - %s | tee %s | ./krypto/sign/sign -V' % (wname, sname, sname, oname))
    assert(ret == 0)
    h = hashlib.new('ripemd160')
    h.update(open(oname,'rb').read())
    hd = h.hexdigest()
    fname = '%s/xtns.tmp/%s' % (name, hd)
    os.system('mv %s %s' % (oname, fname))
    if remote_url:
        os.system("peer2peer.py pub %s xtn -<%s" % (remote_url, fname))
    return fname

def remove_chain(name):
    os.system("rm -fr " + name)

def create_chain(name, force=False):
    if force:
        remove_chain(name)
        time.sleep(0.02)
    os.mkdir(name)
    os.mkdir(name+'/wallets')
    os.mkdir(name+'/tmp')
    os.mkdir(name+'/xtns')
    os.mkdir(name+'/xtns.tmp') # when things get created
    os.mkdir(name+'/xtns.all') # kind of a dumping ground
    os.mkdir(name+'/blks')
    os.mkdir(name+'/blks.tmp')
    os.system('cat /dev/urandom 2>/dev/null| head -c 32 >%s/wallets/0.raw' % name)
    os.system('cat /dev/urandom 2>/dev/null| head -c 32 >%s/wallets/1.raw' % name)
    os.system('cat /dev/urandom 2>/dev/null| head -c 32 >%s/wallets/2.raw' % name)
    os.system('cat /dev/urandom 2>/dev/null| head -c 32 >%s/wallets/3.raw' % name)
    os.system('cd %s/wallets ; ln -s 0.raw root.raw' % name)
    os.system('tree -sh ' + name)

def main(args):
    if args['create-chain']:
        create_chain(args['<name>'], args['-f'] or args['--force'])
    elif args['remove-chain']:
        remove_chain(args['<name>'])
    elif args['create-cat']:
        mk_xtn('create', args['<name>'], args['<wallet>'], '', args['<remote-url>'])
    elif args['remove-cat']:
        mk_xtn('remove', args['<name>'], args['<wallet>'], '', args['<remote-url>'])
    elif args['rename-cat']:
        mk_xtn('rename', args['<name>'], args['<wallet>'], args['<new-name>'],args['<remote-url>'])
    elif args['meow']:
        mk_xtn('meow',   args['<name>'], args['<wallet>'], args['<message>'], args['<remote-url>'])
    elif args['purr']:
        mk_xtn('purr',   args['<name>'], args['<wallet>'], args['<message>'], args['<remote-url>'])
    elif args['hiss']:
        mk_xtn('hiss',   args['<name>'], args['<wallet>'], args['<message>'], args['<remote-url>'])
        pass
    pass
