from Model.user import *
from Model.client import *
from Model.folder import *
from Model.timesheet import *
from Model.sso import *
from Model.timesheet import *

def setuproute(app, call):
    @app.route('/sso',                                  ['OPTIONS', 'GET'],           lambda x = None: call([sso_url])                                               )
    @app.route('/sso/conn/<>',                          ['OPTIONS', 'GET'],           lambda x = None: call([sso_token])                                             )

    @app.route('/users',                                ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, user_get_all])                        )
    @app.route('/user/<>',                              ['OPTIONS', 'GET'],           lambda x = None: call([sso_verify_token, user_set_by_id, user_get])            )
    @app.route('/user/<>',                              ['OPTIONS', 'PUT'],           lambda x = None: call([sso_verify_token, user_set_by_id, user_edit])           )
    @app.route('/user/<>',                              ['OPTIONS', 'DELETE'],        lambda x = None: call([sso_verify_token, user_set_by_id, user_delete])         )

    @app.route('/clients',                              ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, client_get_all])                      )
    @app.route('/client',                               ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, client_new, client_edit])             )
    @app.route('/client/<>',                            ['OPTIONS', 'GET'],           lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, client_get])        )
    @app.route('/client/<>',                            ['OPTIONS', 'PUT'],           lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, client_edit])       )
    @app.route('/client/<>',                            ['OPTIONS', 'DELETE'],        lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, client_delete])     )

    @app.route('/folders',                              ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, folder_get_all]) )
    @app.route('/client/<>/folders',                    ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, folder_get_all])                      )
    @app.route('/client/<>/folder',                     ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_new, folder_edit])             )
    @app.route('/client/<>/folder/<>',                  ['OPTIONS', 'GET'],           lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_set_by_id, folder_exist, folder_get])        )
    @app.route('/client/<>/folder/<>',                  ['OPTIONS', 'PUT'],           lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_set_by_id, folder_exist, folder_edit])       )
    @app.route('/client/<>/folder/<>',                  ['OPTIONS', 'DELETE'],        lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_set_by_id, folder_exist, folder_delete])     )


    @app.route('/user/<>/timesheets',                   ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, user_set_by_id, timesheet_get_all])                      )
    @app.route('/client/<>/timesheets',                 ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, timesheet_get_all])                      )
    @app.route('/client/<>/folder/<>/timesheet',        ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_set_by_id, folder_exist, timesheet_new, timesheet_edit])                      )
    @app.route('/client/<>/folder/<>timesheet/<>',      ['OPTIONS', 'GET'],           lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_set_by_id, folder_exist, timesheet_set_by_id, timesheet_exist, timesheet_get])                      )
    @app.route('/client/<>/folder/<>timesheet/<>',      ['OPTIONS', 'PUT'],           lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_set_by_id, folder_exist, timesheet_set_by_id, timesheet_exist, timesheet_edit])                      )
    @app.route('/client/<>/folder/<>timesheet/<>',      ['OPTIONS', 'DELETE'],        lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_set_by_id, folder_exist, timesheet_set_by_id, timesheet_exist, timesheet_delete])                      )
    def base():
        return
