'''
Replace rpc_user and rpc_password with user/login details for RPC server as defined
in ~/.woodcoin/woodcoin.conf
'''
# coding=utf-8
from woodcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

rpconn = AuthServiceProxy("http://%s:%s@127.0.0.1:8338"%(rpc_user, rpc_password))