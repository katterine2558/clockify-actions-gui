import datetime
import pytz

def convertir_a_formato_completo(hora_str):
    # Intentamos convertir el formato en HH:MM AM/PM
    try:
        hora_obj = datetime.datetime.strptime(hora_str, "%I:%M %p")
    except ValueError:
        # Si falla, intentamos con el formato HH:MM:SS AM/PM
        hora_obj = datetime.datetime.strptime(hora_str, "%I:%M:%S %p")

    # Convertimos al formato HH:MM:SS AM/PM
    hora_formato_completo = hora_obj.strftime("%I:%M:%S %p")
    
    return hora_formato_completo


def convert24HFormat(str1):

    if 'AM' in str1:
        if int(str1.split(':')[0])<=9:

            if str1.split(':')[0][0] == "0":
                hora = str1.split(':')[0]
            else:
                hora =  str1.split(':')[0]
                hora = f'0{hora}'
                
        elif int(str1.split(':')[0])== 12:
            hora = '00'
        else:
            hora =  str1.split(':')[0]

    else:
        if int(str1.split(':')[0])==12:
            hora = str1.split(':')[0]
        else:
            if int(str1.split(':')[0])>=1: 
                hora = int(str1.split(':')[0])+12  
            else:
                hora = str1.split(':')[0]

    minutos = str1.split(':')[1]
    segundos = str1.split(' ')[0].split(':')[2]
    hora = f'{hora}:{minutos}:{segundos}'

    return hora


def convertUTCHour(hour):

    timezone = pytz.timezone('America/Bogota')

    fecha = hour.split('T')[0]
    hora = hour.split('T')[1]

    anio = int(fecha.split('-')[0])
    mes = int(fecha.split('-')[1])
    dia = int(fecha.split('-')[2])

    h = int(hora.split(':')[0])
    m = int(hora.split(':')[1])

    original_time = datetime.datetime(anio, mes, dia, h, m)  # change this to sample datetime to test different values

    local_timezone_datetime = timezone.localize(original_time, False)  # change False to True if DST is enabled on the timezone

    converted_datetime = local_timezone_datetime.astimezone(pytz.utc)

    anio = converted_datetime.year
    mes = converted_datetime.month
    if mes < 10:
        mes = f'0{mes}'
    dia = converted_datetime.day
    if dia < 10:
        dia  = f'0{dia}'

    h =  converted_datetime.hour
    m = converted_datetime.minute

    if h < 10:
        h = f'0{h}'
    if m < 10:
        m = f'0{m}'

    hora = f'{anio}-{mes}-{dia}T{h}:{m}:00'

    return hora