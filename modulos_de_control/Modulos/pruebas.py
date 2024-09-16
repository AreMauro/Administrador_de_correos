from cuentaCorreo import cuentaDeCorreo
from Email import Email
from emaildresses import Obtener_correos_spam
from eliminarmails import Eliminar_Todos_los_emails, EliminarMailsporcorreo, EliminarMailsporFechaycorreo
from pprint import pprint
from baseDeDatos import Datos

nuevaCuenta = cuentaDeCorreo("enaruto2@gmail.com","Mauro16" ,"xumzfxvpugnjlgqx")


nuevaconexion = Datos()

nuevaconexion.insertIntoUsuario("Mauro16", "PUPE&wolf34")

nuevaconexion.insertIntoCuentadeCorreo("Mauro16", "enaruto2@gmail.com","xumzfxvpugnjlgqx", "gmail")

print(nuevaconexion.getCuenta("Mauro16"))

print(nuevaconexion.getUsuario("Mauro16"))

print(nuevaconexion.getAllDataByCorreo("enaruto2@gmail.com"))

print(nuevaconexion.getCuentaByCorreo("enaruto2@gamil.com"))

print(nuevaconexion.getCuentaByCorreo("enaruto2@gamil.com"))
print(nuevaconexion.getCuentaByCorreo("enaruto2@gamil.com"))

print(nuevaconexion.getUserByCorreo("enaruto2@gmail.com"))

nuevaconexion.modificarCorreo("Mauro16", "enaruto3@gmail.com")

nuevaconexion.cambiarContraseñaCuenta("Mauro16", "shhahahahahahhaha")

nuevaconexion.cambiarContraseña("Mauro16", "PUPE&wolf45")

nuevaconexion.modificarProveedor("Mauro16", "outlook")

print(nuevaconexion.getAllDataByCorreo("enaruto3@gmail.com"))

print(nuevaconexion.getCuentaByCorreo("enaruto3@gamil.com"))

print(nuevaconexion.getUserByCorreo("enaruto3@gmail.com"))

nuevaconexion.deleteUser("Mauro16")

nuevaconexion.insertIntoUsuario("Mauro16", "PUPE&wolf34")

nuevaconexion.insertIntoCuentadeCorreo("Mauro16", "enaruto2@gmail.com","xumzfxvpugnjlgqx", "gmail")

nuevaconexion.deleteByCorreo("enaruto2@gmail.com")

print(nuevaconexion.getAllUserData("Mauro16"))



""""
enviodeEmails = Email(nuevaCuenta)

correos = nuevaCuenta.getEmailsByAddress("noreply@redditmail.com")


#nuevaCuenta.Eliminar_spam("Gmail")




EliminarMailsporcorreo("groupupdates@facebookmail.com", 
                             "enaruto2@gmail.com","Mauro16" ,"xumzfxvpugnjlgqx")
"""