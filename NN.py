# Runs the handler and the file creation

from NnServer import NnServer

def main():
    handler = NnServer()
    handler.privateKeyFilePath = '/Users/nathannorth/Desktop'
    handler.create_private_key()

    handler.username = 'Nate'
    handler.password = 'default'
    handler.dataFilePath = '/Users/nathannorth/Documents/GitHub/NN-File-Formatter'

    handler.create_user_file()
    #handler.run_server()
    #handler.initialize_new_file('/Users/nathannorth/Desktop')

main()
