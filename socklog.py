import socket, os, datetime, argparse

FILESIZE_LIMIT = 10 * 1024 * 1024
DEBUG = False

log_name = 'pharmaseq.log'
port = 8877


def debug_write(msg):
    if DEBUG: print msg

def archive_logfile():
    datestr = datetime.datetime.now().strftime('%Y.%m.%d')
    try_rename(datestr, 0)

def try_rename(datestr, tries):
    try:
        suffix = '' if tries == 0 else '.' + str(tries)
        new_name = log_name + '.' + datestr + suffix
        print new_name
        os.rename(log_name, new_name)
    except OSError:
        tries += 1
        if tries < 50: try_rename(datestr, tries)

def write_msg(msg):
    print log_name
    if os.path.exists(log_name) and os.path.getsize(log_name) > FILESIZE_LIMIT:
        archive_logfile()
    f = open(log_name, 'a')
    f.write(msg)
    f.flush()
    
def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind( ('', port) )
    
    if DEBUG: server_listen(s)
    else:
        while True:
            server_listen(s)

def server_listen(s):
    max_packet_size = 1024 * 1024;
    d, a = s.recvfrom(max_packet_size)
    debug_write("Connected: " + str(a))
    write_msg(d)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='UDP Receiver/Writer')
    parser.add_argument('-n', '--name', metavar='name')
    parser.add_argument('-p', '--port', metavar='port')
    args = parser.parse_args()
    if args.name:
        global log_name
        log_name = str(args.name) + '.log'
    if args.port:
        global port
        port = int(args.port)
    start_server()