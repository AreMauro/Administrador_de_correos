from cuentaCorreo import cuentaDeCorreo
from Email import Email
from eliminarmails import EliminarMailsporFechaycorreo, EliminarMailsporcorreo
from emailConection import emailConection


nuevaCuenta = cuentaDeCorreo("enaruto2@gmail.com","Mauro16" ,"xumzfxvpugnjlgqx")

emails = nuevaCuenta.getEmailsByAddress("enaruto2@gmail.com")

print(f"Emails hallados: {len(emails)}")



print(nuevaCuenta.getConection() is nuevaCuenta.getConection())


for email in emails:

    print (Email(nuevaCuenta, email).getSender())

    break;

print (nuevaCuenta.closeConection())

""""
enviodeEmails = Email(nuevaCuenta)

correos = nuevaCuenta.getEmailsByAddress("noreply@redditmail.com")


#nuevaCuenta.Eliminar_spam("Gmail")

EliminarMailsporFechaycorreo("groupupdates@facebookmail.com", "30-jan-2024",
                             "enaruto2@gmail.com","Mauro16" ,"xumzfxvpugnjlgqx")


EliminarMailsporcorreo("groupupdates@facebookmail.com", 
                             "enaruto2@gmail.com","Mauro16" ,"xumzfxvpugnjlgqx")
"""