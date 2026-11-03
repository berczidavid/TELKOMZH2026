from socket import socket, AF_INET, SOCK_DGRAM, timeout

with socket(AF_INET, SOCK_DGRAM) as server:
  server_address = ('localhost', 10002)

  server.bind(server_address)
  server.settimeout(1.0)
  
  while True:
    try:
      data, client = server.recvfrom(1024)
      print("Received:", data.decode(), "From:", client)
      server.sendto("Hello client!".encode(), client)

      data, client = server.recvfrom(1024)
      req = data.decode()
					
      ask1 = req[0].decode().replace('\x00','')
      ask2 = req[1].decode().replace('\x00','')
      print("Vásárló kérése: ", ask1)
      print("Adat: ", ask2)
                    
      res = ""
      if ask1 == "tipus":
          for i in range(len(cars)):
              if cars[i][0] == ask2:
                  res = res + cars[i][0] + " " + cars[i][1] + " "  + cars[i][2] + "|"
      elif ask1 == "kor":
          for i in range(len(cars)):
              if cars[i][1] <= ask2:
                  res = res + cars[i][0] + " " + cars[i][1] + " "  + cars[i][2] + "|"
      elif ask1 == "ar":
          for i in range(len(cars)):
              if cars[i][2] <= ask2:
                  res = res + cars[i][0] + " " + cars[i][1] + " "  + cars[i][2] + "|"
      print('Kérésre válasz:', res)
      server.sendto(res.encode(), client)
    except timeout:
      pass
