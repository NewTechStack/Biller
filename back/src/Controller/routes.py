from Model.user import *
from Model.client import *
from Model.folder import *
from Model.timesheet import *
from Model.sso import *
from Model.timesheet import *
from Model.bill import *

def setuproute(app, call):
    @app.route('/sso',                                  ['OPTIONS', 'GET'],           lambda x = None: call([sso_url])                                                                                                                                      )
    @app.route('/sso/conn/<>',                          ['OPTIONS', 'GET'],           lambda x = None: call([sso_token])                                                                                                                                    )

    @app.route('/users',                                ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, user_get_all])                                                                                                               )
    @app.route('/user/<>',                              ['OPTIONS', 'GET'],           lambda x = None: call([sso_verify_token, user_set_by_id, user_get])                                                                                                   )
    @app.route('/user/<>',                              ['OPTIONS', 'PUT'],           lambda x = None: call([sso_verify_token, user_set_by_id, user_edit])                                                                                                  )
    @app.route('/user/<>',                              ['OPTIONS', 'DELETE'],        lambda x = None: call([sso_verify_token, user_set_by_id, user_exist, user_delete])                                                                                    )

    @app.route('/clients',                              ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, client_get_all])                                                                                                             )
    @app.route('/client',                               ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, client_new, client_edit])                                                                                                    )
    @app.route('/client/<>',                            ['OPTIONS', 'GET'],           lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, client_get])                                                                                 )
    @app.route('/client/<>',                            ['OPTIONS', 'PUT'],           lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, client_edit])                                                                                )
    @app.route('/client/<>',                            ['OPTIONS', 'DELETE'],        lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, client_delete])                                                                              )

    @app.route('/folders',                              ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, folder_get_all])                                                                                                             )
    @app.route('/user/<>/folders',                      ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, user_set_by_id, user_exist, folder_get_by_user])                                                                             )
    @app.route('/client/<>/folders',                    ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, folder_get_all])                                                                                                             )
    @app.route('/client/<>/folder',                     ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_new, folder_edit])                                                                    )
    @app.route('/client/<>/folder/<>',                  ['OPTIONS', 'GET'],           lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_set_by_id, folder_exist, folder_get])                                                 )
    @app.route('/client/<>/folder/<>',                  ['OPTIONS', 'PUT'],           lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_set_by_id, folder_exist, folder_edit])                                                )
    @app.route('/client/<>/folder/<>',                  ['OPTIONS', 'DELETE'],        lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_set_by_id, folder_exist, folder_delete])                                              )

    @app.route('/timesheets',                           ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, timesheet_get_all])                                                                                                          )
    @app.route('/timesheets/sum',                       ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, timesheet_get_all_sum])                                                                                                          )
    @app.route('/user/<>/timesheets',                   ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, user_set_by_id, user_exist, timesheet_get_all])                                                                              )
    @app.route('/client/<>/timesheets',                 ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, timesheet_get_all])                                                                          )
    @app.route('/client/<>/folder/<>/timesheet',        ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_set_by_id, folder_exist, timesheet_new, timesheet_edit])                              )
    @app.route('/client/<>/folder/<>/timesheet/<>',     ['OPTIONS', 'GET'],           lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_set_by_id, folder_exist, timesheet_set_by_id, timesheet_exist, timesheet_get])        )
    @app.route('/client/<>/folder/<>/timesheet/<>',     ['OPTIONS', 'PUT'],           lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_set_by_id, folder_exist, timesheet_set_by_id, timesheet_exist, timesheet_status_under_2, timesheet_edit])       )
    @app.route('/client/<>/folder/<>/timesheet/<>',     ['OPTIONS', 'DELETE'],        lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_set_by_id, folder_exist, timesheet_set_by_id, timesheet_exist, timesheet_status_under_2, timesheet_delete])     )
    @app.route('/client/<>/folder/<>/timesheet/<>/status',   ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_set_by_id, folder_exist, timesheet_set_by_id, timesheet_exist, timesheet_change_status])             )

    @app.route('/bills',                                ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, bill_get_all])                                                                                                               )
    @app.route('/bills/sum',                           ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, bill_get_all_sum])                                                                                                               )
    @app.route('/client/<>/bills',                      ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, bill_get_all])                                                                               )
    @app.route('/client/<>/folder/<>/bills',            ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_set_by_id, folder_exist, bill_get_all])                                               )
    @app.route('/client/<>/folder/<>/bill',             ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_set_by_id, folder_exist, bill_new, bill_edit])                                        )
    @app.route('/client/<>/folder/<>/bill/<>',          ['OPTIONS', 'GET'],           lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_set_by_id, folder_exist, bill_set_by_id, bill_exist, bill_get])                       )
    @app.route('/client/<>/folder/<>/bill/<>',          ['OPTIONS', 'PUT'],           lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_set_by_id, folder_exist, bill_set_by_id, bill_exist, bill_status_under_2, bill_edit])       )
    @app.route('/client/<>/folder/<>/bill/<>',          ['OPTIONS', 'DELETE'],        lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_set_by_id, folder_exist, bill_set_by_id, bill_exist, bill_status_under_2, bill_delete])     )
    @app.route('/client/<>/folder/<>/bill/<>/status',   ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, client_set_by_id, client_exist, folder_set_by_id, folder_exist, bill_set_by_id, bill_exist, bill_change_status])             )
    
    @app.route('/banks',                                ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, bank_get_all])                                                                                                               )
    @app.route('/bank/<>',                              ['OPTIONS', 'GET'],           lambda x = None: call([sso_verify_token, bank_set_by_id, bank_get])                                                                                                   )
    @app.route('/bank/<>',                              ['OPTIONS', 'PUT'],           lambda x = None: call([sso_verify_token, bank_set_by_id, bank_edit])                                                                                                  )
    @app.route('/bank/<>',                              ['OPTIONS', 'DELETE'],        lambda x = None: call([sso_verify_token, bank_set_by_id, bank_exist, bank_delete])) 
    
    @app.route('/v2/folders',                           ['OPTIONS', 'GET'],          lambda x = None: call([sso_verify_token, folders_v2]))
    @app.route('/v2/timsheet',                          ['OPTIONS', 'GET'],          lambda x = None: call([sso_verify_token, timesheets_all]))
    @app.route('/v2/timsheet/byfolders',                ['OPTIONS', 'GET'],          lambda x = None: call([sso_verify_token, timesheets_by_folder]))
    @app.route('/v2/bill',                              ['OPTIONS', 'GET'],          lambda x = None: call([sso_verify_token, bills_all]))


    def base():
        return
