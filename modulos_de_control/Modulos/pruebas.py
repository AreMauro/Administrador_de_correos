from cuentaCorreo import cuentaDeCorreo
from Email import Email
from pprint import pprint
from baseDeDatos import Datos


nuevaCuenta = cuentaDeCorreo("enaruto2@gmail.com","Mauro16" ,"xumzfxvpugnjlgqx")

nuevaCuenta.DescargarAtachmentsByAddress("enaruto2@gmail.com", ".")

nuevaCuenta.EliminarMailsporcorreo("messages@facebookmail.com")
""""
enviodeEmails = Email(nuevaCuenta)

correos = nuevaCuenta.getEmailsByAddress("noreply@redditmail.com")


#nuevaCuenta.Eliminar_spam("Gmail")




EliminarMailsporcorreo("groupupdates@facebookmail.com", 
                             "enaruto2@gmail.com","Mauro16" ,"xumzfxvpugnjlgqx")
"""