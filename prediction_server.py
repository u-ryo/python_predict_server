#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import keras, io, base64
from PIL import Image
import numpy as np

model_file = 'fruits.hdf5'
port = 8180
target_width = 224
target_height = 224
target_classes = ['bad', 'good']


model = keras.models.load_model(model_file)

class BaseHttpServer(BaseHTTPRequestHandler):
    def do_GET(self):
        s = '''
<!DOCTYPE html>
<html lang="ja">
  <head>
    <title>Image Check</title>
  </head>
  <body>
    <h3>Image Check</h3>
    <form>
      <label>Image File: <input id="file" type="file" accept="image/*" onChange="change()"/></label>
    </form>
    <p id="prediction"></p>
    <img id="img" src="" width="50%"/>
    <script>
      function change() {
        var reader = new FileReader();
        document.getElementById("prediction").innerHTML = "";
        var file = document.getElementById("file");
        // console.log(file.files[0].name);
        var filename = file.files[0].name;
        reader.onload = function() {
          document.getElementById("img").setAttribute("src", reader.result);
          var req = new XMLHttpRequest();
          req.onreadystatechange = function() {
            if (req.readyState == 4) {
              if (req.status == 200) {
                document.getElementById("prediction").innerHTML = req.responseText;
              } else {
                document.getElementById("prediction").innerHTML = "Request failed. " + req.status;
              }
            } else {
                document.getElementById("prediction").innerHTML = "Asking...";
            }
          };
          req.open("POST", "/", true);
          req.setRequestHeader("content-type", "application/x-www-form-urlencoded;charset=UTF-8");
          req.send(filename + "," + reader.result);
        }
        reader.readAsDataURL(file.files[0]);
      };
    </script>
  </body>
</html>
        '''
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(s, 'utf-8'))
        # print(s)

    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        content = self.rfile.read(content_len).decode('UTF-8')
        contents = content.split(',', 2)
        filename = contents[0]
        image = np.array(Image.open(io.BytesIO(base64.b64decode(contents[2])))
                         .resize((target_width, target_height))).transpose(1, 0, 2)
        image = np.expand_dims(image, axis=0)
        result = model.predict(image)
        # print(str(result))
        answer = target_classes[result[0].argmax()]
        print(filename + ':' + answer)
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-length', len(answer))
        self.end_headers()
        self.wfile.write(bytes(answer, 'utf-8'))

baseHttpServer = HTTPServer(('', port), BaseHttpServer)
try:
    baseHttpServer.serve_forever()
except KeyboardInterrupt:
    pass

baseHttpServer.server_close()
