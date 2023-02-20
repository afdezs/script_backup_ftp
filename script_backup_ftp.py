# Propiedad de Adrian Fdz.

import os
import ftplib
import tarfile
import datetime
import smtplib
import hashlib
#from email.mime.text import MIMEText
from email.message import EmailMessage

import contrasena

# Uso de la contraseña encriptada
contraseña_encriptada = contrasena

# Uso de la contraseña encriptada en el script
print("La contraseña encriptada es:", contraseña_encriptada)

def desencriptar_contraseña(contraseña_encriptada):
    # Creación del objeto hash con sha256
    sha = hashlib.sha256()
    # Desencriptación de la contraseña
    contrasenaokey = sha.update(contraseña_encriptada.encode('utf-8'))
    # Devolución de la contraseña desencriptada
    return contrasenaokey

# Desencriptación de la contraseña
contrasenalimpia = desencriptar_contraseña(contraseña_encriptada)


# Directorio a copiar
directorio = '/var/www/html/public_html'
# Servidor FTP remoto
servidorFTP = 'IP_PUBLICA' #Tenemos asociado un subdominio a la IP pública
usuarioFTP = 'afernandez193'
contrasenaFTP = 'password'
# Número máximo de copias de seguridad
copiasMaximas = 10
# Correo del administrador
correoAdmin = 'jrivero32@ieszaidinvergeles.org'

# Obtener la fecha actual
fechaActual = datetime.datetime.now()
fechaCadena = fechaActual.strftime("%Y%m%d")

#Comprobamos si tiene todos los permisos.
#permisos = oct(os.stat(directorio).st_mode)[-3:]

# Crear nombre de archivo de copia de seguridad
nombreCopia = 'copia' + fechaCadena + '.tar.gz'

# Comprimir directorio
with tarfile.open(nombreCopia, mode='w:gz') as archive:
    archive.add(directorio, recursive=True)

# Conectarse al servidor FTP

#ftp = ftplib.FTP('192.168.112.7')
ftp_servidor = '192.168.112.15'
ftp_usuario  = 'afernandez193'
ftp_clave    = 'password'
ftp_raiz     = '/'
ftp=ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)

# ENCONTRAR CÓMO CIFRAR CONEXIÓN, CON ftplib.FTP_TLS
# Ejemplo:
# ftp=ftplib.FTP_TLS(ftp_servidor, ftp_usuario, ftp_clave, acct='', keyfile=None, certfile=None, context=None, timeout=None, source_address=None, encoding='utf-8')

# ftp.login('afernandez193', 'password')

# Subir archivo de copia de seguridad al servidor FTP
with open(nombreCopia, 'rb') as f:
    ftp.storbinary('STOR ' + nombreCopia, f)
print("Se ha subido la copia al servidor FTP.")

# Eliminar archivo de copia de seguridad local
os.remove(nombreCopia)

# Obtener lista de archivos de copia de seguridad en el servidor FTP
archivos = ftp.nlst()
compruebaArchivos = [f for f in archivos if f.startswith('copia')]

# Borrar archivos de copia de seguridad antiguos si hay más de 10
if len(compruebaArchivos) > copiasMaximas:
    copiaAntigua = min(compruebaArchivos, key=lambda x: x[5:])
    ftp.delete(copiaAntigua)
print("Se han eliminado los archivos antiguos de copia de seguridad.")

# Cerrar conexión FTP
ftp.quit()

"""
# Enviar e-mail de confirmación
remitente = 'ftpserver@ieszaidinvergeles.org'
receptor = correoAdmin
mensaje = 'La copia de seguridad del directorio public_html se ha realizado con éxito.'
msg = MIMEText(mensaje)
msg['Subject'] = 'Copia de seguridad completada'
msg['From'] = remitente
msg['To'] = receptor

server = smtplib.SMTP('smtp.example.com')
server.sendmail(remitente, [receptor], msg.as_string())

#La tarea se realizará todos los días a las 12:00h mediante crontab
os.system("(crontab -l ; echo '0 12 * * * /usr/bin/python3 " + nombreCopia + "') | crontab -")

#Cortamos la conexión
server.quit()
"""

#Envío de correo
remitente = "afernandez193@ieszaidinvergeles.org"
destinatario = "jrivero32@ieszaidinvergeles.org"
mensaje = "La copia de seguridad del servidor realizada con el script fue exitosa"
email = EmailMessage()
email["From"] = remitente
email["To"] = destinatario
email["Subject"] = "Copia de seguridad"
email.set_content(mensaje)
smtp = smtplib.SMTP_SSL("smtp.gmail.com")
# HABRÍA QUE CIFRAR LA CONTRASEÑA CON MD5 POR EJEMPLO
smtp.login(remitente, contrasenalimpia)
smtp.sendmail(remitente, destinatario, email.as_string())
smtp.quit()
print ("El correo fue enviado éxitosamente")
