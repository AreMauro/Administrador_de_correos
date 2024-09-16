import sqlite3
from pathlib import Path
from Usuario import Usuario
from cuentaCorreo import cuentaDeCorreo

class Datos():
    
    def __init__(self) -> None:
        
        if Path(".\\Datos\\basePrincipal.db").is_file() == False:
            
            self._con = sqlite3.connect(".\\Datos\\basePrincipal.db")
            self._cur = self._con.cursor()
            self._cur.execute("""CREATE TABLE IF NOT EXISTS USUARIO(usuario TEXT PRIMARY KEY,
                               password TEXT)""")
            self._cur.execute("""CREATE TABLE IF NOT EXISTS CUENTACORREO(usuario TEXT PRIMARY KEY,
                        Correo TEXT UNIQUE, password_de_la_cuenta TEXT, proveedor TEXT, 
                              FOREIGN KEY (usuario) REFERENCES USUARIO(usuario) ON DELETE CASCADE)""")
            
            self._con.execute("PRAGMA foreign_keys = ON")

        else:

            self._con = sqlite3.connect(".\\Datos\\basePrincipal.db")
            self._con.execute("PRAGMA foreign_keys = ON")
            self._cur = self._con.cursor()


    @property
    def cur(self) -> sqlite3.connect:
         
        return self._cur

    @property
    def con(self) -> sqlite3.Cursor :

         return self._con

    @cur.setter
    def cur(self, cursor) -> None:
         
        self._cur = cursor
    
    @con.setter
    def con(self, nuevaConexion) -> None:
         
        self._con = nuevaConexion

    def insertIntoUsuario(self, usuario: str, password:str) -> bool:

        try:
            if Usuario._verificadordeContrasegna(password) == True:


                self._cur.execute("""
                      INSERT INTO USUARIO ('usuario', 'password') 
                      VALUES (?, ?)""", (usuario, password))
        
                self._con.commit()

                return True
        except sqlite3.IntegrityError:

            print("Usuario ya registrado...")

            return False

        
    def getUsuario(self, usuario: str) -> Usuario:

        resultados = self._cur.execute(""" SELECT usuario, password FROM Usuario WHERE Usuario = ?""", (usuario,))
    
        usuario = resultados.fetchone()

        if usuario is not None:

            password = usuario[1]
            
            return Usuario(usuario, password)

        else: return None
        
    def insertIntoCuentadeCorreo(self, usuario:str, correo:str, passworCuenta: str,
                                  proveedor: str )  -> bool:
        try:

            if cuentaDeCorreo._verificarCorreo(correo) == True: 

                self._cur.execute("""
                      INSERT INTO CUENTACORREO(usuario, Correo, password_de_la_cuenta,
                      proveedor ) 
                      VALUES (?, ?, ?, ?)""", (usuario,correo, passworCuenta, proveedor))
        
                self._con.commit()

            return True
        except sqlite3.IntegrityError:

            print("Cuenta ya registrada...")
            return False

    def getCuenta(self, usuario:str) -> cuentaDeCorreo:

        try:
            resultados = self._cur.execute(""" SELECT *
                                       FROM CUENTACORREO WHERE Usuario = ?""", (usuario,))
    
            usuario,correo, password, proveedor = resultados.fetchone()

            if usuario is not None:
                return cuentaDeCorreo(correo, usuario, password, proveedor)
            else: return None
        
        except TypeError:

            return None

    def getAllUserData(self, usuario:str) -> tuple:

        resultados = self._cur.execute(""" Select usuario, password, Correo, password_de_la_cuenta,
                                             proveedor  FROM (
                                            SELECT *
                                            FROM Usuario 
                                            INNER JOIN CUENTACORREO
                                            ON Usuario.usuario = CUENTACORREO.Usuario)
                                            WHERE usuario = ?
                                            """, (usuario,))

        data = resultados.fetchone()

        if isinstance(data, tuple) == True:

            return data
        
        else: return None

    def getUserByCorreo(self, correo:str) ->Usuario :

        if self.getCuentaByCorreo(correo) is not None:

            usuario = self.getCuentaByCorreo(correo).usuario

            datos = self.getUsuario(usuario)

            return datos

    def getCuentaByCorreo(self, correo:str) -> cuentaDeCorreo:

        try:
            resultados = self._cur.execute(""" SELECT *
                                       FROM CUENTACORREO WHERE correo = ?""", (correo,))
    
            usuario,correo, password, proveedor = resultados.fetchone()

            if usuario is not None:
                return cuentaDeCorreo(correo, usuario, password, proveedor)
            
            else: return None
        
        except TypeError:

            return None

    def getAllDataByCorreo(self, correo:str) -> tuple: 

         if self.getCuentaByCorreo(correo) is not None:

            usuario = self.getCuentaByCorreo(correo).usuario

            return self.getAllUserData(usuario)


    def deleteUser(self, usuario:str) -> None:

        self._cur.execute(""" DELETE FROM Usuario 
                                    WHERE usuario = ?;
                                    """, (usuario,))
        self._con.commit()

        return self.getAllUserData(usuario)

    def deleteByCorreo(self, correo) -> None: 
        
        if self.getCuentaByCorreo(correo) is not None:

            usuario = self.getCuentaByCorreo(correo).usuario

            self.deleteUser(usuario)

            self._con.commit()

            return self.getAllUserData(usuario)
        else:
            print("El dato  no existe o  ya fue eliminado....")

    def cambiarContraseña(self, usuario: str, nuevaPassword: str) -> bool:

        if Usuario._verificadordeContrasegna(nuevaPassword) == True:

            try:
                contrasegnaActual = self.getUsuario(usuario).password

                self._cur.execute("""
                                UPDATE Usuario SET password = ? WHERE usuario = ?
                            """, (nuevaPassword, usuario))
                contrasegnaActualizada = self.getUsuario(usuario).password

                self._con.commit()

                return not(contrasegnaActual == contrasegnaActualizada)
            except:

                return None
        else: 
            print("Contraseña erronea")
            return False

    def cambiarContraseñaCuenta(self, usuario: str, nuevaPassword: str) -> bool: 

        cuenta =  self.getCuenta(usuario)

        if cuenta is not None:

            contrasegnaActual = cuenta.password

            self._cur.execute("""
                                UPDATE CUENTACORREO SET password_de_la_cuenta = ? WHERE usuario = ?
                            """, (nuevaPassword, usuario))
            
            self._con.commit()

            contrasegnaActualizada = self.getCuenta(usuario).password

            return not(contrasegnaActual == contrasegnaActualizada)

    def modificarProveedor(self, usuario:str, nuevoProveedor) -> bool: 

        bandera = self.getCuenta(usuario)

        if bandera is not None:

            proveedorActual = bandera.proveedor

            self._cur.execute("""
                                UPDATE CUENTACORREO SET proveedor = ? WHERE usuario = ?
                            """, (nuevoProveedor, usuario))
            
            self._con.commit()
            
            proveedorActualizado = self.getCuenta(usuario).proveedor

            return not(proveedorActual == proveedorActualizado)

      

    def modificarCorreo(self, usuario:str, correoNuevo) -> bool: 

        bandera = self.getCuenta(usuario)

        if bandera is not None:

            proveedorActual = bandera.proveedor

            self._cur.execute("""
                                UPDATE CUENTACORREO SET correo = ? WHERE usuario = ?
                            """, (correoNuevo, usuario))
            
            self._con.commit()

            proveedorActualizado = self.getCuenta(usuario).proveedor

            return not(proveedorActual == proveedorActualizado)







        
    
         


          