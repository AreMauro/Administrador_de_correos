from cuentaCorreo import cuentaDeCorreo
from Email import Email
nuevaCuenta = cuentaDeCorreo("enaruto2@gmail.com","Mauro16" ,"xumzfxvpugnjlgqx", "llljjk")

nuevaCuenta.proveedor = "gma l"

nuevaCuenta.puerto = 993

nuevaCuenta.puerto_ssl = 465

nuevaCuenta.smtp = 'smtp.gmail.com'

emails = nuevaCuenta.getEmailsByAddress("updates@academia-mail.com")



if emails:
    
    print(len(emails))

    for email in emails:

        emailnuevo = Email(email, nuevaCuenta)

        print(emailnuevo.getSender())

        emailnuevo.EliminarEmail()
        
        emails2 = nuevaCuenta.getEmailsByAddress("updates@academia-mail.com")

        print(len(emails2))


        break;


