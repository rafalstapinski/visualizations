import web
import helpers as Help

class DB:

    @staticmethod
    def connect():
        return web.database(dbn=Help.Config.get('DB/dbn'),
                            db=Help.Config.get('DB/db'),
                            user=Help.Config.get('DB/user'),
                            pw=Help.Config.get('DB/pw'),
                            host=Help.Config.get('DB/host')
        )
